#!/usr/bin/env python3
"""
selection, and writes a flat ntuple.  Output format is determined by the
file extension you give --output:

Selection (mirrors the CMSSW EDAnalyzer H4lNtuplizer.cc):

  0  HLT_IsoMu24
  1  HLT_IsoMu27
  2  HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8
  3  HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8
  4  HLT_Ele32_WPTight_Gsf
  5  HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
  6  HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ
  7  HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ
  8  HLT_TripleMu_12_10_5
  9  HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
  10 HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ

Requirements:
  pip install uproot awkward numpy pyarrow tqdm

Usage:
  python h4l_ntuplize.py \\
      --input step5_NANO.root [more_NANO.root ...] \\
      --output h4l_ntuple.parquet \\
      [--tree Events] \\
      [--chunk 50000] \\
      [--workers 4]

  python h4l_ntuplize.py --input step5_NANO.root --output h4l_ntuple.root
"""

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import awkward as ak
import uproot

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HLT_PATHS = [
    "IsoMu24",                                         # bit 0
    "IsoMu27",                                         # bit 1
    "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",       # bit 2
    "Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",          # bit 3
    "Ele32_WPTight_Gsf",                               # bit 4
    "Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",             # bit 5
    "Mu8_DiEle12_CaloIdL_TrackIdL_DZ",                # bit 6
    "DiMu9_Ele9_CaloIdL_TrackIdL_DZ",                 # bit 7
    "TripleMu_12_10_5",                                # bit 8
    "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",  # bit 9
    "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", # bit 10
]

MZ = 91.1876  # GeV

DEFAULTS = dict(
    minMuPt=5.0,  minElPt=7.0,
    maxMuEta=2.4, maxElEta=2.5,
    maxSip3d=4.0, maxDxy=0.5, maxDz=1.0, maxRelIso=0.35,
    minZ1m=12.0,  maxZ1m=120.0,
    minZ2m=4.0,   maxZ2m=120.0,
    minM4l=70.0,
)

# ---------------------------------------------------------------------------
# Physics helpers
# ---------------------------------------------------------------------------

def _p4_sum(*p4s):
    """Sum four-vectors given as (pt, eta, phi, mass) tuples. Returns (px,py,pz,e)."""
    px = py = pz = e = 0.0
    for pt, eta, phi, mass in p4s:
        cph, sph = np.cos(phi), np.sin(phi)
        ch, sh   = np.cosh(eta), np.sinh(eta)
        px += pt * cph
        py += pt * sph
        pz += pt * sh
        e  += np.hypot(pt * ch, mass)
    return px, py, pz, e


def inv_mass(*p4s):
    px, py, pz, e = _p4_sum(*p4s)
    m2 = e**2 - px**2 - py**2 - pz**2
    return float(np.sqrt(max(m2, 0.0)))


def rapidity(*p4s):
    _, _, pz, e = _p4_sum(*p4s)
    return 0.5 * np.log((e + pz) / (e - pz + 1e-30))


def system_pt_eta_phi(*p4s):
    px, py, pz, e = _p4_sum(*p4s)
    pt  = np.hypot(px, py)
    phi = np.arctan2(py, px)
    eta = np.arcsinh(pz / (pt + 1e-30))
    return float(pt), float(eta), float(phi)


def dr2(eta1, phi1, eta2, phi2):
    dphi = (phi1 - phi2 + np.pi) % (2 * np.pi) - np.pi
    return (eta1 - eta2)**2 + dphi**2

# ---------------------------------------------------------------------------
# Per-event quadruplet search
# ---------------------------------------------------------------------------

