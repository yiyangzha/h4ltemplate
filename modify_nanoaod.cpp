#include <TBranch.h>
#include <TClass.h>
#include <TDirectory.h>
#include <TError.h>
#include <TFile.h>
#include <TH1.h>
#include <TKey.h>
#include <TLeaf.h>
#include <TROOT.h>
#include <TTree.h>

#include <algorithm>
#include <atomic>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <cctype>
#include <exception>
#include <filesystem>
#include <fstream>
#include <future>
#include <glob.h>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <memory>
#include <mutex>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <utility>
#include <vector>

namespace fs = std::filesystem;

namespace {

constexpr double kPi = 3.141592653589793238462643383279502884;
std::mutex g_logMutex;

void logLine(const std::string& level, const std::string& message) {
  std::lock_guard<std::mutex> lock(g_logMutex);
  std::cerr << "[" << level << "] " << message << "\n";
}

[[noreturn]] void fail(const std::string& message) {
  throw std::runtime_error(message);
}

std::string quote(const std::string& s) {
  return "'" + s + "'";
}

std::string normalizeTypeName(std::string s) {
  s.erase(std::remove_if(s.begin(), s.end(), [](unsigned char c) { return std::isspace(c); }), s.end());
  const std::string stdPrefix = "std::";
  for (std::size_t pos = 0; (pos = s.find(stdPrefix, pos)) != std::string::npos;) {
    s.erase(pos, stdPrefix.size());
  }
  return s;
}

// -------------------------- Minimal JSON parser --------------------------

class Json {
 public:
  enum class Type { Null, Bool, Number, String, Array, Object };

  Type type = Type::Null;
  bool boolean = false;
  double number = 0.0;
  std::string str;
  std::vector<Json> array;
  std::map<std::string, Json> object;

  bool isNull() const { return type == Type::Null; }
  bool isBool() const { return type == Type::Bool; }
  bool isNumber() const { return type == Type::Number; }
  bool isString() const { return type == Type::String; }
  bool isArray() const { return type == Type::Array; }
  bool isObject() const { return type == Type::Object; }

  const Json* get(const std::string& key) const {
    if (!isObject()) return nullptr;
    auto it = object.find(key);
    return it == object.end() ? nullptr : &it->second;
  }

  std::string stringValue(const std::string& def = "") const {
    if (isString()) return str;
    return def;
  }

  bool boolValue(bool def = false) const {
    if (isBool()) return boolean;
    return def;
  }

  double doubleValue(double def = 0.0) const {
    if (isNumber()) return number;
    return def;
  }

  int intValue(int def = 0) const {
    if (isNumber()) return static_cast<int>(std::llround(number));
    return def;
  }

  std::uint64_t uint64Value(std::uint64_t def = 0) const {
    if (isNumber()) return static_cast<std::uint64_t>(std::llround(number));
    return def;
  }
};

class JsonParser {
 public:
  explicit JsonParser(std::string text) : text_(std::move(text)) {}

  Json parse() {
    skipWs();
    Json v = parseValue();
    skipWs();
    if (pos_ != text_.size()) fail("Unexpected trailing characters in JSON");
    return v;
  }

 private:
  std::string text_;
  std::size_t pos_ = 0;

  void skipWs() {
    while (pos_ < text_.size() && std::isspace(static_cast<unsigned char>(text_[pos_]))) ++pos_;
  }

  bool consume(char c) {
    skipWs();
    if (pos_ < text_.size() && text_[pos_] == c) {
      ++pos_;
      return true;
    }
    return false;
  }

  void expect(char c) {
    if (!consume(c)) {
      std::ostringstream os;
      os << "Expected '" << c << "' at JSON byte " << pos_;
      fail(os.str());
    }
  }

  Json parseValue() {
    skipWs();
    if (pos_ >= text_.size()) fail("Unexpected end of JSON");
    const char c = text_[pos_];
    if (c == '"') return parseString();
    if (c == '{') return parseObject();
    if (c == '[') return parseArray();
    if (c == 't' || c == 'f') return parseBool();
    if (c == 'n') return parseNull();
    if (c == '-' || std::isdigit(static_cast<unsigned char>(c))) return parseNumber();
    std::ostringstream os;
    os << "Unexpected JSON token at byte " << pos_;
    fail(os.str());
  }

  Json parseNull() {
    if (text_.compare(pos_, 4, "null") != 0) fail("Invalid JSON null");
    pos_ += 4;
    return Json{};
  }

  Json parseBool() {
    Json v;
    v.type = Json::Type::Bool;
    if (text_.compare(pos_, 4, "true") == 0) {
      v.boolean = true;
      pos_ += 4;
    } else if (text_.compare(pos_, 5, "false") == 0) {
      v.boolean = false;
      pos_ += 5;
    } else {
      fail("Invalid JSON boolean");
    }
    return v;
  }

  Json parseNumber() {
    const std::size_t start = pos_;
    if (text_[pos_] == '-') ++pos_;
    while (pos_ < text_.size() && std::isdigit(static_cast<unsigned char>(text_[pos_]))) ++pos_;
    if (pos_ < text_.size() && text_[pos_] == '.') {
      ++pos_;
      while (pos_ < text_.size() && std::isdigit(static_cast<unsigned char>(text_[pos_]))) ++pos_;
    }
    if (pos_ < text_.size() && (text_[pos_] == 'e' || text_[pos_] == 'E')) {
      ++pos_;
      if (pos_ < text_.size() && (text_[pos_] == '+' || text_[pos_] == '-')) ++pos_;
      while (pos_ < text_.size() && std::isdigit(static_cast<unsigned char>(text_[pos_]))) ++pos_;
    }
    Json v;
    v.type = Json::Type::Number;
    v.number = std::strtod(text_.c_str() + start, nullptr);
    return v;
  }

  Json parseString() {
    expect('"');
    Json v;
    v.type = Json::Type::String;
    while (pos_ < text_.size()) {
      char c = text_[pos_++];
      if (c == '"') return v;
      if (c != '\\') {
        v.str.push_back(c);
        continue;
      }
      if (pos_ >= text_.size()) fail("Invalid JSON string escape");
      const char e = text_[pos_++];
      switch (e) {
        case '"': v.str.push_back('"'); break;
        case '\\': v.str.push_back('\\'); break;
        case '/': v.str.push_back('/'); break;
        case 'b': v.str.push_back('\b'); break;
        case 'f': v.str.push_back('\f'); break;
        case 'n': v.str.push_back('\n'); break;
        case 'r': v.str.push_back('\r'); break;
        case 't': v.str.push_back('\t'); break;
        case 'u': {
          if (pos_ + 4 > text_.size()) fail("Invalid JSON unicode escape");
          // Config keys/values used here are ASCII. Preserve non-ASCII escapes as '?'.
          pos_ += 4;
          v.str.push_back('?');
          break;
        }
        default: fail("Invalid JSON string escape");
      }
    }
    fail("Unterminated JSON string");
  }

  Json parseArray() {
    expect('[');
    Json v;
    v.type = Json::Type::Array;
    skipWs();
    if (consume(']')) return v;
    while (true) {
      v.array.push_back(parseValue());
      skipWs();
      if (consume(']')) return v;
      expect(',');
    }
  }

  Json parseObject() {
    expect('{');
    Json v;
    v.type = Json::Type::Object;
    skipWs();
    if (consume('}')) return v;
    while (true) {
      skipWs();
      if (pos_ >= text_.size() || text_[pos_] != '"') fail("Expected JSON object key string");
      Json key = parseString();
      expect(':');
      v.object.emplace(key.str, parseValue());
      skipWs();
      if (consume('}')) return v;
      expect(',');
    }
  }
};

Json readJsonFile(const std::string& path) {
  std::ifstream in(path);
  if (!in) fail("Cannot open config file " + quote(path));
  std::ostringstream ss;
  ss << in.rdbuf();
  return JsonParser(ss.str()).parse();
}

std::vector<double> readDoubleArray(const Json* j, const std::vector<double>& def = {}) {
  if (!j || !j->isArray()) return def;
  std::vector<double> out;
  out.reserve(j->array.size());
  for (const Json& x : j->array) out.push_back(x.doubleValue());
  return out;
}

std::vector<std::vector<double>> readDouble2D(const Json* j) {
  std::vector<std::vector<double>> out;
  if (!j || !j->isArray()) return out;
  for (const Json& row : j->array) {
    if (row.isArray()) {
      std::vector<double> r;
      for (const Json& x : row.array) r.push_back(x.doubleValue(1.0));
      out.push_back(std::move(r));
    }
  }
  return out;
}

// ------------------------------- Config ----------------------------------

struct RegionScale {
  std::string name;
  double absEtaMin = 0.0;
  double absEtaMax = std::numeric_limits<double>::infinity();
  double constant = 0.0;
  double ptSlopeLog = 0.0;
  double chargeAsymmetry = 0.0;
};

struct RegionResolution {
  std::string name;
  double absEtaMin = 0.0;
  double absEtaMax = std::numeric_limits<double>::infinity();
  double sigma = 0.0;
  double ptSlopeLog = 0.0;
};

struct DistortionConfig {
  double globalFactor = 1.0;
  double ptSlopeLog = 0.0;
  double ptReference = 45.0;
  std::vector<double> etaFactors;
  std::vector<double> ptFactors;
  std::vector<std::vector<double>> binFactors;
};

enum class EffType { Bool, IntWP, FloatMax };

struct EffBranchConfig {
  std::string name;
  EffType type = EffType::Bool;
  int passThreshold = 1;
  int passValue = 1;
  int failValue = 0;
  double floatThreshold = 0.0;
  double passDoubleValue = 0.0;
  double failDoubleValue = 1.0;
  std::string referenceFlavor;
  DistortionConfig distortion;
};

struct LeptonBranches {
  std::string n;
  std::string pt;
  std::string eta;
  std::string phi;
  std::string mass;
  std::string charge;
  std::string energy;
};

struct EventIdBranches {
  std::string run = "run";
  std::string luminosityBlock = "luminosityBlock";
  std::string event = "event";
};

struct BinningConfig {
  std::vector<double> pt;
  std::vector<double> absEta;
  std::vector<double> energy;
};

struct Config {
  std::uint64_t seed = 314159;
  unsigned threads = 16;
  std::string treeName = "Events";
  std::vector<std::string> inputPaths;
  bool recursive = true;
  std::string outputDirectory = "modified";
  std::string outputSuffix = "_modified";
  bool copyMetadataTrees = true;
  bool overwrite = false;

