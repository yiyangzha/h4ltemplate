from __future__ import annotations

import subprocess
from pathlib import Path

from phase1_utils import ROOT, append_experiment, append_session, ensure_dirs, setup_logging, write_json, OUT


def main() -> None:
    ensure_dirs()
    log = setup_logging()
    note_dir = ROOT / "analysis_note"
    note_dir.mkdir(parents=True, exist_ok=True)
    tex = note_dir / "test_build.tex"
    tex.write_text(
        "\\documentclass{article}\n"
        "\\usepackage{amsmath}\n"
        "\\begin{document}\n"
        "Phase 1 PDF toolchain test. The normalization check uses "
        "$w = \\sigma L / N_{\\mathrm{gen}}$ as a reproducibility equation.\n"
        "\\end{document}\n"
    )
    command = ["pixi", "run", "build-pdf", str(tex)]
    log.info("Running %s", " ".join(command))
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    passed = proc.returncode == 0 and (note_dir / "test_build.pdf").exists()
    for artifact in (tex, note_dir / "test_build.pdf", note_dir / "test_build.aux", note_dir / "test_build.log"):
        if artifact.exists():
            artifact.unlink()
    write_json(
        OUT / "pdf_build_test.json",
        {
            "command": " ".join(command),
            "returncode": proc.returncode,
            "passed": passed,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
            "stub_removed": not tex.exists(),
        },
    )
    append_session(
        "2026-05-29 PDF build test\n\n"
        f"- Ran `{' '.join(command)}`; passed={passed}; removed temporary stub."
    )
    append_experiment(
        "## 2026-05-29 — Phase 1 PDF toolchain test\n\n"
        f"- Ran `{' '.join(command)}`; passed={passed}; temporary stub removed."
    )
    if not passed:
        raise SystemExit("PDF build test failed; see outputs/pdf_build_test.json")


if __name__ == "__main__":
    main()