def find_best_quadruplet(leps, cuts):
    """
    leps: list of dicts with keys pt, eta, phi, mass, charge, pdgId,
          dxy, dz, dxyErr, dzErr, sip3d, ip3d, pfRelIso03, miniRelIso,
          muMedium, muTight, muGlobal, muPF, elCutBased, elMvaWP90,
          elMvaWP80, elMvaBdt.

    Returns dict with all output fields or None if no valid quadruplet.
    """
    N = len(leps)
    if N < 4:
        return None

    best_mZ1   = -1.0
    best_result = None

    # C(N,4) combinations 
    for combo in itertools.combinations(range(N), 4):
        ls = [leps[i] for i in combo]

        # Ghost removal
        ghost = False
        for a, b in itertools.combinations(range(4), 2):
            if dr2(ls[a]['eta'], ls[a]['phi'], ls[b]['eta'], ls[b]['phi']) < 4e-4:
                ghost = True
                break
        if ghost:
            continue

        # Three possible SFOS pairings
        for (pa, pb), (pc, pd) in [((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))]:
            la, lb = ls[pa], ls[pb]
            lc, ld = ls[pc], ls[pd]

            if abs(la['pdgId']) != abs(lb['pdgId']) or la['charge'] == lb['charge']:
                continue
            if abs(lc['pdgId']) != abs(ld['pdgId']) or lc['charge'] == ld['charge']:
                continue

            mab = inv_mass((la['pt'], la['eta'], la['phi'], la['mass']),
                           (lb['pt'], lb['eta'], lb['phi'], lb['mass']))
            mcd = inv_mass((lc['pt'], lc['eta'], lc['phi'], lc['mass']),
                           (ld['pt'], ld['eta'], ld['phi'], ld['mass']))

            # Z1 = pair closest to mZ
            if abs(mab - MZ) <= abs(mcd - MZ):
                mZ1, mZ2 = mab, mcd
                z1 = [combo[pa], combo[pb]]
                z2 = [combo[pc], combo[pd]]
                z1l = [la, lb];  z2l = [lc, ld]
            else:
                mZ1, mZ2 = mcd, mab
                z1 = [combo[pc], combo[pd]]
                z2 = [combo[pa], combo[pb]]
                z1l = [lc, ld];  z2l = [la, lb]

            if not (cuts['minZ1m'] <= mZ1 <= cuts['maxZ1m']): continue
            if not (cuts['minZ2m'] <= mZ2 <= cuts['maxZ2m']): continue

            # Leading/subleading pT on Z1
            z1pts = sorted([z1l[0]['pt'], z1l[1]['pt']], reverse=True)
            if z1pts[0] < 20.0 or z1pts[1] < 10.0:
                continue

            # QCD suppression: all OS lepton pairs > 4 GeV
            qcd_ok = True
            for a, b in itertools.combinations(range(4), 2):
                if ls[a]['charge'] != ls[b]['charge']:
                    mll = inv_mass((ls[a]['pt'], ls[a]['eta'], ls[a]['phi'], ls[a]['mass']),
                                   (ls[b]['pt'], ls[b]['eta'], ls[b]['phi'], ls[b]['mass']))
                    if mll < 4.0:
                        qcd_ok = False
                        break
            if not qcd_ok:
                continue

            # 4l mass
            m4l = inv_mass(*((l['pt'], l['eta'], l['phi'], l['mass']) for l in ls))
            if m4l < cuts['minM4l']:
                continue

            # Best candidate: highest mZ1
            if mZ1 <= best_mZ1:
                continue
            best_mZ1 = mZ1

            # Sort each Z pair by pT descending
            if z1l[0]['pt'] < z1l[1]['pt']:
                z1, z1l = z1[::-1], z1l[::-1]
            if z2l[0]['pt'] < z2l[1]['pt']:
                z2, z2l = z2[::-1], z2l[::-1]

            quad = z1l + z2l
            pt4l, eta4l, phi4l = system_pt_eta_phi(
                *((l['pt'], l['eta'], l['phi'], l['mass']) for l in quad))

            nmu = sum(1 for l in quad if abs(l['pdgId']) == 13)
            fstate = 0 if nmu == 4 else (1 if nmu == 0 else 2)

            best_result = dict(
                mZ1=mZ1, mZ2=mZ2, m4l=m4l,
                pt4l=pt4l, eta4l=eta4l, phi4l=phi4l,
                y4l=float(rapidity(*((l['pt'], l['eta'], l['phi'], l['mass']) for l in quad))),
                finalState=fstate,
                quad=quad,
                zId=[1, 1, 2, 2],
            )

    return best_result

# ---------------------------------------------------------------------------
# Branch readers  (graceful fallback for missing columns)
# ---------------------------------------------------------------------------

def _ak_field(arr, name, default):
    """Return arr[name] if the field exists, otherwise an array of `default`."""
    if name in ak.fields(arr):
        return arr[name]
    return ak.full_like(arr[ak.fields(arr)[0]], default, dtype=type(default))