  EventIdBranches eventId;
  LeptonBranches muonBranches{"nMuon", "Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge", ""};
  LeptonBranches electronBranches{"nElectron", "Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge", ""};

  bool scaleEnabled = true;
  double scalePtReference = 45.0;
  std::vector<RegionScale> muonScale;
  std::vector<RegionScale> electronScale;

  bool resolutionEnabled = true;
  std::vector<RegionResolution> muonResolution;
  std::vector<RegionResolution> electronResolution;

  bool efficiencyEnabled = true;
  BinningConfig binning;
  std::vector<EffBranchConfig> muonEffBranches;
  std::vector<EffBranchConfig> electronEffBranches;
  std::vector<EffBranchConfig> eventEffBranches;
};

const Json* child(const Json* j, const std::string& key) {
  return j ? j->get(key) : nullptr;
}

std::string getString(const Json* j, const std::string& key, const std::string& def) {
  const Json* v = child(j, key);
  return v ? v->stringValue(def) : def;
}

bool getBool(const Json* j, const std::string& key, bool def) {
  const Json* v = child(j, key);
  return v ? v->boolValue(def) : def;
}

int getInt(const Json* j, const std::string& key, int def) {
  const Json* v = child(j, key);
  return v ? v->intValue(def) : def;
}

double getDouble(const Json* j, const std::string& key, double def) {
  const Json* v = child(j, key);
  return v ? v->doubleValue(def) : def;
}

std::vector<RegionScale> parseScaleRegions(const Json* obj) {
  std::vector<RegionScale> out;
  if (!obj || !obj->isObject()) return out;
  for (const auto& kv : obj->object) {
    const Json* r = &kv.second;
    if (!r->isObject()) continue;
    RegionScale region;
    region.name = kv.first;
    region.absEtaMin = getDouble(r, "abs_eta_min", 0.0);
    region.absEtaMax = getDouble(r, "abs_eta_max", std::numeric_limits<double>::infinity());
    region.constant = getDouble(r, "constant", 0.0);
    region.ptSlopeLog = getDouble(r, "pt_slope_log", 0.0);
    region.chargeAsymmetry = getDouble(r, "charge_asymmetry", 0.0);
    out.push_back(region);
  }
  return out;
}

std::vector<RegionResolution> parseResolutionRegions(const Json* obj) {
  std::vector<RegionResolution> out;
  if (!obj || !obj->isObject()) return out;
  for (const auto& kv : obj->object) {
    const Json* r = &kv.second;
    if (!r->isObject()) continue;
    RegionResolution region;
    region.name = kv.first;
    region.absEtaMin = getDouble(r, "abs_eta_min", 0.0);
    region.absEtaMax = getDouble(r, "abs_eta_max", std::numeric_limits<double>::infinity());
    region.sigma = getDouble(r, "sigma", 0.0);
    region.ptSlopeLog = getDouble(r, "pt_slope_log", 0.0);
    out.push_back(region);
  }
  return out;
}

DistortionConfig parseDistortion(const Json* obj, double defaultPtRef) {
  DistortionConfig d;
  d.ptReference = defaultPtRef;
  if (!obj || !obj->isObject()) return d;
  d.globalFactor = getDouble(obj, "global_factor", 1.0);
  d.ptSlopeLog = getDouble(obj, "pt_slope_log", 0.0);
  d.ptReference = getDouble(obj, "pt_reference", defaultPtRef);
  d.etaFactors = readDoubleArray(child(obj, "eta_factors"));
  d.ptFactors = readDoubleArray(child(obj, "pt_factors"));
  d.binFactors = readDouble2D(child(obj, "bin_factors"));
  return d;
}

std::vector<EffBranchConfig> parseEffBranches(const Json* obj, double defaultPtRef) {
  std::vector<EffBranchConfig> out;
  if (!obj || !obj->isObject()) return out;
  for (const auto& kv : obj->object) {
    const Json* b = &kv.second;
    if (!b->isObject()) continue;
    EffBranchConfig cfg;
    cfg.name = kv.first;
    const std::string type = getString(b, "type", "bool");
    if (type == "bool") {
      cfg.type = EffType::Bool;
      cfg.passThreshold = 1;
      cfg.passValue = 1;
      cfg.failValue = 0;
    } else if (type == "int_wp") {
      cfg.type = EffType::IntWP;
      cfg.passThreshold = getInt(b, "pass_threshold", 1);
      cfg.passValue = getInt(b, "pass_value", cfg.passThreshold);
      cfg.failValue = getInt(b, "fail_value", 0);
    } else if (type == "float_max") {
      cfg.type = EffType::FloatMax;
      cfg.floatThreshold = getDouble(b, "max", getDouble(b, "pass_threshold", 0.15));
      cfg.passDoubleValue = getDouble(b, "pass_value", 0.5 * cfg.floatThreshold);
      cfg.failDoubleValue = getDouble(b, "fail_value", 2.0 * cfg.floatThreshold);
    } else {
      fail("Unsupported efficiency branch type " + quote(type) + " for branch " + quote(kv.first));
    }
    cfg.referenceFlavor = getString(b, "reference_flavor", "");
    cfg.distortion = parseDistortion(child(b, "distortion"), defaultPtRef);
    out.push_back(cfg);
  }
  return out;
}

LeptonBranches parseLeptonBranches(const Json* obj, LeptonBranches def) {
  if (!obj || !obj->isObject()) return def;
  def.n = getString(obj, "n", def.n);
  def.pt = getString(obj, "pt", def.pt);
  def.eta = getString(obj, "eta", def.eta);
  def.phi = getString(obj, "phi", def.phi);
  def.mass = getString(obj, "mass", def.mass);
  def.charge = getString(obj, "charge", def.charge);
  def.energy = getString(obj, "energy", def.energy);
  return def;
}

Config parseConfig(const std::string& path) {
  Json root = readJsonFile(path);
  if (!root.isObject()) fail("Top-level config must be a JSON object");
  Config cfg;

  const Json* global = root.get("global");
  cfg.seed = child(global, "seed") ? child(global, "seed")->uint64Value(cfg.seed) : cfg.seed;
  cfg.threads = static_cast<unsigned>(std::max(1, getInt(global, "threads", static_cast<int>(cfg.threads))));
  cfg.treeName = getString(global, "tree_name", cfg.treeName);

  const Json* input = root.get("input");
  const Json* pathValue = child(input, "path");
  const Json* pathsValue = child(input, "paths");
  if (pathValue && pathValue->isString()) {
    cfg.inputPaths.push_back(pathValue->str);
  }
  if (pathsValue && pathsValue->isArray()) {
    for (const Json& p : pathsValue->array) {
      if (p.isString()) cfg.inputPaths.push_back(p.str);
    }
  }
  cfg.recursive = getBool(input, "recursive", cfg.recursive);
  if (cfg.inputPaths.empty()) fail("Config must provide input.path or input.paths");

  const Json* output = root.get("output");
  cfg.outputDirectory = getString(output, "directory", cfg.outputDirectory);
  cfg.outputSuffix = getString(output, "suffix", cfg.outputSuffix);
  cfg.copyMetadataTrees = getBool(output, "copy_metadata_trees", cfg.copyMetadataTrees);
  cfg.overwrite = getBool(output, "overwrite", cfg.overwrite);

  const Json* branches = root.get("branches");
  const Json* eventId = child(branches, "event_id");
  cfg.eventId.run = getString(eventId, "run", cfg.eventId.run);
  cfg.eventId.luminosityBlock = getString(eventId, "luminosityBlock", cfg.eventId.luminosityBlock);
  cfg.eventId.event = getString(eventId, "event", cfg.eventId.event);
  cfg.muonBranches = parseLeptonBranches(child(branches, "muon"), cfg.muonBranches);
  cfg.electronBranches = parseLeptonBranches(child(branches, "electron"), cfg.electronBranches);

  const Json* scale = root.get("scale");
  cfg.scaleEnabled = getBool(scale, "enabled", cfg.scaleEnabled);
  cfg.scalePtReference = getDouble(scale, "pt_reference", cfg.scalePtReference);
  cfg.muonScale = parseScaleRegions(child(scale, "muon"));
  cfg.electronScale = parseScaleRegions(child(scale, "electron"));

  const Json* resolution = root.get("resolution");
  cfg.resolutionEnabled = getBool(resolution, "enabled", cfg.resolutionEnabled);
  cfg.muonResolution = parseResolutionRegions(child(resolution, "muon"));
  cfg.electronResolution = parseResolutionRegions(child(resolution, "electron"));

  const Json* eff = root.get("efficiency");
  cfg.efficiencyEnabled = getBool(eff, "enabled", cfg.efficiencyEnabled);
  const Json* binning = child(eff, "binning");
  cfg.binning.pt = readDoubleArray(child(binning, "pt"), {5, 10, 20, 30, 40, 50, 80, 120, 200});
  cfg.binning.absEta = readDoubleArray(child(binning, "abs_eta"), {0.0, 0.8, 1.2, 1.4442, 1.566, 2.0, 2.5});
  cfg.binning.energy = readDoubleArray(child(binning, "energy"));
  cfg.muonEffBranches = parseEffBranches(child(eff, "muon_branches"), cfg.scalePtReference);
  cfg.electronEffBranches = parseEffBranches(child(eff, "electron_branches"), cfg.scalePtReference);
  cfg.eventEffBranches = parseEffBranches(child(eff, "event_branches"), cfg.scalePtReference);

  auto validateEdges = [](const std::vector<double>& edges, const std::string& name) {
    if (edges.size() < 2) fail(name + " binning must contain at least two edges");
    for (std::size_t i = 1; i < edges.size(); ++i) {
      if (!(edges[i] > edges[i - 1])) fail(name + " binning edges must be strictly increasing");
    }
  };
  validateEdges(cfg.binning.pt, "pt");
  validateEdges(cfg.binning.absEta, "abs_eta");
  if (!cfg.binning.energy.empty()) validateEdges(cfg.binning.energy, "energy");
  return cfg;
}

// ------------------------------- Branch I/O -------------------------------

enum class ValueType {
  Bool,
  Char,
  UChar,
  Short,
  UShort,
  Int,
  UInt,
  Long64,
  ULong64,
  Float,
  Double,
  Unknown
};

ValueType leafTypeFromName(const std::string& typeName) {
  const std::string t = normalizeTypeName(typeName);
  if (t == "Bool_t" || t == "bool") return ValueType::Bool;
  if (t == "Char_t" || t == "char") return ValueType::Char;
  if (t == "UChar_t" || t == "unsignedchar") return ValueType::UChar;
  if (t == "Short_t" || t == "short") return ValueType::Short;
  if (t == "UShort_t" || t == "unsignedshort") return ValueType::UShort;
  if (t == "Int_t" || t == "int") return ValueType::Int;
  if (t == "UInt_t" || t == "unsignedint") return ValueType::UInt;
  if (t == "Long64_t" || t == "longlong" || t == "Long_t") return ValueType::Long64;
  if (t == "ULong64_t" || t == "unsignedlonglong" || t == "ULong_t") return ValueType::ULong64;
  if (t == "Float_t" || t == "float") return ValueType::Float;
  if (t == "Double_t" || t == "double") return ValueType::Double;
  return ValueType::Unknown;
}

ValueType vectorTypeFromClassName(const std::string& className) {
  const std::string t = normalizeTypeName(className);
  if (t.find("vector<bool") != std::string::npos || t.find("vector<Bool_t") != std::string::npos) return ValueType::Bool;
  if (t.find("vector<char") != std::string::npos || t.find("vector<Char_t") != std::string::npos) return ValueType::Char;
  if (t.find("vector<unsignedchar") != std::string::npos || t.find("vector<UChar_t") != std::string::npos) return ValueType::UChar;
  if (t.find("vector<short") != std::string::npos || t.find("vector<Short_t") != std::string::npos) return ValueType::Short;
  if (t.find("vector<unsignedshort") != std::string::npos || t.find("vector<UShort_t") != std::string::npos) return ValueType::UShort;
  if (t.find("vector<int") != std::string::npos || t.find("vector<Int_t") != std::string::npos) return ValueType::Int;
  if (t.find("vector<unsignedint") != std::string::npos || t.find("vector<UInt_t") != std::string::npos) return ValueType::UInt;
  if (t.find("vector<longlong") != std::string::npos || t.find("vector<Long64_t") != std::string::npos) return ValueType::Long64;
  if (t.find("vector<unsignedlonglong") != std::string::npos || t.find("vector<ULong64_t") != std::string::npos) return ValueType::ULong64;
  if (t.find("vector<float") != std::string::npos || t.find("vector<Float_t") != std::string::npos) return ValueType::Float;
  if (t.find("vector<double") != std::string::npos || t.find("vector<Double_t") != std::string::npos) return ValueType::Double;
  return ValueType::Unknown;
}

std::string valueTypeName(ValueType t) {
  switch (t) {
    case ValueType::Bool: return "Bool_t";
    case ValueType::Char: return "Char_t";
    case ValueType::UChar: return "UChar_t";
    case ValueType::Short: return "Short_t";
    case ValueType::UShort: return "UShort_t";
    case ValueType::Int: return "Int_t";
    case ValueType::UInt: return "UInt_t";
    case ValueType::Long64: return "Long64_t";
    case ValueType::ULong64: return "ULong64_t";
    case ValueType::Float: return "Float_t";
    case ValueType::Double: return "Double_t";
    case ValueType::Unknown: return "Unknown";
  }
  return "Unknown";
}

bool isFloatingType(ValueType t) {
  return t == ValueType::Float || t == ValueType::Double;
}

class VectorHolderBase {
 public:
  virtual ~VectorHolderBase() = default;
  virtual void* addressOfPointer() = 0;
  virtual std::size_t size() const = 0;
  virtual double getDouble(std::size_t i) const = 0;
  virtual std::int64_t getInt64(std::size_t i) const = 0;
  virtual std::uint64_t getUInt64(std::size_t i) const = 0;
  virtual bool getBool(std::size_t i) const = 0;
  virtual void setDouble(std::size_t i, double v) = 0;
  virtual void setInt(std::size_t i, int v) = 0;
};

template <typename T>
class VectorHolder final : public VectorHolderBase {
 public:
  std::vector<T>* ptr = nullptr;