def read_chunk(chunk, cuts):
    """
    chunk: dict of awkward arrays read from one uproot iterate batch.
    Returns a list of row-dicts, one per passing event.
    """
    rows = []
    nevt = len(chunk['run'])

    for iev in range(nevt):
        if iev % 1000 == 0:
            print("Processes..",iev,"/",nevt)
        # ---- Build lepton list ---------------------------------------------
        leps = []
        
        # NANOGEN mode: use GenDressedLepton when reco collections are absent
        #print(chunk['nGenDressedLepton'],"check")
        if 'nGenDressedLepton' in chunk.fields and 'nMuon' not in chunk.fields:
            ndl = int(chunk['nGenDressedLepton'][iev])
            for i in range(ndl):
                def gl(b, d=0.0, _iev=iev, _i=i):
                    v = chunk.get(b)
                    return float(v[_iev][_i]) if v is not None else d
                def gli(b, d=0, _iev=iev, _i=i):
                    v = chunk.get(b)
                    return int(v[_iev][_i]) if v is not None else d

                pdgId = gli('GenDressedLepton_pdgId')
                pt    = gl('GenDressedLepton_pt')
                eta   = gl('GenDressedLepton_eta')
                
                if abs(pdgId) == 13:
                    if pt < cuts['minMuPt'] or abs(eta) > cuts['maxMuEta']:
                        continue
                elif abs(pdgId) == 11:
                    if pt < cuts['minElPt'] or abs(eta) > cuts['maxElEta']:
                        continue
                else:
                    continue

                charge = -1 if pdgId > 0 else 1
                ismu = abs(pdgId) == 13
                leps.append(dict(
                    pt=pt, eta=eta, phi=gl('GenDressedLepton_phi'),
                    mass=gl('GenDressedLepton_mass'),
                    charge=charge, pdgId=pdgId,
                    dxy=0.0, dz=0.0, dxyErr=0.0, dzErr=0.0,
                    sip3d=0.0, ip3d=0.0,
                    pfRelIso03=0.0, miniRelIso=0.0,
                    muMedium=int(ismu), muTight=int(ismu),
                    muGlobal=int(ismu), muPF=int(ismu),
                    elCutBased=0 if ismu else 4,
                    elMvaWP90=0 if ismu else 1, elMvaWP80=0 if ismu else 1,
                    elMvaBdt=0.0,
                ))
        else:
            #print("Muons:",chunk['nMuon'][iev],"Electrons:",chunk['nElectron'][iev],"!")
            # Muons
            nmu = int(chunk['nMuon'][iev])
            for i in range(nmu):
                def mu(b, d=0.0, _iev=iev, _i=i):
                    v = chunk[b]
                    return float(v[_iev][_i]) if v is not None else d
                def mub(b, _iev=iev, _i=i):
                    v = chunk[b]
                    return bool(v[_iev][_i]) if v is not None else False

                pt  = mu('Muon_pt')
                eta = mu('Muon_eta')
                if pt < cuts['minMuPt'] or abs(eta) > cuts['maxMuEta']:
                    continue
                dxy   = mu('Muon_dxy')
                dz    = mu('Muon_dz')
                sip3d = mu('Muon_sip3d')
                iso   = mu('Muon_pfRelIso03_all', 99.0)
                isPF  = mub('Muon_isPFcand')
                isGlo = mub('Muon_isGlobal')

                
                if abs(dxy) > cuts['maxDxy']:   continue
                if abs(dz)  > cuts['maxDz']:    continue
                if sip3d    > cuts['maxSip3d']: continue
                if iso      > cuts['maxRelIso']: continue
                if not isPF and not isGlo:      continue
                charge = int(mu('Muon_charge'))
                leps.append(dict(
                    pt=pt, eta=eta, phi=mu('Muon_phi'), mass=mu('Muon_mass', 0.10566),
                    charge=charge, pdgId=-13 * charge,
                    dxy=dxy, dz=dz,
                    dxyErr=mu('Muon_dxyErr'), dzErr=mu('Muon_dzErr'),
                    sip3d=sip3d, ip3d=mu('Muon_ip3d', -99.0),
                    pfRelIso03=iso, miniRelIso=mu('Muon_miniPFRelIso_all', -99.0),
                    muMedium=int(mub('Muon_mediumId')),
                    muTight=int(mub('Muon_tightId')),
                    muGlobal=int(isGlo), muPF=int(isPF),
                    elCutBased=0, elMvaWP90=0, elMvaWP80=0, elMvaBdt=-99.0,
                ))

            # Electrons
            nel = int(chunk['nElectron'][iev])
            for i in range(nel):
                def el(b, d=0.0, _iev=iev, _i=i):
                    if b in chunk.fields:
                        v = chunk[b]
                    else:
                        v = None
                    return float(v[_iev][_i]) if v is not None else d
                def elb(b, _iev=iev, _i=i):
                    if b in chunk.fields:
                        v = chunk[b]
                    else:
                        v = None
                    return bool(v[_iev][_i]) if v is not None else False
                def eli(b, d=0, _iev=iev, _i=i):
                    if b in chunk.fields:
                        v = chunk[b]
                    else:
                        v = None
                    return int(v[_iev][_i]) if v is not None else d

                pt  = el('Electron_pt')
                eta = el('Electron_eta')
                if pt < cuts['minElPt'] or abs(eta) > cuts['maxElEta']:
                    continue

                dxy      = el('Electron_dxy')
                dz       = el('Electron_dz')
                sip3d    = el('Electron_sip3d')
                iso      = el('Electron_pfRelIso03_all', 99.0)
                cutBased = eli('Electron_cutBased')

                if abs(dxy) > cuts['maxDxy']:   continue
                if abs(dz)  > cuts['maxDz']:    continue
                if sip3d    > cuts['maxSip3d']: continue
                if iso      > cuts['maxRelIso']: continue
                #if cutBased < 1:                continue  # at least veto

                charge = int(el('Electron_charge'))
                # MVA score: try Fall17V2 then generic mvaIso
                bdt = el('Electron_mvaFall17V2Iso', None)
                if bdt is None:
                    bdt = el('Electron_mvaIso', -99.0)

                leps.append(dict(
                    pt=pt, eta=eta, phi=el('Electron_phi'), mass=el('Electron_mass', 0.000511),
                    charge=charge, pdgId=-11 * charge,
                    dxy=dxy, dz=dz,
                    dxyErr=el('Electron_dxyErr'), dzErr=el('Electron_dzErr'),
                    sip3d=sip3d, ip3d=el('Electron_ip3d', -99.0),
                    pfRelIso03=iso, miniRelIso=el('Electron_miniPFRelIso_all', -99.0),
                    muMedium=0, muTight=0, muGlobal=0, muPF=0,
                    elCutBased=cutBased,
                    elMvaWP90=int(elb('Electron_mvaFall17V2Iso_WP90') or elb('Electron_mvaIso_WP90')),
                    elMvaWP80=int(elb('Electron_mvaFall17V2Iso_WP80') or elb('Electron_mvaIso_WP80')),
                    elMvaBdt=float(bdt),
                ))

        if len(leps) < 4:
            continue

        # Sort by pT descending before quadruplet search
        leps.sort(key=lambda l: l['pt'], reverse=True)

        result = find_best_quadruplet(leps, cuts)
        if result is None:
            continue

        # ---- Event-level quantities ----------------------------------------
        def ev(b, d=0.0):
            v = chunk[b]
            return float(v[iev]) if v is not None else d
        def evi(b, d=0):
            v = chunk[b]
            return int(v[iev]) if v is not None else d

        # Trigger bitmask
        trig = 0
        for bit, name in enumerate(HLT_PATHS):
            key = 'HLT_'+str(name)
            v = chunk[key]
            if v is not None and bool(v[iev]):
                trig |= (1 << bit)

        row = dict(
            run=int(chunk['run'][iev]),
            lumi=int(chunk['luminosityBlock'][iev]),
            event=int(chunk['event'][iev]),
            nPV=evi('PV_npvs') or evi('PV_npvsGood', 1),
            pvX=ev('PV_x'),   pvY=ev('PV_y'),   pvZ=ev('PV_z'),
            pvChi2=ev('PV_chi2'), pvNdof=ev('PV_ndof'), pvScore=ev('PV_score'),
            mZ1=result['mZ1'],   mZ2=result['mZ2'],
            m4l=result['m4l'],   pt4l=result['pt4l'],
            eta4l=result['eta4l'], phi4l=result['phi4l'], y4l=result['y4l'],
            finalState=result['finalState'],
            trigBits=trig,
        )

        # Per-lepton branches (l1..l4)
        for n, lep in enumerate(result['quad'], start=1):
            p = 'l'+str(n)
            row[p+'pt']       = lep['pt']
            row[p+'eta']      = lep['eta']
            row[p+'phi']      = lep['phi']
            row[p+'mass']     = lep['mass']
            row[p+'charge']   = lep['charge']
            row[p+'pdgId']    = lep['pdgId']
            row[p+'zId']      = result['zId'][n-1]
            row[p+'dxy']      = lep['dxy']
            row[p+'dz']       = lep['dz']
            row[p+'dxyErr']   = lep['dxyErr']
            row[p+'dzErr']    = lep['dzErr']
            row[p+'sip3d']    = lep['sip3d']
            row[p+'ip3d']     = lep['ip3d']
            row[p+'pfRelIso03']  = lep['pfRelIso03']
            row[p+'miniRelIso']  = lep['miniRelIso']
            row[p+'muMedium'] = lep['muMedium']
            row[p+'muTight']  = lep['muTight']
            row[p+'muGlobal'] = lep['muGlobal']
            row[p+'muPF']     = lep['muPF']
            row[p+'elCutBased'] = lep['elCutBased']
            row[p+'elMvaWP90']  = lep['elMvaWP90']
            row[p+'elMvaWP80']  = lep['elMvaWP80']
            row[p+'elMvaBdt']   = lep['elMvaBdt']

        rows.append(row)

    return rows