  void* addressOfPointer() override { return &ptr; }
  std::size_t size() const override { return ptr ? ptr->size() : 0; }
  double getDouble(std::size_t i) const override { return static_cast<double>((*ptr)[i]); }
  std::int64_t getInt64(std::size_t i) const override { return static_cast<std::int64_t>((*ptr)[i]); }
  std::uint64_t getUInt64(std::size_t i) const override { return static_cast<std::uint64_t>((*ptr)[i]); }
  bool getBool(std::size_t i) const override { return static_cast<bool>((*ptr)[i]); }
  void setDouble(std::size_t i, double v) override { (*ptr)[i] = static_cast<T>(v); }
  void setInt(std::size_t i, int v) override { (*ptr)[i] = static_cast<T>(v); }
};

class VectorBoolHolder final : public VectorHolderBase {
 public:
  std::vector<bool>* ptr = nullptr;

  void* addressOfPointer() override { return &ptr; }
  std::size_t size() const override { return ptr ? ptr->size() : 0; }
  double getDouble(std::size_t i) const override { return (*ptr)[i] ? 1.0 : 0.0; }
  std::int64_t getInt64(std::size_t i) const override { return (*ptr)[i] ? 1 : 0; }
  std::uint64_t getUInt64(std::size_t i) const override { return (*ptr)[i] ? 1 : 0; }
  bool getBool(std::size_t i) const override { return (*ptr)[i]; }
  void setDouble(std::size_t i, double v) override { (*ptr)[i] = (v != 0.0); }
  void setInt(std::size_t i, int v) override { (*ptr)[i] = (v != 0); }
};

std::unique_ptr<VectorHolderBase> makeVectorHolder(ValueType type) {
  switch (type) {
    case ValueType::Bool: return std::make_unique<VectorBoolHolder>();
    case ValueType::Char: return std::make_unique<VectorHolder<Char_t>>();
    case ValueType::UChar: return std::make_unique<VectorHolder<UChar_t>>();
    case ValueType::Short: return std::make_unique<VectorHolder<Short_t>>();
    case ValueType::UShort: return std::make_unique<VectorHolder<UShort_t>>();
    case ValueType::Int: return std::make_unique<VectorHolder<Int_t>>();
    case ValueType::UInt: return std::make_unique<VectorHolder<UInt_t>>();
    case ValueType::Long64: return std::make_unique<VectorHolder<Long64_t>>();
    case ValueType::ULong64: return std::make_unique<VectorHolder<ULong64_t>>();
    case ValueType::Float: return std::make_unique<VectorHolder<Float_t>>();
    case ValueType::Double: return std::make_unique<VectorHolder<Double_t>>();
    case ValueType::Unknown: break;
  }
  return nullptr;
}

class BranchBuffer {
 public:
  bool bind(TTree* tree, const std::string& branchName, std::size_t capacity, bool warnIfMissing, const std::string& context) {
    name_ = branchName;
    TBranch* branch = tree ? tree->GetBranch(branchName.c_str()) : nullptr;
    if (!branch) {
      if (warnIfMissing) logLine("WARN", context + ": missing branch " + quote(branchName));
      return false;
    }

    const std::string className = branch->GetClassName() ? branch->GetClassName() : "";
    if (!className.empty()) {
      type_ = vectorTypeFromClassName(className);
      if (type_ == ValueType::Unknown) {
        logLine("WARN", context + ": unsupported vector branch type " + quote(className) + " for " + quote(branchName));
        return false;
      }
      isVector_ = true;
      vectorHolder_ = makeVectorHolder(type_);
      if (!vectorHolder_) return false;
      tree->SetBranchStatus(branchName.c_str(), 1);
      if (tree->SetBranchAddress(branchName.c_str(), vectorHolder_->addressOfPointer()) < 0) {
        logLine("WARN", context + ": SetBranchAddress failed for vector branch " + quote(branchName));
        return false;
      }
      bound_ = true;
      return true;
    }

    TObjArray* leaves = branch->GetListOfLeaves();
    if (!leaves || leaves->GetEntries() != 1) {
      logLine("WARN", context + ": unsupported non-leaf-list branch " + quote(branchName));
      return false;
    }
    TLeaf* leaf = static_cast<TLeaf*>(leaves->At(0));
    type_ = leafTypeFromName(leaf ? leaf->GetTypeName() : "");
    if (type_ == ValueType::Unknown) {
      logLine("WARN", context + ": unsupported leaf type " + quote(leaf ? leaf->GetTypeName() : "") + " for " + quote(branchName));
      return false;
    }
    isVector_ = false;
    capacity_ = std::max<std::size_t>(capacity, 1);
    allocateArray(capacity_);
    tree->SetBranchStatus(branchName.c_str(), 1);
    if (tree->SetBranchAddress(branchName.c_str(), arrayAddress()) < 0) {
      logLine("WARN", context + ": SetBranchAddress failed for leaf branch " + quote(branchName));
      return false;
    }
    bound_ = true;
    return true;
  }

  bool bound() const { return bound_; }
  bool isVector() const { return isVector_; }
  ValueType valueType() const { return type_; }
  std::size_t capacity() const { return isVector_ ? size() : capacity_; }

  std::size_t size() const {
    if (!bound_) return 0;
    return isVector_ ? vectorHolder_->size() : capacity_;
  }

  std::size_t availableForN(std::size_t n) const {
    if (!bound_) return 0;
    return isVector_ ? vectorHolder_->size() : std::min(n, capacity_);
  }

  double getDouble(std::size_t i) const {
    if (isVector_) return vectorHolder_->getDouble(i);
    switch (type_) {
      case ValueType::Bool: return arrBool_[i] ? 1.0 : 0.0;
      case ValueType::Char: return arrChar_[i];
      case ValueType::UChar: return arrUChar_[i];
      case ValueType::Short: return arrShort_[i];
      case ValueType::UShort: return arrUShort_[i];
      case ValueType::Int: return arrInt_[i];
      case ValueType::UInt: return arrUInt_[i];
      case ValueType::Long64: return static_cast<double>(arrLong64_[i]);
      case ValueType::ULong64: return static_cast<double>(arrULong64_[i]);
      case ValueType::Float: return arrFloat_[i];
      case ValueType::Double: return arrDouble_[i];
      case ValueType::Unknown: break;
    }
    return 0.0;
  }

  std::int64_t getInt64(std::size_t i) const {
    if (isVector_) return vectorHolder_->getInt64(i);
    switch (type_) {
      case ValueType::Bool: return arrBool_[i] ? 1 : 0;
      case ValueType::Char: return arrChar_[i];
      case ValueType::UChar: return arrUChar_[i];
      case ValueType::Short: return arrShort_[i];
      case ValueType::UShort: return arrUShort_[i];
      case ValueType::Int: return arrInt_[i];
      case ValueType::UInt: return arrUInt_[i];
      case ValueType::Long64: return arrLong64_[i];
      case ValueType::ULong64: return static_cast<std::int64_t>(arrULong64_[i]);
      case ValueType::Float: return static_cast<std::int64_t>(arrFloat_[i]);
      case ValueType::Double: return static_cast<std::int64_t>(arrDouble_[i]);
      case ValueType::Unknown: break;
    }
    return 0;
  }

  std::uint64_t getUInt64(std::size_t i) const {
    if (isVector_) return vectorHolder_->getUInt64(i);
    switch (type_) {
      case ValueType::Bool: return arrBool_[i] ? 1 : 0;
      case ValueType::Char: return static_cast<std::uint64_t>(arrChar_[i]);
      case ValueType::UChar: return arrUChar_[i];
      case ValueType::Short: return static_cast<std::uint64_t>(arrShort_[i]);
      case ValueType::UShort: return arrUShort_[i];
      case ValueType::Int: return static_cast<std::uint64_t>(arrInt_[i]);
      case ValueType::UInt: return arrUInt_[i];
      case ValueType::Long64: return static_cast<std::uint64_t>(arrLong64_[i]);
      case ValueType::ULong64: return arrULong64_[i];
      case ValueType::Float: return static_cast<std::uint64_t>(arrFloat_[i]);
      case ValueType::Double: return static_cast<std::uint64_t>(arrDouble_[i]);
      case ValueType::Unknown: break;
    }
    return 0;
  }

  bool getBool(std::size_t i) const {
    if (isVector_) return vectorHolder_->getBool(i);
    switch (type_) {
      case ValueType::Bool: return arrBool_[i];
      case ValueType::Char: return arrChar_[i] != 0;
      case ValueType::UChar: return arrUChar_[i] != 0;
      case ValueType::Short: return arrShort_[i] != 0;
      case ValueType::UShort: return arrUShort_[i] != 0;
      case ValueType::Int: return arrInt_[i] != 0;
      case ValueType::UInt: return arrUInt_[i] != 0;
      case ValueType::Long64: return arrLong64_[i] != 0;
      case ValueType::ULong64: return arrULong64_[i] != 0;
      case ValueType::Float: return arrFloat_[i] != 0.0f;
      case ValueType::Double: return arrDouble_[i] != 0.0;
      case ValueType::Unknown: break;
    }
    return false;
  }

  void setDouble(std::size_t i, double v) {
    if (isVector_) {
      vectorHolder_->setDouble(i, v);
      return;
    }
    switch (type_) {
      case ValueType::Bool: arrBool_[i] = (v != 0.0); break;
      case ValueType::Char: arrChar_[i] = static_cast<Char_t>(std::llround(v)); break;
      case ValueType::UChar: arrUChar_[i] = static_cast<UChar_t>(std::llround(v)); break;
      case ValueType::Short: arrShort_[i] = static_cast<Short_t>(std::llround(v)); break;
      case ValueType::UShort: arrUShort_[i] = static_cast<UShort_t>(std::llround(v)); break;
      case ValueType::Int: arrInt_[i] = static_cast<Int_t>(std::llround(v)); break;
      case ValueType::UInt: arrUInt_[i] = static_cast<UInt_t>(std::llround(v)); break;
      case ValueType::Long64: arrLong64_[i] = static_cast<Long64_t>(std::llround(v)); break;
      case ValueType::ULong64: arrULong64_[i] = static_cast<ULong64_t>(std::llround(v)); break;
      case ValueType::Float: arrFloat_[i] = static_cast<Float_t>(v); break;
      case ValueType::Double: arrDouble_[i] = static_cast<Double_t>(v); break;
      case ValueType::Unknown: break;
    }
  }

  void setInt(std::size_t i, int v) {
    if (isVector_) {
      vectorHolder_->setInt(i, v);
      return;
    }
    switch (type_) {
      case ValueType::Bool: arrBool_[i] = (v != 0); break;
      case ValueType::Char: arrChar_[i] = static_cast<Char_t>(v); break;
      case ValueType::UChar: arrUChar_[i] = static_cast<UChar_t>(v); break;
      case ValueType::Short: arrShort_[i] = static_cast<Short_t>(v); break;
      case ValueType::UShort: arrUShort_[i] = static_cast<UShort_t>(v); break;
      case ValueType::Int: arrInt_[i] = static_cast<Int_t>(v); break;
      case ValueType::UInt: arrUInt_[i] = static_cast<UInt_t>(v); break;
      case ValueType::Long64: arrLong64_[i] = static_cast<Long64_t>(v); break;
      case ValueType::ULong64: arrULong64_[i] = static_cast<ULong64_t>(v); break;
      case ValueType::Float: arrFloat_[i] = static_cast<Float_t>(v); break;
      case ValueType::Double: arrDouble_[i] = static_cast<Double_t>(v); break;
      case ValueType::Unknown: break;
    }
  }

 private:
  std::string name_;
  bool bound_ = false;
  bool isVector_ = false;
  ValueType type_ = ValueType::Unknown;
  std::size_t capacity_ = 0;
  std::unique_ptr<VectorHolderBase> vectorHolder_;

  std::unique_ptr<Bool_t[]> arrBool_;
  std::unique_ptr<Char_t[]> arrChar_;
  std::unique_ptr<UChar_t[]> arrUChar_;
  std::unique_ptr<Short_t[]> arrShort_;
  std::unique_ptr<UShort_t[]> arrUShort_;
  std::unique_ptr<Int_t[]> arrInt_;
  std::unique_ptr<UInt_t[]> arrUInt_;
  std::unique_ptr<Long64_t[]> arrLong64_;
  std::unique_ptr<ULong64_t[]> arrULong64_;
  std::unique_ptr<Float_t[]> arrFloat_;
  std::unique_ptr<Double_t[]> arrDouble_;

  void allocateArray(std::size_t n) {
    switch (type_) {
      case ValueType::Bool: arrBool_.reset(new Bool_t[n]()); break;
      case ValueType::Char: arrChar_.reset(new Char_t[n]()); break;
      case ValueType::UChar: arrUChar_.reset(new UChar_t[n]()); break;
      case ValueType::Short: arrShort_.reset(new Short_t[n]()); break;
      case ValueType::UShort: arrUShort_.reset(new UShort_t[n]()); break;
      case ValueType::Int: arrInt_.reset(new Int_t[n]()); break;
      case ValueType::UInt: arrUInt_.reset(new UInt_t[n]()); break;
      case ValueType::Long64: arrLong64_.reset(new Long64_t[n]()); break;
      case ValueType::ULong64: arrULong64_.reset(new ULong64_t[n]()); break;
      case ValueType::Float: arrFloat_.reset(new Float_t[n]()); break;
      case ValueType::Double: arrDouble_.reset(new Double_t[n]()); break;
      case ValueType::Unknown: break;
    }
  }