# ---------------------------------------------------------------------------
# Branch list to read from NanoAOD
# ---------------------------------------------------------------------------

def branches_to_read(tree_keys):
    """Return the subset of desired branches that actually exist in the file."""
    desired = [
        'run', 'luminosityBlock', 'event',
        'nMuon',
        'Muon_pt', 'Muon_eta', 'Muon_phi', 'Muon_mass', 'Muon_charge',
        'Muon_dxy', 'Muon_dz', 'Muon_dxyErr', 'Muon_dzErr',
        'Muon_sip3d', 'Muon_ip3d',
        'Muon_pfRelIso03_all', 'Muon_miniPFRelIso_all',
        'Muon_mediumId', 'Muon_tightId', 'Muon_isPFcand', 'Muon_isGlobal',
        'nElectron',
        'Electron_pt', 'Electron_eta', 'Electron_phi', 'Electron_mass', 'Electron_charge',
        'Electron_dxy', 'Electron_dz', 'Electron_dxyErr', 'Electron_dzErr',
        'Electron_sip3d', 'Electron_ip3d',
        'Electron_pfRelIso03_all', 'Electron_miniPFRelIso_all',
        'Electron_cutBased',
        'Electron_mvaFall17V2Iso_WP90', 'Electron_mvaFall17V2Iso_WP80', 'Electron_mvaFall17V2Iso',
        'Electron_mvaIso_WP90', 'Electron_mvaIso_WP80', 'Electron_mvaIso',
        'PV_x', 'PV_y', 'PV_z', 'PV_chi2', 'PV_ndof', 'PV_score',
        'PV_npvs', 'PV_npvsGood',
        # NANOGEN GenDressedLepton collections
        'nGenDressedLepton',
        'GenDressedLepton_pt', 'GenDressedLepton_eta', 'GenDressedLepton_phi',
        'GenDressedLepton_mass', 'GenDressedLepton_pdgId',
        'genWeight',
    ] + [f'HLT_{p}' for p in HLT_PATHS]

    # uproot 3 returns bytes keys; decode for comparison
    present = set(k.decode() if isinstance(k, bytes) else k for k in tree_keys)
    return [b for b in desired if b in present]

# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def rows_to_arrays(rows):
    """Convert list of row dicts to dict of numpy arrays."""
    if not rows:
        return {}
    keys = list(rows[0].keys())
    out = {}
    for k in keys:
        vals = [r[k] for r in rows]
        # Infer dtype
        sample = vals[0]
        if isinstance(sample, int):
            out[k] = np.array(vals, dtype=np.int32)
        elif isinstance(sample, float):
            out[k] = np.array(vals, dtype=np.float32)
        else:
            out[k] = np.array(vals)
    # uproot 3 doesn't support unsigned int writing; use signed equivalents
    for col in ('run', 'lumi', 'trigBits'):
        if col in out:
            out[col] = out[col].astype(np.int32)
    if 'event' in out:
        out['event'] = out['event'].astype(np.int64)
    return out


def write_root(arrays, path, total_events):
    branch_types = {k: v.dtype for k, v in arrays.items()}
    with uproot.recreate(str(path)) as f:
        tree = f.mktree("h4lTree", branch_types)
        tree.extend(arrays)

        f["Metadata"] = {
            "nEvents": np.array([total_events], dtype=np.int64)
        }
    print(f"Written {len(next(iter(arrays.values())))} events ->{path}  [ROOT TTree: h4lTree]")


def write_parquet(arrays, path, total_events):
    import pyarrow as pa
    import pyarrow.parquet as pq

    pa_cols = {}
    for k, v in arrays.items():
        if v.dtype == np.uint32:
            pa_cols[k] = pa.array(v, type=pa.uint32())
        elif v.dtype == np.uint64:
            pa_cols[k] = pa.array(v, type=pa.uint64())
        elif v.dtype == np.int32:
            pa_cols[k] = pa.array(v, type=pa.int32())
        elif v.dtype == np.float32:
            pa_cols[k] = pa.array(v, type=pa.float32())
        else:
            pa_cols[k] = pa.array(v)

    table = pa.table(pa_cols)
    table = table.replace_schema_metadata({
        b"n_input_events": str(total_events).encode()
    })

    pq.write_table(table, path, compression="snappy")
    print(f"Written {len(table)} events -> {path} [Parquet, snappy]")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--input',  nargs='+', required=True, metavar='FILE',
                   help='Input NanoAOD ROOT file(s)')
    p.add_argument('--output', required=True, metavar='FILE',
                   help='Output file (.root or .parquet)')
    p.add_argument('--tree',   default='Events',
                   help='TTree name inside the NanoAOD file (default: Events)')
    p.add_argument('--chunk',  type=int, default=50000,
                   help='Events per read chunk (default: 50000)')
    p.add_argument('--max-events', type=int, default=-1,
                   help='Stop after this many input events (-1 = all)')
    # Selection overrides
    p.add_argument('--min-mu-pt',  type=float, default=DEFAULTS['minMuPt'])
    p.add_argument('--min-el-pt',  type=float, default=DEFAULTS['minElPt'])
    p.add_argument('--max-reliso', type=float, default=DEFAULTS['maxRelIso'])
    p.add_argument('--min-m4l',    type=float, default=DEFAULTS['minM4l'])
    return p.parse_args()