  void* arrayAddress() {
    switch (type_) {
      case ValueType::Bool: return arrBool_.get();
      case ValueType::Char: return arrChar_.get();
      case ValueType::UChar: return arrUChar_.get();
      case ValueType::Short: return arrShort_.get();
      case ValueType::UShort: return arrUShort_.get();
      case ValueType::Int: return arrInt_.get();
      case ValueType::UInt: return arrUInt_.get();
      case ValueType::Long64: return arrLong64_.get();
      case ValueType::ULong64: return arrULong64_.get();
      case ValueType::Float: return arrFloat_.get();
      case ValueType::Double: return arrDouble_.get();
      case ValueType::Unknown: break;
    }
    return nullptr;
  }
};

// --------------------------- Efficiency maps ------------------------------

int findBinClamped(const std::vector<double>& edges, double x) {
  if (edges.size() < 2) return 0;
  if (x < edges.front()) return 0;
  if (x >= edges.back()) return static_cast<int>(edges.size() - 2);
  auto it = std::upper_bound(edges.begin(), edges.end(), x);
  int bin = static_cast<int>(std::distance(edges.begin(), it)) - 1;
  return std::max(0, std::min(bin, static_cast<int>(edges.size() - 2)));
}

struct BinIndex {
  int pt = 0;
  int eta = 0;
  int energy = 0;
  int flat = 0;
};

BinIndex makeBinIndex(const BinningConfig& b, double pt, double eta, double energy = std::numeric_limits<double>::quiet_NaN()) {
  BinIndex idx;
  idx.pt = findBinClamped(b.pt, pt);
  idx.eta = findBinClamped(b.absEta, std::abs(eta));
  const int nPt = static_cast<int>(b.pt.size() - 1);
  const int nEta = static_cast<int>(b.absEta.size() - 1);
  if (!b.energy.empty()) {
    const double binEnergy = std::isfinite(energy) ? energy : std::max(0.0, pt) * std::cosh(eta);
    idx.energy = findBinClamped(b.energy, binEnergy);
    const int nEnergy = static_cast<int>(b.energy.size() - 1);
    idx.flat = (idx.energy * nEta + idx.eta) * nPt + idx.pt;
    (void)nEnergy;
  } else {
    idx.flat = idx.eta * nPt + idx.pt;
  }
  return idx;
}

int nFlatBins(const BinningConfig& b) {
  const int nPt = static_cast<int>(b.pt.size() - 1);
  const int nEta = static_cast<int>(b.absEta.size() - 1);
  const int nEnergy = b.energy.empty() ? 1 : static_cast<int>(b.energy.size() - 1);
  return nPt * nEta * nEnergy;
}

struct EffCounts {
  std::vector<std::uint64_t> pass;
  std::vector<std::uint64_t> total;
  std::uint64_t globalPass = 0;
  std::uint64_t globalTotal = 0;

  explicit EffCounts(int bins = 0) : pass(bins, 0), total(bins, 0) {}

  void add(int bin, bool passed) {
    if (bin < 0 || bin >= static_cast<int>(total.size())) return;
    ++total[bin];
    ++globalTotal;
    if (passed) {
      ++pass[bin];
      ++globalPass;
    }
  }

  void merge(const EffCounts& other) {
    if (pass.size() < other.pass.size()) {
      pass.resize(other.pass.size(), 0);
      total.resize(other.total.size(), 0);
    }
    for (std::size_t i = 0; i < other.pass.size(); ++i) {
      pass[i] += other.pass[i];
      total[i] += other.total[i];
    }
    globalPass += other.globalPass;
    globalTotal += other.globalTotal;
  }

  double efficiency(int bin) const {
    if (bin >= 0 && bin < static_cast<int>(total.size()) && total[bin] > 0) {
      return static_cast<double>(pass[bin]) / static_cast<double>(total[bin]);
    }
    if (globalTotal > 0) return static_cast<double>(globalPass) / static_cast<double>(globalTotal);
    return 0.0;
  }
};

struct Calibration {
  std::map<std::string, EffCounts> muon;
  std::map<std::string, EffCounts> electron;
  std::map<std::string, EffCounts> event;
};

Calibration makeEmptyCalibration(const Config& cfg) {
  Calibration c;
  const int bins = nFlatBins(cfg.binning);
  for (const auto& b : cfg.muonEffBranches) c.muon.emplace(b.name, EffCounts(bins));
  for (const auto& b : cfg.electronEffBranches) c.electron.emplace(b.name, EffCounts(bins));
  for (const auto& b : cfg.eventEffBranches) c.event.emplace(b.name, EffCounts(bins));
  return c;
}

void mergeCalibration(Calibration& into, const Calibration& from) {
  for (const auto& kv : from.muon) into.muon[kv.first].merge(kv.second);
  for (const auto& kv : from.electron) into.electron[kv.first].merge(kv.second);
  for (const auto& kv : from.event) into.event[kv.first].merge(kv.second);
}

bool originalPasses(const EffBranchConfig& cfg, const BranchBuffer& branch, std::size_t i) {
  if (cfg.type == EffType::Bool) return branch.getBool(i);
  if (cfg.type == EffType::FloatMax) return branch.getDouble(i) <= cfg.floatThreshold;
  return branch.getInt64(i) >= cfg.passThreshold;
}

double distortedEfficiency(double base, const EffBranchConfig& cfg, const BinIndex& idx, double pt) {
  double p = base * cfg.distortion.globalFactor;
  if (idx.eta >= 0 && idx.eta < static_cast<int>(cfg.distortion.etaFactors.size())) {
    p *= cfg.distortion.etaFactors[idx.eta];
  }
  if (idx.pt >= 0 && idx.pt < static_cast<int>(cfg.distortion.ptFactors.size())) {
    p *= cfg.distortion.ptFactors[idx.pt];
  }
  if (idx.eta >= 0 && idx.eta < static_cast<int>(cfg.distortion.binFactors.size())) {
    const auto& row = cfg.distortion.binFactors[idx.eta];
    if (idx.pt >= 0 && idx.pt < static_cast<int>(row.size())) p *= row[idx.pt];
  }
  const double ptRef = std::max(cfg.distortion.ptReference, 1.0e-9);
  p *= 1.0 + cfg.distortion.ptSlopeLog * std::log(std::max(pt, 1.0e-9) / ptRef);
  if (!std::isfinite(p)) p = 0.0;
  return std::clamp(p, 0.0, 1.0);
}

// ------------------------------ RNG ---------------------------------------

std::uint64_t fnv1a64(const std::string& s) {
  std::uint64_t h = 1469598103934665603ULL;
  for (unsigned char c : s) {
    h ^= c;
    h *= 1099511628211ULL;
  }
  return h;
}

void hashCombine(std::uint64_t& seed, std::uint64_t v) {
  seed ^= v + 0x9e3779b97f4a7c15ULL + (seed << 6) + (seed >> 2);
}

std::uint64_t splitmix64(std::uint64_t x) {
  x += 0x9e3779b97f4a7c15ULL;
  x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
  x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
  return x ^ (x >> 31);
}

double uniform01(std::uint64_t key) {
  const std::uint64_t x = splitmix64(key);
  return static_cast<double>(x >> 11) * (1.0 / 9007199254740992.0);
}

double normal01(std::uint64_t key) {
  double u1 = uniform01(key);
  const double u2 = uniform01(key ^ 0xd1b54a32d192ed03ULL);
  u1 = std::max(u1, std::numeric_limits<double>::min());
  return std::sqrt(-2.0 * std::log(u1)) * std::cos(2.0 * kPi * u2);
}

std::uint64_t objectKey(const Config& cfg,
                        std::uint64_t run,
                        std::uint64_t lumi,
                        std::uint64_t event,
                        Long64_t entry,
                        std::size_t index,
                        int flavor,
                        const std::string& stream) {
  std::uint64_t key = cfg.seed;
  hashCombine(key, run);
  hashCombine(key, lumi);
  hashCombine(key, event);
  if (run == 0 && lumi == 0 && event == 0) hashCombine(key, static_cast<std::uint64_t>(entry));
  hashCombine(key, static_cast<std::uint64_t>(index));
  hashCombine(key, static_cast<std::uint64_t>(flavor));
  hashCombine(key, fnv1a64(stream));
  return key;
}

// ----------------------------- Physics model ------------------------------

double scaleShift(const std::vector<RegionScale>& regions, double eta, double pt, int charge, double ptRef) {
  const double aeta = std::abs(eta);
  for (const RegionScale& r : regions) {
    if (aeta >= r.absEtaMin && aeta < r.absEtaMax) {
      const double logTerm = std::log(std::max(pt, 1.0e-9) / std::max(ptRef, 1.0e-9));
      return r.constant + r.ptSlopeLog * logTerm + r.chargeAsymmetry * static_cast<double>(charge);
    }
  }
  return 0.0;
}

double resolutionSigma(const std::vector<RegionResolution>& regions, double eta, double pt, double ptRef) {
  const double aeta = std::abs(eta);
  for (const RegionResolution& r : regions) {
    if (aeta >= r.absEtaMin && aeta < r.absEtaMax) {
      const double logTerm = std::log(std::max(pt, 1.0e-9) / std::max(ptRef, 1.0e-9));
      const double sigma = r.sigma + r.ptSlopeLog * logTerm;
      return std::max(0.0, sigma);
    }
  }
  return 0.0;
}

// ----------------------------- File handling ------------------------------

bool containsGlobMeta(const std::string& path) {
  return path.find_first_of("*?[") != std::string::npos;
}

bool hasRootExtension(const fs::path& p) {
  return p.extension() == ".root";
}

std::vector<std::string> expandInputPaths(const Config& cfg) {
  std::set<std::string> files;
  for (const std::string& raw : cfg.inputPaths) {
    if (containsGlobMeta(raw)) {
      glob_t globResult;
      std::memset(&globResult, 0, sizeof(globResult));
      const int rc = glob(raw.c_str(), 0, nullptr, &globResult);
      if (rc == 0) {
        for (std::size_t i = 0; i < globResult.gl_pathc; ++i) {
          fs::path p(globResult.gl_pathv[i]);
          if (fs::is_regular_file(p) && hasRootExtension(p)) files.insert(fs::absolute(p).string());
        }
      } else {
        logLine("WARN", "Input glob matched no files: " + quote(raw));
      }
      globfree(&globResult);
      continue;
    }

    fs::path p(raw);
    if (fs::is_regular_file(p)) {
      if (hasRootExtension(p)) files.insert(fs::absolute(p).string());
    } else if (fs::is_directory(p)) {
      if (cfg.recursive) {
        for (const auto& entry : fs::recursive_directory_iterator(p)) {
          if (entry.is_regular_file() && hasRootExtension(entry.path())) files.insert(fs::absolute(entry.path()).string());
        }
      } else {
        for (const auto& entry : fs::directory_iterator(p)) {
          if (entry.is_regular_file() && hasRootExtension(entry.path())) files.insert(fs::absolute(entry.path()).string());
        }
      }
    } else {
      logLine("WARN", "Input path does not exist or is not readable: " + quote(raw));
    }
  }
  return {files.begin(), files.end()};
}

std::string shortHashHex(const std::string& s) {
  std::ostringstream os;
  os << std::hex << std::setw(8) << std::setfill('0') << (fnv1a64(s) & 0xffffffffULL);
  return os.str();
}

std::vector<std::string> makeOutputPaths(const Config& cfg, const std::vector<std::string>& inputs) {
  std::vector<std::string> outputs;
  std::set<std::string> used;
  for (const std::string& input : inputs) {
    fs::path inPath(input);
    fs::path outDir(cfg.outputDirectory);
    std::string ext = inPath.extension().empty() ? ".root" : inPath.extension().string();
    fs::path out = outDir / (inPath.stem().string() + cfg.outputSuffix + ext);
    if (used.count(fs::absolute(out).string())) {
      out = outDir / (inPath.stem().string() + "_" + shortHashHex(input) + cfg.outputSuffix + ext);
    }
    used.insert(fs::absolute(out).string());
    outputs.push_back(out.string());
  }
  return outputs;
}

// ----------------------------- Pre-scan -----------------------------------

struct PreScanResult {
  std::string input;
  std::size_t maxMuon = 0;
  std::size_t maxElectron = 0;
  Calibration calibration;
};

std::size_t readMaxCount(TTree* tree, const std::string& branchName, const std::string& context) {
  if (branchName.empty()) return 0;
  tree->ResetBranchAddresses();
  tree->SetBranchStatus("*", 0);
  BranchBuffer n;
  if (!n.bind(tree, branchName, 1, true, context)) return 0;
  std::size_t maxN = 0;
  const Long64_t entries = tree->GetEntries();
  for (Long64_t i = 0; i < entries; ++i) {
    tree->GetEntry(i);
    maxN = std::max<std::size_t>(maxN, static_cast<std::size_t>(n.getUInt64(0)));
  }
  return maxN;
}

struct EffBranchRuntime {
  EffBranchConfig cfg;
  BranchBuffer branch;
  EffCounts* counts = nullptr;
};

void writeEfficiencyValue(EffBranchRuntime& branch, std::size_t index, bool pass) {
  if (branch.cfg.type == EffType::Bool) {
    branch.branch.setInt(index, pass ? 1 : 0);
  } else if (branch.cfg.type == EffType::IntWP) {
    branch.branch.setInt(index, pass ? branch.cfg.passValue : branch.cfg.failValue);
  } else if (branch.cfg.type == EffType::FloatMax) {
    const bool currentPass = branch.branch.getDouble(index) <= branch.cfg.floatThreshold;
    if (currentPass != pass) {
      branch.branch.setDouble(index, pass ? branch.cfg.passDoubleValue : branch.cfg.failDoubleValue);
    }
  }
}

void enableBranchIfPresent(TTree* tree, const std::string& name) {
  if (!name.empty() && tree->GetBranch(name.c_str())) tree->SetBranchStatus(name.c_str(), 1);
}

std::string eventReferenceFlavor(const EffBranchConfig& cfg) {
  if (!cfg.referenceFlavor.empty()) return cfg.referenceFlavor;
  if (cfg.name.find("Ele") != std::string::npos || cfg.name.find("Ele") != std::string::npos) return "electron";
  if (cfg.name.find("Mu") != std::string::npos) return "muon";
  return "muon";
}

bool leadingKinematics(const BranchBuffer& n,
                       const BranchBuffer& pt,
                       const BranchBuffer& eta,
                       double& leadingPt,
                       double& leadingEta,
                       std::size_t& leadingIndex) {
  if (!n.bound() || !pt.bound() || !eta.bound()) return false;
  const std::size_t nObj = static_cast<std::size_t>(n.getUInt64(0));
  const std::size_t limit = std::min({nObj, pt.availableForN(nObj), eta.availableForN(nObj)});
  if (limit == 0) return false;
  leadingIndex = 0;
  leadingPt = pt.getDouble(0);
  leadingEta = eta.getDouble(0);
  for (std::size_t i = 1; i < limit; ++i) {
    const double candidatePt = pt.getDouble(i);
    if (candidatePt > leadingPt) {
      leadingPt = candidatePt;
      leadingEta = eta.getDouble(i);
      leadingIndex = i;
    }
  }
  return true;
}

void prescanFlavor(TTree* tree,
                   const Config& cfg,
                   const std::string& input,
                   bool isMuon,
                   std::size_t maxN,
                   Calibration& outCal) {
  const LeptonBranches& br = isMuon ? cfg.muonBranches : cfg.electronBranches;
  const std::vector<EffBranchConfig>& effCfgs = isMuon ? cfg.muonEffBranches : cfg.electronEffBranches;
  std::map<std::string, EffCounts>& maps = isMuon ? outCal.muon : outCal.electron;
  if (!cfg.efficiencyEnabled || effCfgs.empty()) return;

  const std::string context = input + (isMuon ? " [muon prescan]" : " [electron prescan]");
  tree->ResetBranchAddresses();
  tree->SetBranchStatus("*", 0);
  enableBranchIfPresent(tree, br.n);
  enableBranchIfPresent(tree, br.pt);
  enableBranchIfPresent(tree, br.eta);
  for (const auto& e : effCfgs) enableBranchIfPresent(tree, e.name);

  BranchBuffer n, pt, eta;
  if (!n.bind(tree, br.n, 1, true, context)) return;
  if (!pt.bind(tree, br.pt, maxN + 1, true, context)) return;
  if (!eta.bind(tree, br.eta, maxN + 1, true, context)) return;
  BranchBuffer energy;
  bool useEnergy = false;
  if (!cfg.binning.energy.empty()) {
    if (!br.energy.empty()) {
      useEnergy = energy.bind(tree, br.energy, maxN + 1, true, context);
    }
    if (!useEnergy) {
      logLine("WARN", context + ": energy binning configured without a usable energy branch; using pt*cosh(eta) proxy");
    }
  }

  std::vector<EffBranchRuntime> effBranches;
  for (const auto& e : effCfgs) {
    EffBranchRuntime rt;
    rt.cfg = e;
    auto it = maps.find(e.name);
    if (it == maps.end()) continue;
    rt.counts = &it->second;
    if (rt.branch.bind(tree, e.name, maxN + 1, true, context)) effBranches.push_back(std::move(rt));
  }
  if (effBranches.empty()) return;

  const Long64_t entries = tree->GetEntries();
  for (Long64_t entry = 0; entry < entries; ++entry) {
    tree->GetEntry(entry);
    const std::size_t nObj = static_cast<std::size_t>(n.getUInt64(0));
    const std::size_t limit = std::min({nObj, pt.availableForN(nObj), eta.availableForN(nObj)});
    for (std::size_t i = 0; i < limit; ++i) {
      const double energyValue = useEnergy && i < energy.availableForN(nObj) ? energy.getDouble(i) : std::numeric_limits<double>::quiet_NaN();
      const BinIndex idx = makeBinIndex(cfg.binning, pt.getDouble(i), eta.getDouble(i), energyValue);
      for (auto& e : effBranches) {
        if (i >= e.branch.availableForN(nObj)) continue;
        e.counts->add(idx.flat, originalPasses(e.cfg, e.branch, i));
      }
    }
  }
}

void prescanEventEfficiencies(TTree* tree,
                              const Config& cfg,
                              const std::string& input,
                              std::size_t maxMuon,
                              std::size_t maxElectron,
                              Calibration& outCal) {
  if (!cfg.efficiencyEnabled || cfg.eventEffBranches.empty()) return;
  const std::string context = input + " [event prescan]";
  tree->ResetBranchAddresses();
  tree->SetBranchStatus("*", 0);
  enableBranchIfPresent(tree, cfg.muonBranches.n);
  enableBranchIfPresent(tree, cfg.muonBranches.pt);
  enableBranchIfPresent(tree, cfg.muonBranches.eta);
  enableBranchIfPresent(tree, cfg.electronBranches.n);
  enableBranchIfPresent(tree, cfg.electronBranches.pt);
  enableBranchIfPresent(tree, cfg.electronBranches.eta);
  for (const auto& e : cfg.eventEffBranches) enableBranchIfPresent(tree, e.name);

  BranchBuffer nMuon, muPt, muEta, nElectron, elePt, eleEta;
  nMuon.bind(tree, cfg.muonBranches.n, 1, false, context);
  muPt.bind(tree, cfg.muonBranches.pt, maxMuon + 1, false, context);
  muEta.bind(tree, cfg.muonBranches.eta, maxMuon + 1, false, context);
  nElectron.bind(tree, cfg.electronBranches.n, 1, false, context);
  elePt.bind(tree, cfg.electronBranches.pt, maxElectron + 1, false, context);
  eleEta.bind(tree, cfg.electronBranches.eta, maxElectron + 1, false, context);

  std::vector<EffBranchRuntime> eventBranches;
  for (const auto& e : cfg.eventEffBranches) {
    EffBranchRuntime rt;
    rt.cfg = e;
    auto it = outCal.event.find(e.name);
    if (it == outCal.event.end()) continue;
    rt.counts = &it->second;
    if (rt.branch.bind(tree, e.name, 1, true, context)) eventBranches.push_back(std::move(rt));
  }
  if (eventBranches.empty()) return;

  const Long64_t entries = tree->GetEntries();
  for (Long64_t entry = 0; entry < entries; ++entry) {
    tree->GetEntry(entry);
    for (auto& e : eventBranches) {
      const std::string ref = eventReferenceFlavor(e.cfg);
      double leadPt = 0.0;
      double leadEta = 0.0;
      std::size_t leadIndex = 0;
      const bool haveLead = ref == "electron"
          ? leadingKinematics(nElectron, elePt, eleEta, leadPt, leadEta, leadIndex)
          : leadingKinematics(nMuon, muPt, muEta, leadPt, leadEta, leadIndex);
      if (!haveLead) continue;
      const BinIndex idx = makeBinIndex(cfg.binning, leadPt, leadEta);
      e.counts->add(idx.flat, originalPasses(e.cfg, e.branch, 0));
    }
  }
}

PreScanResult prescanFile(const Config& cfg, const std::string& input) {
  PreScanResult result;
  result.input = input;
  result.calibration = makeEmptyCalibration(cfg);

  std::unique_ptr<TFile> file(TFile::Open(input.c_str(), "READ"));
  if (!file || file->IsZombie()) fail("Cannot open input file " + quote(input));
  TTree* tree = dynamic_cast<TTree*>(file->Get(cfg.treeName.c_str()));
  if (!tree) fail("Input file " + quote(input) + " does not contain tree " + quote(cfg.treeName));
  tree->SetCacheSize(64LL * 1024LL * 1024LL);

  result.maxMuon = readMaxCount(tree, cfg.muonBranches.n, input + " [max nMuon]");
  result.maxElectron = readMaxCount(tree, cfg.electronBranches.n, input + " [max nElectron]");
  prescanFlavor(tree, cfg, input, true, result.maxMuon, result.calibration);
  prescanFlavor(tree, cfg, input, false, result.maxElectron, result.calibration);
  prescanEventEfficiencies(tree, cfg, input, result.maxMuon, result.maxElectron, result.calibration);
  tree->ResetBranchAddresses();
  tree->SetBranchStatus("*", 1);
  return result;
}

// ----------------------------- Modification -------------------------------

struct FlavorRuntime {
  bool active = false;
  bool isMuon = false;
  BranchBuffer n;
  BranchBuffer pt;
  BranchBuffer eta;
  BranchBuffer charge;
  BranchBuffer energy;
  bool useEnergy = false;
  bool warnedSizeMismatch = false;
  std::vector<EffBranchRuntime> effBranches;
};

FlavorRuntime bindFlavorForModification(TTree* tree,
                                        const Config& cfg,
                                        const Calibration& cal,
                                        const std::string& input,
                                        bool isMuon,
                                        std::size_t maxN) {
  FlavorRuntime rt;
  rt.isMuon = isMuon;
  const LeptonBranches& br = isMuon ? cfg.muonBranches : cfg.electronBranches;
  const std::vector<EffBranchConfig>& effCfgs = isMuon ? cfg.muonEffBranches : cfg.electronEffBranches;
  const std::map<std::string, EffCounts>& maps = isMuon ? cal.muon : cal.electron;
  const std::string context = input + (isMuon ? " [muon modify]" : " [electron modify]");

  if (!rt.n.bind(tree, br.n, 1, true, context)) return rt;
  if (!rt.pt.bind(tree, br.pt, maxN + 1, true, context)) return rt;
  if (!isFloatingType(rt.pt.valueType())) {
    logLine("WARN", context + ": pT branch " + quote(br.pt) + " is " + valueTypeName(rt.pt.valueType()) + ", expected Float_t/Double_t");
  }
  if (!rt.eta.bind(tree, br.eta, maxN + 1, true, context)) return rt;
  if (!br.charge.empty()) rt.charge.bind(tree, br.charge, maxN + 1, false, context);
  if (!cfg.binning.energy.empty()) {
    if (!br.energy.empty()) {
      rt.useEnergy = rt.energy.bind(tree, br.energy, maxN + 1, true, context);
    }
    if (!rt.useEnergy) {
      logLine("WARN", context + ": energy binning configured without a usable energy branch; using pt*cosh(eta) proxy");
    }
  }

  if (cfg.efficiencyEnabled) {
    for (const auto& e : effCfgs) {
      auto it = maps.find(e.name);
      if (it == maps.end() || it->second.globalTotal == 0) {
        logLine("WARN", context + ": no calibration entries for efficiency branch " + quote(e.name) + "; branch will not be modified");
        continue;
      }
      EffBranchRuntime brt;
      brt.cfg = e;
      brt.counts = const_cast<EffCounts*>(&it->second);
      if (brt.branch.bind(tree, e.name, maxN + 1, true, context)) rt.effBranches.push_back(std::move(brt));
    }
  }

  rt.active = true;
  return rt;
}

struct EventEffRuntime {
  EffBranchRuntime eff;
  std::string referenceFlavor;
};

struct EventRuntime {
  std::vector<EventEffRuntime> branches;
};

EventRuntime bindEventEfficienciesForModification(TTree* tree,
                                                  const Config& cfg,
                                                  const Calibration& cal,
                                                  const std::string& input) {
  EventRuntime rt;
  if (!cfg.efficiencyEnabled || cfg.eventEffBranches.empty()) return rt;
  const std::string context = input + " [event modify]";
  for (const auto& e : cfg.eventEffBranches) {
    auto it = cal.event.find(e.name);
    if (it == cal.event.end() || it->second.globalTotal == 0) {
      logLine("WARN", context + ": no calibration entries for event efficiency branch " + quote(e.name) + "; branch will not be modified");
      continue;
    }
    EventEffRuntime brt;
    brt.eff.cfg = e;
    brt.referenceFlavor = eventReferenceFlavor(e);
    brt.eff.counts = const_cast<EffCounts*>(&it->second);
    if (brt.eff.branch.bind(tree, e.name, 1, true, context)) rt.branches.push_back(std::move(brt));
  }
  return rt;
}

void processFlavor(FlavorRuntime& rt,
                   const Config& cfg,
                   std::uint64_t run,
                   std::uint64_t lumi,
                   std::uint64_t eventId,
                   Long64_t entry) {
  if (!rt.active) return;
  const bool isMuon = rt.isMuon;
  const int flavorId = isMuon ? 13 : 11;
  const std::vector<RegionScale>& scaleRegions = isMuon ? cfg.muonScale : cfg.electronScale;
  const std::vector<RegionResolution>& resRegions = isMuon ? cfg.muonResolution : cfg.electronResolution;
  const std::size_t nObj = static_cast<std::size_t>(rt.n.getUInt64(0));
  const std::size_t limit = std::min({nObj, rt.pt.availableForN(nObj), rt.eta.availableForN(nObj)});
  if (limit < nObj && !rt.warnedSizeMismatch) {
    logLine("WARN", std::string(isMuon ? "Muon" : "Electron") + " array length smaller than configured n branch; modifying available elements only");
    rt.warnedSizeMismatch = true;
  }

  for (std::size_t i = 0; i < limit; ++i) {
    const double oldPt = rt.pt.getDouble(i);
    const double eta = rt.eta.getDouble(i);
    const double oldEnergy = rt.useEnergy && i < rt.energy.availableForN(nObj) ? rt.energy.getDouble(i) : std::numeric_limits<double>::quiet_NaN();
    const int charge = rt.charge.bound() && i < rt.charge.availableForN(nObj) ? static_cast<int>(rt.charge.getInt64(i)) : 0;

    double newPt = oldPt;
    if (cfg.scaleEnabled) {
      newPt *= 1.0 + scaleShift(scaleRegions, eta, oldPt, charge, cfg.scalePtReference);
    }
    if (cfg.resolutionEnabled) {
      const double sigma = resolutionSigma(resRegions, eta, oldPt, cfg.scalePtReference);
      if (sigma > 0.0) {
        const std::uint64_t key = objectKey(cfg, run, lumi, eventId, entry, i, flavorId, "resolution");
        newPt *= 1.0 + normal01(key) * sigma;
      }
    }
    if (!std::isfinite(newPt) || newPt < 0.0) newPt = 0.0;
    rt.pt.setDouble(i, newPt);

    if (cfg.efficiencyEnabled) {
      const double scaledEnergy = std::isfinite(oldEnergy) && oldPt > 0.0 ? oldEnergy * (newPt / oldPt) : std::numeric_limits<double>::quiet_NaN();
      const BinIndex idx = makeBinIndex(cfg.binning, newPt, eta, scaledEnergy);
      for (auto& e : rt.effBranches) {
        if (i >= e.branch.availableForN(nObj)) continue;
        const double base = e.counts->efficiency(idx.flat);
        const double p = distortedEfficiency(base, e.cfg, idx, newPt);
        const std::uint64_t key = objectKey(cfg, run, lumi, eventId, entry, i, flavorId, "efficiency:" + e.cfg.name);
        const bool pass = uniform01(key) < p;
        writeEfficiencyValue(e, i, pass);
      }
    }
  }
}

void processEventEfficiencies(EventRuntime& eventRt,
                              const FlavorRuntime& muon,
                              const FlavorRuntime& electron,
                              const Config& cfg,
                              std::uint64_t run,
                              std::uint64_t lumi,
                              std::uint64_t eventId,
                              Long64_t entry) {
  if (!cfg.efficiencyEnabled || eventRt.branches.empty()) return;
  for (auto& e : eventRt.branches) {
    const FlavorRuntime& ref = e.referenceFlavor == "electron" ? electron : muon;
    if (!ref.active) continue;
    double leadPt = 0.0;
    double leadEta = 0.0;
    std::size_t leadIndex = 0;
    if (!leadingKinematics(ref.n, ref.pt, ref.eta, leadPt, leadEta, leadIndex)) continue;
    const BinIndex idx = makeBinIndex(cfg.binning, leadPt, leadEta);
    const double base = e.eff.counts->efficiency(idx.flat);
    const double p = distortedEfficiency(base, e.eff.cfg, idx, leadPt);
    const int flavorId = e.referenceFlavor == "electron" ? 11 : 13;
    const std::uint64_t key = objectKey(cfg, run, lumi, eventId, entry, leadIndex, flavorId, "efficiency:" + e.eff.cfg.name);
    writeEfficiencyValue(e.eff, 0, uniform01(key) < p);
  }
}

void copyOtherObjects(TDirectory* inDir,
                      TDirectory* outDir,
                      const std::string& eventsTreeName,
                      bool topLevel,
                      bool copyMetadataTrees) {
  TIter next(inDir->GetListOfKeys());
  while (TKey* key = static_cast<TKey*>(next())) {
    const std::string name = key->GetName();
    if (topLevel && name == eventsTreeName) continue;

    std::unique_ptr<TObject> obj(key->ReadObj());
    if (!obj) continue;

    outDir->cd();
    if (obj->InheritsFrom(TDirectory::Class())) {
      TDirectory* subIn = dynamic_cast<TDirectory*>(obj.get());
      TDirectory* subOut = outDir->mkdir(name.c_str(), key->GetTitle());
      if (subIn && subOut) copyOtherObjects(subIn, subOut, eventsTreeName, false, copyMetadataTrees);
      continue;
    }

    if (obj->InheritsFrom(TTree::Class())) {
      if (!copyMetadataTrees) continue;
      TTree* tree = dynamic_cast<TTree*>(obj.get());
      if (!tree) continue;
      outDir->cd();
      TTree* clone = tree->CloneTree(-1, "fast");
      if (clone) {
        clone->Write(name.c_str(), TObject::kOverwrite);
        delete clone;
      }
      continue;
    }

    outDir->cd();
    obj->Write(name.c_str(), TObject::kOverwrite);
  }
}

void modifyFile(const Config& cfg,
                const Calibration& calibration,
                const PreScanResult& scan,
                const std::string& outputPath) {
  if (fs::exists(outputPath) && !cfg.overwrite) {
    fail("Output file already exists and output.overwrite is false: " + quote(outputPath));
  }
  fs::create_directories(fs::path(outputPath).parent_path());

  std::unique_ptr<TFile> inFile(TFile::Open(scan.input.c_str(), "READ"));
  if (!inFile || inFile->IsZombie()) fail("Cannot open input file " + quote(scan.input));
  TTree* inTree = dynamic_cast<TTree*>(inFile->Get(cfg.treeName.c_str()));
  if (!inTree) fail("Input file " + quote(scan.input) + " does not contain tree " + quote(cfg.treeName));
  inTree->SetCacheSize(128LL * 1024LL * 1024LL);
  inTree->SetBranchStatus("*", 1);

  BranchBuffer run, lumi, event;
  run.bind(inTree, cfg.eventId.run, 1, false, scan.input + " [event id]");
  lumi.bind(inTree, cfg.eventId.luminosityBlock, 1, false, scan.input + " [event id]");
  event.bind(inTree, cfg.eventId.event, 1, false, scan.input + " [event id]");

  FlavorRuntime muon = bindFlavorForModification(inTree, cfg, calibration, scan.input, true, scan.maxMuon);
  FlavorRuntime electron = bindFlavorForModification(inTree, cfg, calibration, scan.input, false, scan.maxElectron);
  EventRuntime eventEff = bindEventEfficienciesForModification(inTree, cfg, calibration, scan.input);

  const char* mode = cfg.overwrite ? "RECREATE" : "CREATE";
  std::unique_ptr<TFile> outFile(TFile::Open(outputPath.c_str(), mode));
  if (!outFile || outFile->IsZombie()) fail("Cannot create output file " + quote(outputPath));
  outFile->SetCompressionSettings(inFile->GetCompressionSettings());
  outFile->cd();

  TTree* outTree = inTree->CloneTree(0);
  if (!outTree) fail("Failed to clone tree structure for " + quote(scan.input));

  const Long64_t entries = inTree->GetEntries();
  for (Long64_t entry = 0; entry < entries; ++entry) {
    inTree->GetEntry(entry);
    const std::uint64_t runValue = run.bound() ? run.getUInt64(0) : 0;
    const std::uint64_t lumiValue = lumi.bound() ? lumi.getUInt64(0) : 0;
    const std::uint64_t eventValue = event.bound() ? event.getUInt64(0) : 0;
    processFlavor(muon, cfg, runValue, lumiValue, eventValue, entry);
    processFlavor(electron, cfg, runValue, lumiValue, eventValue, entry);
    processEventEfficiencies(eventEff, muon, electron, cfg, runValue, lumiValue, eventValue, entry);
    outTree->Fill();
  }

  outFile->cd();
  outTree->Write(cfg.treeName.c_str(), TObject::kOverwrite);
  copyOtherObjects(inFile.get(), outFile.get(), cfg.treeName, true, cfg.copyMetadataTrees);
  outFile->Write();
  outFile->Close();
  inTree->ResetBranchAddresses();
  logLine("INFO", "Wrote " + quote(outputPath) + " from " + quote(scan.input));
}

// ----------------------------- Parallelism --------------------------------

template <typename Func>
void parallelFor(std::size_t n, unsigned threads, Func func) {
  if (n == 0) return;
  const unsigned nThreads = std::max(1u, std::min<unsigned>(threads, static_cast<unsigned>(n)));
  std::atomic<std::size_t> next{0};
  std::mutex errMutex;
  std::exception_ptr firstError = nullptr;
  std::vector<std::thread> workers;
  workers.reserve(nThreads);

  for (unsigned t = 0; t < nThreads; ++t) {
    workers.emplace_back([&]() {
      while (true) {
        const std::size_t i = next.fetch_add(1);
        if (i >= n) break;
        try {
          func(i);
        } catch (...) {
          std::lock_guard<std::mutex> lock(errMutex);
          if (!firstError) firstError = std::current_exception();
        }
      }
    });
  }
  for (auto& w : workers) w.join();
  if (firstError) std::rethrow_exception(firstError);
}

// ----------------------------- CLI / main ---------------------------------

struct Cli {
  std::string configPath;
  bool dryRun = false;
  int threadsOverride = 0;
};

void printUsage() {
  std::cerr << "Usage: ./modify_nanoaod --config config.json [--dry-run] [--threads N]\n";
}

Cli parseCli(int argc, char** argv) {
  Cli cli;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg == "--config" && i + 1 < argc) {
      cli.configPath = argv[++i];
    } else if (arg == "--dry-run") {
      cli.dryRun = true;
    } else if (arg == "--threads" && i + 1 < argc) {
      cli.threadsOverride = std::max(1, std::atoi(argv[++i]));
    } else if (arg == "--help" || arg == "-h") {
      printUsage();
      std::exit(0);
    } else {
      printUsage();
      fail("Unknown or incomplete argument " + quote(arg));
    }
  }
  if (cli.configPath.empty()) {
    printUsage();
    fail("Missing --config");
  }
  return cli;
}