def main():
    args = parse_args()

    cuts = dict(DEFAULTS)
    cuts['minMuPt']  = args.min_mu_pt
    cuts['minElPt']  = args.min_el_pt
    cuts['maxRelIso']= args.max_reliso
    cuts['minM4l']   = args.min_m4l

    output_path = Path(args.output)
    suffix = output_path.suffix.lower()
    if suffix not in ('.root', '.parquet'):
        sys.exit("ERROR: output file must end in .root or .parquet, got "+suffix)

    all_rows = []
    n_in = 0
    for fname in args.input:
        print("Reading "+fname+" ...")

        with uproot.open(fname) as f:
            if args.tree not in f:
                print("  WARNING: tree "+args.tree+" not found in "+fname+" skipping")
                continue
            tree = f[args.tree]
            branches = branches_to_read(tree.keys())
            
            for chunk in tree.iterate(branches, step_size=args.chunk):
                rows = read_chunk(chunk, cuts)
                all_rows.extend(rows)
                n_in += len(chunk['run'])

                if args.max_events > 0 and n_in >= args.max_events:
                    print("  Reached --max-events "+str(args.max_events)+", stopping.")
                    break

        if args.max_events > 0 and n_in >= args.max_events:
            break

    print("\nProcessed "+str(n_in)+" input events "+str(len(all_rows))+" passing the H selection")

    if not all_rows:
        print("No events passed selection. Output file not written.")
        return

    arrays = rows_to_arrays(all_rows)

    if suffix == '.root':
        write_root(arrays, output_path, n_in)
    else:
        write_parquet(arrays, output_path, n_in)


if __name__ == '__main__':
    main()