void dryRunInspect(const Config& cfg, const std::vector<std::string>& inputs, const std::vector<std::string>& outputs) {
  logLine("INFO", "Dry run: no output files will be written");
  for (std::size_t i = 0; i < inputs.size(); ++i) {
    std::unique_ptr<TFile> file(TFile::Open(inputs[i].c_str(), "READ"));
    if (!file || file->IsZombie()) {
      logLine("WARN", "Cannot open " + quote(inputs[i]));
      continue;
    }
    TTree* tree = dynamic_cast<TTree*>(file->Get(cfg.treeName.c_str()));
    if (!tree) {
      logLine("WARN", quote(inputs[i]) + " does not contain tree " + quote(cfg.treeName));
      continue;
    }
    std::ostringstream os;
    os << "Would process " << quote(inputs[i]) << " -> " << quote(outputs[i])
       << " entries=" << tree->GetEntries()
       << " branches=" << tree->GetNbranches();
    logLine("INFO", os.str());
  }
}

}  // namespace

int main(int argc, char** argv) {
  try {
    ROOT::EnableThreadSafety();
    TH1::AddDirectory(false);

    const Cli cli = parseCli(argc, argv);
    Config cfg = parseConfig(cli.configPath);
    if (cli.threadsOverride > 0) cfg.threads = static_cast<unsigned>(cli.threadsOverride);

    std::vector<std::string> inputs = expandInputPaths(cfg);
    if (inputs.empty()) fail("No input ROOT files found");
    std::vector<std::string> outputs = makeOutputPaths(cfg, inputs);

    std::ostringstream summary;
    summary << "Inputs=" << inputs.size()
            << " threads=" << cfg.threads
            << " tree=" << quote(cfg.treeName)
            << " output_dir=" << quote(cfg.outputDirectory);
    logLine("INFO", summary.str());

    if (cli.dryRun) {
      dryRunInspect(cfg, inputs, outputs);
      return 0;
    }

    logLine("INFO", "Stage A: pre-scanning all input files for one merged global efficiency calibration");
    std::vector<PreScanResult> scans(inputs.size());
    parallelFor(inputs.size(), cfg.threads, [&](std::size_t i) {
      scans[i] = prescanFile(cfg, inputs[i]);
      std::ostringstream os;
      os << "Pre-scanned " << quote(inputs[i])
         << " max nMuon=" << scans[i].maxMuon
         << " max nElectron=" << scans[i].maxElectron;
      logLine("INFO", os.str());
    });

    Calibration calibration = makeEmptyCalibration(cfg);
    for (const PreScanResult& scan : scans) mergeCalibration(calibration, scan.calibration);
    if (cfg.efficiencyEnabled) {
      logLine("INFO", "Merged efficiency calibration will be used for every output file");
      for (const auto& kv : calibration.muon) {
        logLine("INFO", "Muon efficiency calibration " + quote(kv.first) + ": total=" + std::to_string(kv.second.globalTotal));
      }
      for (const auto& kv : calibration.electron) {
        logLine("INFO", "Electron efficiency calibration " + quote(kv.first) + ": total=" + std::to_string(kv.second.globalTotal));
      }
      for (const auto& kv : calibration.event) {
        logLine("INFO", "Event efficiency calibration " + quote(kv.first) + ": total=" + std::to_string(kv.second.globalTotal));
      }
    }

    logLine("INFO", "Stage B: writing one modified ROOT file per input file using the merged calibration");
    parallelFor(scans.size(), cfg.threads, [&](std::size_t i) {
      modifyFile(cfg, calibration, scans[i], outputs[i]);
    });
    logLine("INFO", "Done");
    return 0;
  } catch (const std::exception& e) {
    logLine("ERROR", e.what());
    return 1;
  }
}
