// SO Sprint Widget v2 — always-on-top reading tracker for the SO written exam.
// Native Win32 + GDI+. Grows sideways only. Serial-numbered sessions with page totals and
// countdown timers; every finished sitting is logged to Desktop\SOPrep\SO_Study_Log.xlsx and
// every finished round produces a JPG report in Desktop\SOPrep.
#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif
#define NOMINMAX
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <shellapi.h>
#include <commctrl.h>
#include <dwmapi.h>
#include <shlobj.h>
#include <algorithm>
#include <cmath>
#include <cstdarg>
#include <cstdio>
#include <cwchar>
#include <string>
#include <vector>
using std::max;
using std::min;
#include <gdiplus.h>

#define IDI_APP 101
#define WM_TRAY (WM_APP + 1)
#define TIMER_TICK 1
#define TIMER_TOP 2

// ───────────────────────── model ─────────────────────────
struct Cat {
  std::wstring name;
  int done = 0, target = 100;
  long long secs = 0;  // total reading time
  int mins = 0;        // planned minutes per sitting
  long long rem = 0;   // countdown seconds left
};
struct LogRow {
  int round = 1, serial = 1;
  std::wstring name, date, start, end, status;
  int planned = 0, actualSec = 0, p0 = 0, p1 = 0, target = 0;
};
struct Theme { const wchar_t* name; COLORREF bg1, bg2, text, muted, track, btn, btnHover, line; };
static const Theme THEMES[] = {
    {L"Midnight", RGB(13, 18, 33), RGB(25, 33, 54), RGB(234, 239, 247), RGB(146, 160, 184), RGB(48, 61, 86), RGB(36, 47, 72), RGB(55, 70, 102), RGB(42, 54, 80)},
    {L"Ocean", RGB(7, 26, 45), RGB(13, 45, 74), RGB(226, 240, 252), RGB(138, 174, 202), RGB(32, 70, 102), RGB(20, 56, 88), RGB(32, 80, 120), RGB(26, 62, 96)},
    {L"Plum", RGB(30, 15, 36), RGB(50, 24, 56), RGB(246, 232, 246), RGB(188, 158, 194), RGB(78, 46, 86), RGB(62, 34, 70), RGB(88, 52, 98), RGB(70, 40, 78)},
    {L"Paper", RGB(251, 252, 254), RGB(237, 241, 247), RGB(15, 23, 42), RGB(98, 113, 136), RGB(213, 220, 231), RGB(226, 232, 240), RGB(203, 213, 225), RGB(221, 227, 236)},
};
static const COLORREF CAT_COLORS[] = {RGB(52, 211, 153), RGB(56, 189, 248), RGB(251, 191, 36), RGB(251, 113, 133),
                                      RGB(167, 139, 250), RGB(163, 230, 53), RGB(34, 211, 238), RGB(251, 146, 60)};
static const COLORREF GOLD = RGB(250, 204, 21), RED = RGB(248, 113, 113);

struct State {
  std::wstring title = L"SO Written Prep";
  std::vector<Cat> cats;
  int cur = 0, theme = 0, opacity = 100, round = 1;
  bool topmost = true, locked = false;
  double zoom = 1.0;
  int width = 900, x = -1, y = -1;
} S;
struct Session { bool active = false; int cat = 0, startDone = 0; long long secs = 0; SYSTEMTIME start{}; } SS;
static std::vector<LogRow> g_log;
static bool g_running = false;
static ULONGLONG g_lastTick = 0;
static HWND g_hwnd = nullptr;
static HINSTANCE g_inst = nullptr;
static NOTIFYICONDATAW g_nid{};
static std::wstring g_ini, g_logPath, g_lastXlsx;
static int g_dpi = 96;
static POINT g_mouse{-1, -1};
static bool g_tracking = false;
static ULONG_PTR g_gdipToken = 0;

// ───────────────────────── helpers ─────────────────────────
static std::wstring Fmt(const wchar_t* f, ...) {
  wchar_t b[512];
  va_list ap;
  va_start(ap, f);
  vswprintf(b, 512, f, ap);
  va_end(ap);
  return b;
}
static std::wstring HMS(long long s) {
  if (s < 0) s = 0;
  return s >= 3600 ? Fmt(L"%lld:%02lld:%02lld", s / 3600, (s / 60) % 60, s % 60) : Fmt(L"%02lld:%02lld", s / 60, s % 60);
}
static std::wstring Mins(double m) {
  long long v = (long long)std::lround(m);
  return v >= 60 ? Fmt(L"%lldh %02lldm", v / 60, v % 60) : Fmt(L"%lldm", v);
}
static COLORREF CatColor(int i) { return CAT_COLORS[((i % 8) + 8) % 8]; }
static COLORREF Mix(COLORREF a, COLORREF b, double t) {
  return RGB((int)(GetRValue(a) * (1 - t) + GetRValue(b) * t), (int)(GetGValue(a) * (1 - t) + GetGValue(b) * t), (int)(GetBValue(a) * (1 - t) + GetBValue(b) * t));
}
static Gdiplus::Color GC(COLORREF c, BYTE a = 255) { return Gdiplus::Color(a, GetRValue(c), GetGValue(c), GetBValue(c)); }
static std::wstring DateS(const SYSTEMTIME& t) { return Fmt(L"%04d-%02d-%02d", t.wYear, t.wMonth, t.wDay); }
static std::wstring TimeS(const SYSTEMTIME& t) { return Fmt(L"%02d:%02d", t.wHour, t.wMinute); }
static long long FT(const SYSTEMTIME& t) { FILETIME f{}; SystemTimeToFileTime(&t, &f); return ((long long)f.dwHighDateTime << 32) | f.dwLowDateTime; }
static SYSTEMTIME FromFT(long long v) { FILETIME f{(DWORD)v, (DWORD)(v >> 32)}; SYSTEMTIME t{}; FileTimeToSystemTime(&f, &t); return t; }
static int TotalDone() { int s = 0; for (auto& c : S.cats) s += std::min(c.done, c.target); return s; }
static int TotalTarget() { int s = 0; for (auto& c : S.cats) s += c.target; return s; }
static double TotalFrac() { int t = TotalTarget(); return t ? (double)TotalDone() / t : 0; }
static std::wstring SOPrepDir() {
  wchar_t buf[MAX_PATH];
  std::wstring d = SUCCEEDED(SHGetFolderPathW(nullptr, CSIDL_DESKTOPDIRECTORY, nullptr, 0, buf)) ? buf : L".";
  d += L"\\SOPrep";
  CreateDirectoryW(d.c_str(), nullptr);
  return d;
}
static std::string U8(const std::wstring& w) {
  if (w.empty()) return {};
  int n = WideCharToMultiByte(CP_UTF8, 0, w.c_str(), (int)w.size(), nullptr, 0, nullptr, nullptr);
  std::string s(n, '\0');
  WideCharToMultiByte(CP_UTF8, 0, w.c_str(), (int)w.size(), s.data(), n, nullptr, nullptr);
  return s;
}
static std::wstring W8(const std::string& s) {
  if (s.empty()) return {};
  int n = MultiByteToWideChar(CP_UTF8, 0, s.c_str(), (int)s.size(), nullptr, 0);
  std::wstring w(n, L'\0');
  MultiByteToWideChar(CP_UTF8, 0, s.c_str(), (int)s.size(), w.data(), n);
  return w;
}
static std::vector<std::wstring> Split(const std::wstring& s, wchar_t d) {
  std::vector<std::wstring> v;
  size_t a = 0, b;
  while ((b = s.find(d, a)) != std::wstring::npos) { v.push_back(s.substr(a, b - a)); a = b + 1; }
  v.push_back(s.substr(a));
  return v;
}
static std::wstring Clean(std::wstring s) { for (auto& ch : s) if (ch == L'\t' || ch == L'\n' || ch == L'\r') ch = L' '; return s; }

// ───────────────────────── persistence ─────────────────────────
static void PutI(const wchar_t* sec, const wchar_t* key, long long v) { WritePrivateProfileStringW(sec, key, std::to_wstring(v).c_str(), g_ini.c_str()); }
static long long GetI(const wchar_t* sec, const wchar_t* key, long long def) {
  wchar_t b[40];
  GetPrivateProfileStringW(sec, key, L"", b, 40, g_ini.c_str());
  return b[0] ? _wtoi64(b) : def;
}
static std::wstring GetS(const wchar_t* sec, const wchar_t* key, const std::wstring& def) {
  wchar_t b[512];
  GetPrivateProfileStringW(sec, key, L"\x01", b, 512, g_ini.c_str());
  return b[0] == 1 ? def : b;
}
static void Save() {
  const wchar_t* A = L"app";
  WritePrivateProfileStringW(A, L"title", S.title.c_str(), g_ini.c_str());
  PutI(A, L"version", 2); PutI(A, L"cur", S.cur); PutI(A, L"theme", S.theme); PutI(A, L"opacity", S.opacity); PutI(A, L"round", S.round);
  PutI(A, L"topmost", S.topmost); PutI(A, L"locked", S.locked); PutI(A, L"zoom", std::lround(S.zoom * 100));
  PutI(A, L"width", S.width); PutI(A, L"x", S.x); PutI(A, L"y", S.y); PutI(A, L"cats", (long long)S.cats.size());
  for (size_t i = 0; i < S.cats.size() + 4; i++) {
    std::wstring sec = L"cat" + std::to_wstring(i);
    if (i >= S.cats.size()) { WritePrivateProfileStringW(sec.c_str(), nullptr, nullptr, g_ini.c_str()); continue; }
    const Cat& c = S.cats[i];
    WritePrivateProfileStringW(sec.c_str(), L"name", c.name.c_str(), g_ini.c_str());
    PutI(sec.c_str(), L"done", c.done); PutI(sec.c_str(), L"target", c.target); PutI(sec.c_str(), L"secs", c.secs);
    PutI(sec.c_str(), L"mins", c.mins); PutI(sec.c_str(), L"rem", c.rem);
  }
  const wchar_t* Z = L"session";
  PutI(Z, L"active", SS.active); PutI(Z, L"cat", SS.cat); PutI(Z, L"startDone", SS.startDone); PutI(Z, L"secs", SS.secs); PutI(Z, L"start", FT(SS.start));
}
static void LoadLog() {
  g_log.clear();
  FILE* f = _wfopen(g_logPath.c_str(), L"rb");
  if (!f) return;
  std::string all;
  char buf[4096];
  size_t n;
  while ((n = fread(buf, 1, sizeof buf, f)) > 0) all.append(buf, n);
  fclose(f);
  for (auto& line : Split(W8(all), L'\n')) {
    auto v = Split(line, L'\t');
    if (v.size() < 12) continue;
    LogRow r;
    r.round = _wtoi(v[0].c_str()); r.serial = _wtoi(v[1].c_str()); r.name = v[2]; r.date = v[3]; r.start = v[4]; r.end = v[5];
    r.planned = _wtoi(v[6].c_str()); r.actualSec = _wtoi(v[7].c_str()); r.p0 = _wtoi(v[8].c_str()); r.p1 = _wtoi(v[9].c_str());
    r.target = _wtoi(v[10].c_str()); r.status = v[11];
    g_log.push_back(r);
  }
}
static void AppendLog(const LogRow& r) {
  g_log.push_back(r);
  FILE* f = _wfopen(g_logPath.c_str(), L"ab");
  if (!f) return;
  std::wstring line = Fmt(L"%d\t%d\t%ls\t%ls\t%ls\t%ls\t%d\t%d\t%d\t%d\t%d\t%ls\n", r.round, r.serial, Clean(r.name).c_str(), r.date.c_str(), r.start.c_str(),
                          r.end.c_str(), r.planned, r.actualSec, r.p0, r.p1, r.target, r.status.c_str());
  std::string u = U8(line);
  fwrite(u.data(), 1, u.size(), f);
  fclose(f);
}
static void Load() {
  wchar_t buf[MAX_PATH];
  std::wstring dir = SUCCEEDED(SHGetFolderPathW(nullptr, CSIDL_APPDATA, nullptr, 0, buf)) ? std::wstring(buf) + L"\\SOSprintWidget" : L".";
  CreateDirectoryW(dir.c_str(), nullptr);
  g_ini = dir + L"\\settings.ini";
  g_logPath = dir + L"\\sessions.tsv";
  LoadLog();
  const wchar_t* A = L"app";
  int n = (int)GetI(A, L"cats", -1);
  if (n < 0) {
    S.cats = {{L"Focus Writing", 0, 115, 0, 120}, {L"Math (Khairul)", 0, 170, 0, 120}, {L"Analytical", 0, 80, 0, 90}, {L"English Focus", 0, 31, 0, 60},
              {L"Proficiency", 0, 28, 0, 60}, {L"Finance (Alal)", 0, 40, 0, 60}, {L"Translation", 0, 18, 0, 45}, {L"GK 500", 0, 19, 0, 60}};
    for (auto& c : S.cats) c.rem = c.mins * 60LL;
    Save();
    return;
  }
  bool v1 = GetI(A, L"version", 1) < 2;
  S.title = GetS(A, L"title", S.title);
  if (v1 && S.title == L"SO Written · 27 Nov") S.title = L"SO Written Prep";
  S.cur = (int)GetI(A, L"cur", 0); S.theme = (int)GetI(A, L"theme", 0); S.opacity = (int)GetI(A, L"opacity", 100);
  S.round = std::max(1, (int)GetI(A, L"round", 1)); S.topmost = GetI(A, L"topmost", 1) != 0; S.locked = GetI(A, L"locked", 0) != 0;
  S.zoom = GetI(A, L"zoom", 100) / 100.0; S.width = (int)GetI(A, L"width", 900); S.x = (int)GetI(A, L"x", -1); S.y = (int)GetI(A, L"y", -1);
  if (v1 && S.width < 900) S.width = 900;
  for (int i = 0; i < n && i < 40; i++) {
    std::wstring sec = L"cat" + std::to_wstring(i);
    Cat c;
    c.name = GetS(sec.c_str(), L"name", L"Session");
    c.target = std::max(1, (int)GetI(sec.c_str(), L"target", 100));
    c.done = std::clamp((int)GetI(sec.c_str(), L"done", 0), 0, c.target);
    c.secs = GetI(sec.c_str(), L"secs", 0);
    c.mins = (int)GetI(sec.c_str(), L"mins", 0);
    c.rem = std::clamp(GetI(sec.c_str(), L"rem", c.mins * 60LL), 0LL, c.mins * 60LL);
    S.cats.push_back(c);
  }
  if (S.cats.empty()) S.cats.push_back({L"Reading", 0, 100, 0, 60, 3600});
  S.cur = std::clamp(S.cur, 0, (int)S.cats.size() - 1);
  S.theme = std::clamp(S.theme, 0, 3); S.opacity = std::clamp(S.opacity, 40, 100); S.zoom = std::clamp(S.zoom, 0.8, 1.8);
  const wchar_t* Z = L"session";
  SS.active = GetI(Z, L"active", 0) != 0; SS.cat = (int)GetI(Z, L"cat", 0); SS.startDone = (int)GetI(Z, L"startDone", 0);
  SS.secs = GetI(Z, L"secs", 0); SS.start = FromFT(GetI(Z, L"start", 0));
  if (SS.cat < 0 || SS.cat >= (int)S.cats.size()) SS.active = false;
}

// ───────────────────────── XLSX writer (stored zip) ─────────────────────────
static unsigned Crc32(const std::string& d) {
  static unsigned t[256];
  static bool init = false;
  if (!init) { for (unsigned i = 0; i < 256; i++) { unsigned c = i; for (int k = 0; k < 8; k++) c = (c & 1) ? 0xEDB88320u ^ (c >> 1) : c >> 1; t[i] = c; } init = true; }
  unsigned c = 0xFFFFFFFFu;
  for (unsigned char ch : d) c = t[(c ^ ch) & 0xFF] ^ (c >> 8);
  return c ^ 0xFFFFFFFFu;
}
static void Le(std::string& o, unsigned v, int n) { for (int i = 0; i < n; i++) o.push_back((char)((v >> (8 * i)) & 0xFF)); }
static bool WriteZip(const std::wstring& path, const std::vector<std::pair<std::string, std::string>>& files) {
  std::string out, cd;
  SYSTEMTIME t; GetLocalTime(&t);
  unsigned dt = ((t.wYear - 1980) << 9) | (t.wMonth << 5) | t.wDay, tm = (t.wHour << 11) | (t.wMinute << 5) | (t.wSecond / 2);
  for (auto& f : files) {
    const std::string &name = f.first, &data = f.second;
    unsigned crc = Crc32(data), off = (unsigned)out.size();
    Le(out, 0x04034b50, 4); Le(out, 20, 2); Le(out, 0x0800, 2); Le(out, 0, 2); Le(out, tm, 2); Le(out, dt, 2);
    Le(out, crc, 4); Le(out, (unsigned)data.size(), 4); Le(out, (unsigned)data.size(), 4); Le(out, (unsigned)name.size(), 2); Le(out, 0, 2);
    out += name; out += data;
    Le(cd, 0x02014b50, 4); Le(cd, 20, 2); Le(cd, 20, 2); Le(cd, 0x0800, 2); Le(cd, 0, 2); Le(cd, tm, 2); Le(cd, dt, 2);
    Le(cd, crc, 4); Le(cd, (unsigned)data.size(), 4); Le(cd, (unsigned)data.size(), 4); Le(cd, (unsigned)name.size(), 2);
    Le(cd, 0, 2); Le(cd, 0, 2); Le(cd, 0, 2); Le(cd, 0, 2); Le(cd, 0, 4); Le(cd, off, 4); cd += name;
  }
  unsigned cdOff = (unsigned)out.size();
  out += cd;
  Le(out, 0x06054b50, 4); Le(out, 0, 2); Le(out, 0, 2); Le(out, (unsigned)files.size(), 2); Le(out, (unsigned)files.size(), 2);
  Le(out, (unsigned)cd.size(), 4); Le(out, cdOff, 4); Le(out, 0, 2);
  FILE* fp = _wfopen(path.c_str(), L"wb");
  if (!fp) return false;
  bool ok = fwrite(out.data(), 1, out.size(), fp) == out.size();
  fclose(fp);
  return ok;
}
static std::string X(const std::wstring& w) {
  std::string s = U8(w), o;
  for (char c : s) { if (c == '&') o += "&amp;"; else if (c == '<') o += "&lt;"; else if (c == '>') o += "&gt;"; else if (c == '"') o += "&quot;"; else o += c; }
  return o;
}
static std::string ColName(int c) { std::string s; c++; while (c) { s.insert(s.begin(), (char)('A' + (c - 1) % 26)); c = (c - 1) / 26; } return s; }
struct Cell { bool num; double v; std::wstring s; int style; };
static Cell N(double v, int st = 0) { return {true, v, L"", st}; }
static Cell T(const std::wstring& s, int st = 0) { return {false, 0, s, st}; }
static std::string Sheet(const std::vector<std::vector<Cell>>& rows, const std::vector<int>& widths) {
  std::string x = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
                  "<sheetViews><sheetView workbookViewId=\"0\"><pane ySplit=\"1\" topLeftCell=\"A2\" activePane=\"bottomLeft\" state=\"frozen\"/></sheetView></sheetViews><cols>";
  for (size_t i = 0; i < widths.size(); i++) x += "<col min=\"" + std::to_string(i + 1) + "\" max=\"" + std::to_string(i + 1) + "\" width=\"" + std::to_string(widths[i]) + "\" customWidth=\"1\"/>";
  x += "</cols><sheetData>";
  for (size_t r = 0; r < rows.size(); r++) {
    x += "<row r=\"" + std::to_string(r + 1) + "\">";
    for (size_t c = 0; c < rows[r].size(); c++) {
      const Cell& e = rows[r][c];
      std::string ref = ColName((int)c) + std::to_string(r + 1), st = e.style ? " s=\"" + std::to_string(e.style) + "\"" : "";
      if (e.num) { char b[40]; snprintf(b, 40, "%.10g", e.v); x += "<c r=\"" + ref + "\"" + st + "><v>" + b + "</v></c>"; }
      else x += "<c r=\"" + ref + "\" t=\"inlineStr\"" + st + "><is><t>" + X(e.s) + "</t></is></c>";
    }
    x += "</row>";
  }
  return x + "</sheetData></worksheet>";
}
static double R1(double v) { return std::round(v * 10) / 10; }
static bool WriteXlsx() {
  std::vector<std::vector<Cell>> a{{T(L"Round", 1), T(L"Serial", 1), T(L"Session", 1), T(L"Date", 1), T(L"Start", 1), T(L"End", 1), T(L"Planned (min)", 1), T(L"Actual (min)", 1),
                                    T(L"From page", 1), T(L"To page", 1), T(L"Pages read", 1), T(L"Pages/hour", 1), T(L"Total pages", 1), T(L"Progress %", 1), T(L"Status", 1)}};
  for (auto& r : g_log) {
    double am = r.actualSec / 60.0, pr = r.p1 - r.p0;
    a.push_back({N(r.round), N(r.serial), T(r.name), T(r.date), T(r.start), T(r.end), N(r.planned), N(R1(am)), N(r.p0), N(r.p1), N(pr),
                 N(am > 0 ? R1(pr / (am / 60)) : 0), N(r.target), N(r.target ? R1(100.0 * r.p1 / r.target) : 0), T(r.status)});
  }
  std::vector<std::vector<Cell>> b{{T(L"Serial", 1), T(L"Session", 1), T(L"Done", 1), T(L"Total pages", 1), T(L"Left", 1), T(L"Progress %", 1), T(L"Time read (min)", 1), T(L"Sittings logged", 1)}};
  for (size_t i = 0; i < S.cats.size(); i++) {
    const Cat& c = S.cats[i];
    int sit = 0; for (auto& r : g_log) if (r.serial == (int)i + 1 && r.name == c.name) sit++;
    b.push_back({N((double)i + 1), T(c.name), N(c.done), N(c.target), N(c.target - c.done), N(R1(100.0 * c.done / c.target)), N(R1(c.secs / 60.0)), N(sit)});
  }
  b.push_back({T(L"", 1), T(L"TOTAL", 1), N(TotalDone(), 1), N(TotalTarget(), 1), N(TotalTarget() - TotalDone(), 1), N(R1(TotalFrac() * 100), 1), T(L"", 1), N((double)g_log.size(), 1)});
  const char* H = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>";
  std::vector<std::pair<std::string, std::string>> files{
      {"[Content_Types].xml", std::string(H) + "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
                              "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/><Default Extension=\"xml\" ContentType=\"application/xml\"/>"
                              "<Override PartName=\"/xl/workbook.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>"
                              "<Override PartName=\"/xl/worksheets/sheet1.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>"
                              "<Override PartName=\"/xl/worksheets/sheet2.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>"
                              "<Override PartName=\"/xl/styles.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml\"/></Types>"},
      {"_rels/.rels", std::string(H) + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
                      "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"xl/workbook.xml\"/></Relationships>"},
      {"xl/workbook.xml", std::string(H) + "<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" "
                          "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\"><sheets><sheet name=\"Sessions log\" sheetId=\"1\" r:id=\"rId1\"/>"
                          "<sheet name=\"Progress\" sheetId=\"2\" r:id=\"rId2\"/></sheets></workbook>"},
      {"xl/_rels/workbook.xml.rels", std::string(H) + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
                                     "<Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" Target=\"worksheets/sheet1.xml\"/>"
                                     "<Relationship Id=\"rId2\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" Target=\"worksheets/sheet2.xml\"/>"
                                     "<Relationship Id=\"rId3\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" Target=\"styles.xml\"/></Relationships>"},
      {"xl/styles.xml", std::string(H) + "<styleSheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
                        "<fonts count=\"2\"><font><sz val=\"11\"/><name val=\"Calibri\"/></font><font><b/><sz val=\"11\"/><color rgb=\"FFFFFFFF\"/><name val=\"Calibri\"/></font></fonts>"
                        "<fills count=\"3\"><fill><patternFill patternType=\"none\"/></fill><fill><patternFill patternType=\"gray125\"/></fill>"
                        "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FF1E293B\"/><bgColor indexed=\"64\"/></patternFill></fill></fills>"
                        "<borders count=\"1\"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count=\"1\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\"/></cellStyleXfs>"
                        "<cellXfs count=\"2\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\" xfId=\"0\"/><xf numFmtId=\"0\" fontId=\"1\" fillId=\"2\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" applyFill=\"1\"/></cellXfs></styleSheet>"},
      {"xl/worksheets/sheet1.xml", Sheet(a, {7, 7, 24, 12, 8, 8, 13, 12, 10, 9, 11, 11, 11, 11, 18})},
      {"xl/worksheets/sheet2.xml", Sheet(b, {7, 24, 8, 11, 8, 11, 15, 14})},
  };
  std::wstring path = SOPrepDir() + L"\\SO_Study_Log.xlsx";
  if (!WriteZip(path, files)) {  // file open in Excel → write a timestamped copy
    SYSTEMTIME t; GetLocalTime(&t);
    path = SOPrepDir() + Fmt(L"\\SO_Study_Log_%02d%02d%02d.xlsx", t.wHour, t.wMinute, t.wSecond);
    if (!WriteZip(path, files)) { g_lastXlsx.clear(); return false; }
  }
  g_lastXlsx = path;
  return true;
}

// ───────────────────────── fonts & drawing ─────────────────────────
static double Sc() { return g_dpi / 96.0 * S.zoom; }
static int Px(double v) { return (int)std::lround(v * Sc()); }
static int Height() { return Px(56); }
static int D(int v) { return MulDiv(v, g_dpi, 96); }
static Cat& C() { return S.cats[S.cur]; }
struct Fonts { HFONT big = 0, title = 0, small = 0, tiny = 0; int key = 0; } F;
static HFONT MakeFont(int px, int weight) {
  HFONT f = CreateFontW(-px, 0, 0, 0, weight, 0, 0, 0, DEFAULT_CHARSET, OUT_TT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, DEFAULT_PITCH, L"Segoe UI Variable Display");
  LOGFONTW lf{};
  GetObjectW(f, sizeof lf, &lf);
  if (wcscmp(lf.lfFaceName, L"Segoe UI Variable Display") != 0) {
    DeleteObject(f);
    f = CreateFontW(-px, 0, 0, 0, weight, 0, 0, 0, DEFAULT_CHARSET, OUT_TT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, DEFAULT_PITCH, L"Segoe UI");
  }
  return f;
}
static void EnsureFonts() {
  int key = (int)std::lround(Sc() * 1000);
  if (F.key == key) return;
  for (HFONT f : {F.big, F.title, F.small, F.tiny}) if (f) DeleteObject(f);
  F.big = MakeFont(Px(20), FW_SEMIBOLD); F.title = MakeFont(Px(13.5), FW_SEMIBOLD); F.small = MakeFont(Px(11.5), FW_NORMAL); F.tiny = MakeFont(Px(10.5), FW_SEMIBOLD);
  F.key = key;
}
struct ISize { int cx, cy; };
static ISize TextSize(HDC dc, HFONT f, const std::wstring& s) {
  HGDIOBJ o = SelectObject(dc, f);
  RECT r{0, 0, 4000, 200};
  DrawTextW(dc, s.c_str(), (int)s.size(), &r, DT_CALCRECT | DT_SINGLELINE | DT_NOPREFIX);
  SelectObject(dc, o);
  return {(int)(r.right - r.left), (int)(r.bottom - r.top)};
}
static void Text(HDC dc, HFONT f, const std::wstring& s, RECT r, COLORREF c, UINT fmt) {
  HGDIOBJ o = SelectObject(dc, f);
  SetTextColor(dc, c);
  SetBkMode(dc, TRANSPARENT);
  DrawTextW(dc, s.c_str(), (int)s.size(), &r, fmt | DT_SINGLELINE | DT_NOPREFIX | DT_VCENTER);
  SelectObject(dc, o);
}
static void RoundRect(Gdiplus::Graphics& g, Gdiplus::Brush* b, float x, float y, float w, float h, float rad) {
  float d = std::min({rad * 2, w, h});
  if (d <= 0) return;
  Gdiplus::GraphicsPath p;
  p.AddArc(x, y, d, d, 180, 90); p.AddArc(x + w - d, y, d, d, 270, 90); p.AddArc(x + w - d, y + h - d, d, d, 0, 90); p.AddArc(x, y + h - d, d, d, 90, 90);
  p.CloseFigure();
  g.FillPath(b, &p);
}
static void IconReset(Gdiplus::Graphics& g, COLORREF c, float cx, float cy, float r) {
  Gdiplus::Pen p(GC(c), r * 0.3f);
  p.SetStartCap(Gdiplus::LineCapRound);
  g.DrawArc(&p, cx - r, cy - r, 2 * r, 2 * r, -30.0f, 290.0f);
  Gdiplus::SolidBrush b(GC(c));
  float ax = cx + r * 0.87f, ay = cy - r * 0.5f;
  Gdiplus::PointF tri[3] = {{ax - r * 0.55f, ay - r * 0.2f}, {ax + r * 0.5f, ay - r * 0.55f}, {ax + r * 0.2f, ay + r * 0.55f}};
  g.FillPolygon(&b, tri, 3);
}
static void IconCheck(Gdiplus::Graphics& g, COLORREF c, float cx, float cy, float r) {
  Gdiplus::Pen p(GC(c), r * 0.32f);
  p.SetStartCap(Gdiplus::LineCapRound); p.SetEndCap(Gdiplus::LineCapRound); p.SetLineJoin(Gdiplus::LineJoinRound);
  Gdiplus::PointF pts[3] = {{cx - r * 0.8f, cy + r * 0.05f}, {cx - r * 0.2f, cy + r * 0.65f}, {cx + r * 0.85f, cy - r * 0.6f}};
  g.DrawLines(&p, pts, 3);
}

// ───────────────────────── widget ─────────────────────────
enum Hit { H_NONE, H_DRAG, H_NAME, H_MINUS, H_PLUS, H_DONE, H_TARGET, H_PLAY, H_TIME, H_RESET, H_END, H_ROUND, H_MENU, H_CHIP, H_TOTAL };
struct Zone { Hit hit; RECT r; int idx; };
static std::vector<Zone> g_zones;
static bool In(const RECT& r, POINT p) { return p.x >= r.left && p.x < r.right && p.y >= r.top && p.y < r.bottom; }
static const Zone* ZoneAt(POINT p) { for (auto it = g_zones.rbegin(); it != g_zones.rend(); ++it) if (In(it->r, p)) return &*it; return nullptr; }
static bool Hover(const RECT& r) { return In(r, g_mouse); }

static void Paint(HWND hwnd, HDC hdc) {
  RECT rc;
  GetClientRect(hwnd, &rc);
  int W = rc.right, H = rc.bottom;
  if (W <= 0 || H <= 0) return;
  EnsureFonts();
  const Theme& T = THEMES[S.theme];
  bool light = S.theme == 3;
  COLORREF ink = light ? RGB(255, 255, 255) : RGB(8, 20, 30), white = light ? RGB(30, 41, 59) : RGB(226, 232, 240);
  HDC mem = CreateCompatibleDC(hdc);
  HBITMAP bmp = CreateCompatibleBitmap(hdc, W, H);
  HGDIOBJ oldBmp = SelectObject(mem, bmp);
  g_zones.clear();

  Cat& c = C();
  COLORREF acc = CatColor(S.cur);
  bool complete = c.done >= c.target, active = SS.active && SS.cat == S.cur;
  COLORREF ring = complete ? GOLD : acc;
  double frac = std::clamp((double)c.done / c.target, 0.0, 1.0), tfrac = TotalFrac();
  int mid = H / 2, pad = Px(12), gap = Px(16);
  double pace = active && SS.secs >= 180 && c.done > SS.startDone ? (c.done - SS.startDone) / (SS.secs / 3600.0) : -1;
  int logged = 0; for (auto& r : g_log) if (r.round == S.round) logged++;

  std::wstring nameS = Fmt(L"#%d  %ls", S.cur + 1, c.name.c_str());
  std::wstring nameSub = Fmt(L"Round %d · %d sitting%ls logged", S.round, logged, logged == 1 ? L"" : L"s");
  std::wstring doneS = std::to_wstring(c.done), targetS = Fmt(L"/ %d", c.target), leftS = complete ? L"all pages done!" : Fmt(L"%d left", c.target - c.done);
  std::wstring timeS = c.mins ? HMS(c.rem) : L"--:--";
  std::wstring timeSub = !c.mins ? L"click time to set" : Fmt(L"of %ls", Mins(c.mins).c_str()) + (pace > 0 ? Fmt(L" · %.0f p/h", pace) : g_running ? L" · reading" : active ? L" · paused" : L" · ready");
  std::wstring totS = Fmt(L"%d%%", (int)std::lround(tfrac * 100)), totSub = Fmt(L"Total · %d / %d pages", TotalDone(), TotalTarget());
  std::wstring roundS = Fmt(L"Finish round %d", S.round);

  int ringW = H - Px(12), btnD = Px(24), smallD = Px(22);
  int nameW = std::clamp(std::max(TextSize(mem, F.title, nameS).cx + Px(30), TextSize(mem, F.small, nameSub).cx), Px(120), Px(230));
  int numW = TextSize(mem, F.big, doneS).cx + Px(4) + TextSize(mem, F.small, targetS).cx;
  int pagesW = std::max(numW, TextSize(mem, F.small, leftS).cx) + 2 * btnD + Px(14);
  int timeTxtW = std::max(TextSize(mem, F.big, L"0:00:00").cx, TextSize(mem, F.small, timeSub).cx);
  int timerW = btnD + Px(8) + timeTxtW + Px(8) + 2 * smallD + Px(4);
  int totW = std::min(std::max(TextSize(mem, F.title, totS).cx + Px(8) + TextSize(mem, F.tiny, S.title).cx, TextSize(mem, F.small, totSub).cx), Px(240));
  int roundW = TextSize(mem, F.tiny, roundS).cx + Px(34), menuW = Px(26), avail = W - pad - menuW - Px(6);

  int x = pad + ringW + gap;
  bool showName = true, showTimer = true, showTot = false, showRound = false, showChips = false;
  int need = x + nameW + gap + pagesW + gap + timerW;
  if (need > avail) { showName = false; need -= nameW + gap; }
  if (need > avail) { showTimer = false; need -= timerW + gap; }
  if (need + gap + totW <= avail) { showTot = true; need += gap + totW; }
  if (need + gap + roundW <= avail) { showRound = true; need += gap + roundW; }
  int chipsX = need + gap;
  if (S.cats.size() > 1 && avail - chipsX > Px(110)) showChips = true;
  int xName = x, xPages = showName ? x + nameW + gap : x, xTimer = xPages + pagesW + gap, xTot = xTimer + (showTimer ? timerW + gap : 0);
  int xRound = xTot + (showTot ? totW + gap : 0);
  RECT minus{xPages, mid - btnD / 2, xPages + btnD, mid + btnD / 2}, plus{xPages + pagesW - btnD, mid - btnD / 2, xPages + pagesW, mid + btnD / 2};
  RECT play{xTimer, mid - btnD / 2, xTimer + btnD, mid + btnD / 2};
  int xIcons = xTimer + btnD + Px(8) + timeTxtW + Px(8);
  RECT reset{xIcons, mid - smallD / 2, xIcons + smallD, mid + smallD / 2}, endb{xIcons + smallD + Px(4), mid - smallD / 2, xIcons + 2 * smallD + Px(4), mid + smallD / 2};
  RECT roundR{xRound, mid - Px(13), xRound + roundW, mid + Px(13)};
  RECT menuR{W - pad - menuW + Px(4), mid - Px(13), W - pad + Px(4), mid + Px(13)};

  {
    Gdiplus::Graphics g(mem);
    g.SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);
    g.SetPixelOffsetMode(Gdiplus::PixelOffsetModeHalf);
    Gdiplus::LinearGradientBrush bg(Gdiplus::Point(0, 0), Gdiplus::Point(W, H), GC(T.bg1), GC(T.bg2));
    g.FillRectangle(&bg, 0, 0, W, H);
    Gdiplus::LinearGradientBrush glow(Gdiplus::Point(0, 0), Gdiplus::Point(Px(180), 0), GC(acc, light ? 30 : 42), GC(acc, 0));
    g.FillRectangle(&glow, 0, 0, Px(180), H);
    if (!light) { Gdiplus::SolidBrush hi(GC(RGB(255, 255, 255), 16)); g.FillRectangle(&hi, 0, 0, W, 1); }
    Gdiplus::Pen sep(GC(T.line), 1.0f);
    auto vsep = [&](int sx) { g.DrawLine(&sep, (float)sx, (float)(mid - Px(15)), (float)sx, (float)(mid + Px(15))); };
    if (showName) vsep(xPages - gap / 2);
    if (showTimer) vsep(xTimer - gap / 2);
    if (showTot) vsep(xTot - gap / 2);
    // rings: outer = total, inner = this session
    float rx = (float)pad, ry = (float)(mid - ringW / 2), rw = (float)ringW, po = (float)Px(2.6), pi = (float)Px(4.2), inset = po + (float)Px(2.4);
    Gdiplus::Pen trO(GC(T.track), po), trI(GC(T.track), pi);
    g.DrawEllipse(&trO, rx + po / 2, ry + po / 2, rw - po, rw - po);
    g.DrawEllipse(&trI, rx + inset + pi / 2, ry + inset + pi / 2, rw - 2 * inset - pi, rw - 2 * inset - pi);
    if (tfrac > 0) {
      Gdiplus::Pen p(GC(white), po);
      p.SetStartCap(Gdiplus::LineCapRound); p.SetEndCap(Gdiplus::LineCapRound);
      g.DrawArc(&p, rx + po / 2, ry + po / 2, rw - po, rw - po, -90.0f, (float)std::max(tfrac * 360, 2.0));
    }
    if (frac > 0) {
      Gdiplus::Pen p(GC(ring), pi);
      p.SetStartCap(Gdiplus::LineCapRound); p.SetEndCap(Gdiplus::LineCapRound);
      g.DrawArc(&p, rx + inset + pi / 2, ry + inset + pi / 2, rw - 2 * inset - pi, rw - 2 * inset - pi, -90.0f, (float)std::max(frac * 360, 2.0));
    }
    if (showName) {
      Gdiplus::SolidBrush dot(GC(acc));
      g.FillEllipse(&dot, (float)xName, (float)(mid - Px(13)), (float)Px(7), (float)Px(7));
      int tw = std::min(TextSize(mem, F.title, nameS).cx, nameW - Px(30));
      float cx = (float)(xName + Px(12) + tw + Px(7)), cy = (float)(mid - Px(9));
      Gdiplus::Pen chev(GC(T.muted), (float)Px(1.6));
      chev.SetStartCap(Gdiplus::LineCapRound); chev.SetEndCap(Gdiplus::LineCapRound);
      g.DrawLine(&chev, cx, cy - Px(1.5), cx + Px(3.5), cy + Px(2));
      g.DrawLine(&chev, cx + Px(3.5), cy + Px(2), cx + Px(7), cy - Px(1.5));
    }
    for (RECT* r : {&minus, &plus}) {
      bool hv = Hover(*r), dis = (r == &plus && complete) || (r == &minus && c.done == 0);
      COLORREF col = r == &plus ? (dis ? T.btn : hv ? Mix(acc, RGB(255, 255, 255), 0.18) : acc) : (hv && !dis ? T.btnHover : T.btn);
      Gdiplus::SolidBrush b(GC(col));
      g.FillEllipse(&b, (float)r->left, (float)r->top, (float)btnD, (float)btnD);
      Gdiplus::Pen p(GC(r == &plus && !dis ? ink : (dis ? T.track : T.text)), (float)Px(2));
      p.SetStartCap(Gdiplus::LineCapRound); p.SetEndCap(Gdiplus::LineCapRound);
      float cx = r->left + btnD / 2.0f, cy = r->top + btnD / 2.0f, a = (float)Px(5);
      g.DrawLine(&p, cx - a, cy, cx + a, cy);
      if (r == &plus) g.DrawLine(&p, cx, cy - a, cx, cy + a);
    }
    float bx = (float)(minus.right + Px(7)), bw = (float)(plus.left - Px(7)) - bx, by = (float)(H - Px(9)), bh = (float)Px(3.2);
    Gdiplus::SolidBrush tb(GC(T.track));
    RoundRect(g, &tb, bx, by, bw, bh, bh / 2);
    if (frac > 0) {
      Gdiplus::LinearGradientBrush pb(Gdiplus::PointF(bx, 0), Gdiplus::PointF(bx + bw + 1, 0), GC(ring), GC(Mix(ring, RGB(255, 255, 255), 0.35)));
      RoundRect(g, &pb, bx, by, (float)std::max(bw * frac, (double)bh), bh, bh / 2);
    }
    if (showTimer) {
      bool hv = Hover(play), dis = c.mins == 0;
      Gdiplus::SolidBrush pbb(GC(g_running ? acc : (hv ? T.btnHover : T.btn)));
      g.FillEllipse(&pbb, (float)play.left, (float)play.top, (float)btnD, (float)btnD);
      Gdiplus::SolidBrush gb(GC(g_running ? ink : (dis ? T.muted : T.text)));
      float cx = play.left + btnD / 2.0f, cy = play.top + btnD / 2.0f, s = (float)Px(4.6);
      if (g_running) { g.FillRectangle(&gb, cx - s * 0.85f, cy - s, s * 0.6f, 2 * s); g.FillRectangle(&gb, cx + s * 0.25f, cy - s, s * 0.6f, 2 * s); }
      else { Gdiplus::PointF tri[3] = {{cx - s * 0.55f, cy - s}, {cx - s * 0.55f, cy + s}, {cx + s, cy}}; g.FillPolygon(&gb, tri, 3); }
      for (RECT* r : {&reset, &endb}) {
        bool h2 = Hover(*r);
        Gdiplus::SolidBrush hb(GC(h2 ? T.btnHover : T.btn));
        g.FillEllipse(&hb, (float)r->left, (float)r->top, (float)smallD, (float)smallD);
        float ix = r->left + smallD / 2.0f, iy = r->top + smallD / 2.0f, ir = (float)Px(5.2);
        if (r == &reset) IconReset(g, h2 ? T.text : T.muted, ix, iy, ir);
        else IconCheck(g, active ? (h2 ? GOLD : acc) : T.track, ix, iy, ir);
      }
      if (c.mins) {  // thin countdown bar under the time
        float tx = (float)(play.right + Px(8)), tw = (float)timeTxtW;
        RoundRect(g, &tb, tx, by, tw, bh, bh / 2);
        double tf = std::clamp((double)c.rem / (c.mins * 60.0), 0.0, 1.0);
        Gdiplus::SolidBrush cb(GC(c.rem <= 300 ? GOLD : acc));
        if (tf > 0) RoundRect(g, &cb, tx, by, (float)std::max(tw * tf, (double)bh), bh, bh / 2);
      }
    }
    if (showTot) {
      float tx = (float)xTot, tw = (float)totW;
      RoundRect(g, &tb, tx, by, tw, bh, bh / 2);
      Gdiplus::SolidBrush wb(GC(white));
      if (tfrac > 0) RoundRect(g, &wb, tx, by, (float)std::max(tw * tfrac, (double)bh), bh, bh / 2);
    }
    if (showRound) {
      bool hv = Hover(roundR);
      Gdiplus::SolidBrush rb(GC(hv ? Mix(GOLD, RGB(255, 255, 255), 0.2) : (light ? RGB(254, 243, 199) : RGB(64, 54, 18))));
      RoundRect(g, &rb, (float)roundR.left, (float)roundR.top, (float)roundW, (float)(roundR.bottom - roundR.top), (float)Px(13));
      IconCheck(g, hv ? RGB(40, 30, 0) : (light ? RGB(146, 64, 14) : GOLD), (float)roundR.left + Px(14), (float)mid, (float)Px(4.5));
    }
    if (showChips) {
      int cx = chipsX, ch = Px(24), cy = mid - ch / 2;
      for (int i = 0; i < (int)S.cats.size(); i++) {
        if (i == S.cur) continue;
        const Cat& k = S.cats[i];
        std::wstring s = Fmt(L"#%d %ls  %d/%d", i + 1, k.name.c_str(), k.done, k.target);
        int w = TextSize(mem, F.tiny, s).cx + Px(24);
        if (cx + w > avail) break;
        RECT r{cx, cy, cx + w, cy + ch};
        Gdiplus::SolidBrush cb(GC(Hover(r) ? T.btnHover : T.btn));
        RoundRect(g, &cb, (float)r.left, (float)r.top, (float)w, (float)ch, ch / 2.0f);
        double f = std::clamp((double)k.done / k.target, 0.0, 1.0);
        Gdiplus::SolidBrush fb(GC(k.done >= k.target ? GOLD : CatColor(i), 70));
        if (f > 0) RoundRect(g, &fb, (float)r.left, (float)r.top, (float)std::max(w * f, (double)ch), (float)ch, ch / 2.0f);
        Gdiplus::SolidBrush dot(GC(CatColor(i)));
        g.FillEllipse(&dot, (float)r.left + Px(8), (float)mid - Px(3), (float)Px(6), (float)Px(6));
        g_zones.push_back({H_CHIP, r, i});
        cx += w + Px(6);
      }
    }
    if (Hover(menuR)) { Gdiplus::SolidBrush hb(GC(T.btnHover)); RoundRect(g, &hb, (float)menuR.left, (float)menuR.top, (float)(menuR.right - menuR.left), (float)(menuR.bottom - menuR.top), (float)Px(7)); }
    Gdiplus::SolidBrush db(GC(T.muted));
    for (int i = -1; i <= 1; i++) g.FillEllipse(&db, (menuR.left + menuR.right) / 2.0f - Px(1.7), (float)(mid + i * Px(5.5) - Px(1.7)), (float)Px(3.4), (float)Px(3.4));
  }

  RECT ringR{pad, mid - ringW / 2, pad + ringW, mid + ringW / 2};
  Text(mem, F.tiny, Fmt(L"%d%%", (int)std::lround(frac * 100)), ringR, complete ? GOLD : T.text, DT_CENTER);
  g_zones.push_back({H_DRAG, ringR, 0});
  if (showName) {
    RECT tr{xName + Px(12), mid - Px(22), xName + Px(12) + std::min(TextSize(mem, F.title, nameS).cx, nameW - Px(30)), mid + Px(1)};
    Text(mem, F.title, nameS, tr, T.text, DT_LEFT | DT_END_ELLIPSIS);
    RECT sr{xName, mid + Px(1), xName + nameW, mid + Px(19)};
    Text(mem, F.small, nameSub, sr, T.muted, DT_LEFT | DT_END_ELLIPSIS);
    g_zones.push_back({H_NAME, {xName, mid - Px(22), xName + nameW, mid + Px(20)}, 0});
  }
  {
    int inner = plus.left - minus.right;
    ISize dsz = TextSize(mem, F.big, doneS), tsz = TextSize(mem, F.small, targetS);
    int nx = minus.right + (inner - (dsz.cx + Px(4) + tsz.cx)) / 2;
    RECT dr{nx, mid - Px(24), nx + dsz.cx, mid + Px(2)};
    Text(mem, F.big, doneS, dr, complete ? GOLD : T.text, DT_LEFT);
    RECT trr{dr.right + Px(4), mid - Px(20), dr.right + Px(4) + tsz.cx, mid + Px(1)};
    Text(mem, F.small, targetS, trr, Hover(trr) ? T.text : T.muted, DT_LEFT);
    RECT lr{minus.right, mid + Px(1), plus.left, mid + Px(17)};
    Text(mem, F.small, leftS, lr, complete ? GOLD : T.muted, DT_CENTER);
    g_zones.push_back({H_MINUS, minus, 0}); g_zones.push_back({H_PLUS, plus, 0});
    g_zones.push_back({H_DONE, dr, 0}); g_zones.push_back({H_TARGET, trr, 0});
  }
  if (showTimer) {
    int tx = play.right + Px(8);
    RECT tr{tx, mid - Px(24), tx + timeTxtW, mid + Px(2)};
    bool warn = c.mins && c.rem <= 300;
    Text(mem, F.big, timeS, tr, warn ? GOLD : (g_running || Hover(tr)) ? T.text : T.muted, DT_LEFT);
    RECT sr{tx, mid + Px(1), tx + timeTxtW, mid + Px(17)};
    Text(mem, F.small, timeSub, sr, T.muted, DT_LEFT);
    g_zones.push_back({H_PLAY, play, 0}); g_zones.push_back({H_TIME, {tx, mid - Px(24), tx + timeTxtW, mid + Px(18)}, 0});
    g_zones.push_back({H_RESET, reset, 0}); g_zones.push_back({H_END, endb, 0});
  }
  if (showTot) {
    int tw = TextSize(mem, F.title, totS).cx;
    RECT pr{xTot, mid - Px(23), xTot + tw, mid + Px(1)};
    Text(mem, F.title, totS, pr, T.text, DT_LEFT);
    RECT lr{xTot + tw + Px(8), mid - Px(22), xTot + totW, mid};
    Text(mem, F.tiny, S.title, lr, T.muted, DT_LEFT | DT_END_ELLIPSIS);
    RECT sr{xTot, mid + Px(1), xTot + totW, mid + Px(17)};
    Text(mem, F.small, totSub, sr, T.muted, DT_LEFT | DT_END_ELLIPSIS);
    g_zones.push_back({H_TOTAL, {xTot, mid - Px(22), xTot + totW, mid + Px(20)}, 0});
  }
  if (showRound) {
    RECT tr{roundR.left + Px(24), roundR.top, roundR.right - Px(8), roundR.bottom};
    Text(mem, F.tiny, roundS, tr, Hover(roundR) ? RGB(40, 30, 0) : (light ? RGB(146, 64, 14) : GOLD), DT_LEFT);
    g_zones.push_back({H_ROUND, roundR, 0});
  }
  for (auto& z : g_zones)
    if (z.hit == H_CHIP) {
      RECT r = z.r;
      r.left += Px(19);
      const Cat& k = S.cats[z.idx];
      Text(mem, F.tiny, Fmt(L"#%d %ls  %d/%d", z.idx + 1, k.name.c_str(), k.done, k.target), r, T.text, DT_LEFT);
    }
  g_zones.push_back({H_MENU, menuR, 0});
  BitBlt(hdc, 0, 0, W, H, mem, 0, 0, SRCCOPY);
  SelectObject(mem, oldBmp);
  DeleteObject(bmp);
  DeleteDC(mem);
}

// ───────────────────────── dialogs ─────────────────────────
static bool g_modalDone = false, g_modalOk = false;
typedef void (*CmdFn)(int);
static CmdFn g_dlgCmd = nullptr;
static LRESULT CALLBACK DlgProc(HWND h, UINT m, WPARAM w, LPARAM l) {
  switch (m) {
    case WM_COMMAND:
      if (LOWORD(w) == IDOK) { g_modalOk = true; g_modalDone = true; return 0; }
      if (LOWORD(w) == IDCANCEL) { g_modalOk = false; g_modalDone = true; return 0; }
      if (g_dlgCmd && HIWORD(w) == BN_CLICKED) g_dlgCmd(LOWORD(w));
      return 0;
    case WM_CLOSE: g_modalOk = false; g_modalDone = true; return 0;
  }
  return DefWindowProcW(h, m, w, l);
}
static HFONT UiFont() { static HFONT f = nullptr; static int k = 0; if (!f || k != g_dpi) { if (f) DeleteObject(f); f = MakeFont(MulDiv(14, g_dpi, 96), FW_NORMAL); k = g_dpi; } return f; }
static HWND Ctl(const wchar_t* cls, const wchar_t* txt, DWORD style, int x, int y, int w, int h, HWND parent, int id) {
  HWND c = CreateWindowExW(0, cls, txt, WS_CHILD | WS_VISIBLE | style, D(x), D(y), D(w), D(h), parent, (HMENU)(INT_PTR)id, g_inst, nullptr);
  SendMessageW(c, WM_SETFONT, (WPARAM)UiFont(), TRUE);
  return c;
}
static HWND MakeDialog(const wchar_t* title, int w, int hgt) {
  static bool reg = false;
  if (!reg) {
    WNDCLASSW wc{};
    wc.lpfnWndProc = DlgProc; wc.hInstance = g_inst; wc.lpszClassName = L"SOSprintDlg"; wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1); wc.hIcon = LoadIconW(g_inst, MAKEINTRESOURCEW(IDI_APP));
    RegisterClassW(&wc);
    reg = true;
  }
  RECT r{0, 0, D(w), D(hgt)};
  AdjustWindowRectEx(&r, WS_CAPTION | WS_SYSMENU, FALSE, WS_EX_DLGMODALFRAME);
  RECT wr; GetWindowRect(g_hwnd, &wr);
  MONITORINFO mi{sizeof mi};
  GetMonitorInfoW(MonitorFromWindow(g_hwnd, MONITOR_DEFAULTTONEAREST), &mi);
  int ww = r.right - r.left, hh = r.bottom - r.top;
  int x = std::clamp((int)wr.left, (int)mi.rcWork.left, std::max((int)mi.rcWork.left, (int)mi.rcWork.right - ww)), y = wr.bottom + D(8);
  if (y + hh > mi.rcWork.bottom) y = std::max((int)mi.rcWork.top, (int)wr.top - hh - D(8));
  return CreateWindowExW(WS_EX_DLGMODALFRAME | WS_EX_TOPMOST, L"SOSprintDlg", title, WS_CAPTION | WS_SYSMENU, x, y, ww, hh, g_hwnd, nullptr, g_inst, nullptr);
}
static void RunModal(HWND dlg) {
  EnableWindow(g_hwnd, FALSE);
  g_modalDone = false;
  MSG msg;
  while (!g_modalDone && GetMessageW(&msg, nullptr, 0, 0)) {
    if (msg.message == WM_KEYDOWN && (msg.wParam == VK_ESCAPE || msg.wParam == VK_RETURN) && (msg.hwnd == dlg || IsChild(dlg, msg.hwnd))) {
      g_modalOk = msg.wParam == VK_RETURN;
      break;
    }
    if (!IsDialogMessageW(dlg, &msg)) { TranslateMessage(&msg); DispatchMessageW(&msg); }
  }
  EnableWindow(g_hwnd, TRUE);
}
static std::wstring GetText(HWND e) { int n = GetWindowTextLengthW(e); std::wstring s(n, L'\0'); GetWindowTextW(e, s.data(), n + 1); return s; }
static bool Ask(const std::wstring& title, const std::wstring& label, std::wstring& value, bool numeric) {
  HWND dlg = MakeDialog(title.c_str(), 360, 122);
  g_dlgCmd = nullptr;
  Ctl(L"STATIC", label.c_str(), 0, 14, 12, 332, 20, dlg, 0);
  HWND e = Ctl(L"EDIT", value.c_str(), WS_BORDER | WS_TABSTOP | ES_AUTOHSCROLL | (numeric ? ES_NUMBER : 0), 14, 36, 332, 28, dlg, 10);
  Ctl(L"BUTTON", L"Save", WS_TABSTOP | BS_DEFPUSHBUTTON, 174, 80, 84, 30, dlg, IDOK);
  Ctl(L"BUTTON", L"Cancel", WS_TABSTOP, 262, 80, 84, 30, dlg, IDCANCEL);
  ShowWindow(dlg, SW_SHOW);
  SetForegroundWindow(dlg);
  SetFocus(e);
  SendMessageW(e, EM_SETSEL, 0, -1);
  g_modalOk = false;
  RunModal(dlg);
  std::wstring v = GetText(e);
  DestroyWindow(dlg);
  if (g_modalOk) value = v;
  return g_modalOk;
}

// ───────────────────────── reports ─────────────────────────
static Gdiplus::FontFamily* g_ff = nullptr;
static Gdiplus::FontFamily& FF() {
  if (!g_ff) {
    g_ff = new Gdiplus::FontFamily(L"Segoe UI");
    if (!g_ff->IsAvailable()) { delete g_ff; g_ff = Gdiplus::FontFamily::GenericSansSerif()->Clone(); }
  }
  return *g_ff;
}
static void DS(Gdiplus::Graphics& g, const std::wstring& s, float x, float y, float size, COLORREF c, bool bold = false, float w = 0, int align = 0) {
  Gdiplus::Font f(&FF(), size, bold ? Gdiplus::FontStyleBold : Gdiplus::FontStyleRegular, Gdiplus::UnitPixel);
  Gdiplus::SolidBrush b(GC(c));
  Gdiplus::StringFormat sf;
  sf.SetTrimming(Gdiplus::StringTrimmingEllipsisCharacter);
  sf.SetFormatFlags(Gdiplus::StringFormatFlagsNoWrap);
  if (align == 1) sf.SetAlignment(Gdiplus::StringAlignmentCenter);
  Gdiplus::RectF r(x, y, w > 0 ? w : 2000.0f, size * 1.6f);
  g.DrawString(s.c_str(), -1, &f, r, &sf, &b);
}
static void Bar(Gdiplus::Graphics& g, float x, float y, float w, float h, double f, COLORREF track, COLORREF fill) {
  Gdiplus::SolidBrush t(GC(track)), b(GC(fill));
  RoundRect(g, &t, x, y, w, h, h / 2);
  if (f > 0) RoundRect(g, &b, x, y, (float)std::max(w * std::clamp(f, 0.0, 1.0), (double)h), h, h / 2);
}
static void Ring(Gdiplus::Graphics& g, float x, float y, float d, float pw, double f, COLORREF track, COLORREF fill) {
  Gdiplus::Pen t(GC(track), pw), p(GC(fill), pw);
  p.SetStartCap(Gdiplus::LineCapRound); p.SetEndCap(Gdiplus::LineCapRound);
  g.DrawEllipse(&t, x + pw / 2, y + pw / 2, d - pw, d - pw);
  if (f > 0) g.DrawArc(&p, x + pw / 2, y + pw / 2, d - pw, d - pw, -90.0f, (float)std::max(std::min(f, 1.0) * 360, 2.0));
}
static Gdiplus::Bitmap* RenderSessionCard(const LogRow& r) {
  int W = 600, H = 316;
  auto* bmp = new Gdiplus::Bitmap(W, H, PixelFormat32bppARGB);
  Gdiplus::Graphics g(bmp);
  g.SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);
  g.SetTextRenderingHint(Gdiplus::TextRenderingHintAntiAliasGridFit);
  const Theme& T = THEMES[0];
  Gdiplus::LinearGradientBrush bg(Gdiplus::Point(0, 0), Gdiplus::Point(W, H), GC(T.bg1), GC(T.bg2));
  g.FillRectangle(&bg, 0, 0, W, H);
  COLORREF acc = CatColor(r.serial - 1);
  Gdiplus::SolidBrush band(GC(acc));
  g.FillRectangle(&band, 0, 0, 6, H);
  bool done = r.status == L"Completed";
  DS(g, done ? L"SESSION COMPLETE" : L"SESSION SAVED", 30, 22, 13, done ? acc : GOLD, true);
  DS(g, Fmt(L"#%d  %ls", r.serial, r.name.c_str()), 30, 42, 26, T.text, true, 400);
  DS(g, Fmt(L"Round %d  ·  %ls  ·  %ls – %ls  ·  %ls", r.round, r.date.c_str(), r.start.c_str(), r.end.c_str(), r.status.c_str()), 30, 82, 14, T.muted, false, W - 60.0f);
  Ring(g, W - 118.0f, 24, 84, 9, r.target ? (double)r.p1 / r.target : 0, T.track, r.p1 >= r.target ? GOLD : acc);
  DS(g, Fmt(L"%d%%", r.target ? (int)std::lround(100.0 * r.p1 / r.target) : 0), W - 118.0f, 52, 20, T.text, true, 84, 1);
  double am = r.actualSec / 60.0;
  int pr = r.p1 - r.p0;
  std::wstring big[4] = {std::to_wstring(pr), Mins(am), am >= 1 ? Fmt(L"%.0f", pr / (am / 60)) : L"–", Fmt(L"%d", r.target - r.p1)};
  std::wstring small[4] = {Fmt(L"pages read (p. %d → %d)", r.p0, r.p1), Fmt(L"read (planned %ls)", Mins(r.planned).c_str()), L"pages per hour", Fmt(L"pages left of %d", r.target)};
  for (int i = 0; i < 4; i++) {
    float tx = 30.0f + i * 138.0f, ty = 122;
    Gdiplus::SolidBrush tbr(GC(T.btn));
    RoundRect(g, &tbr, tx, ty, 128, 90, 12);
    DS(g, big[i], tx + 12, ty + 10, 28, T.text, true, 110);
    DS(g, small[i], tx + 12, ty + 56, 11, T.muted, false, 112);
  }
  DS(g, Fmt(L"Overall progress  %d / %d pages  (%d%%)", TotalDone(), TotalTarget(), (int)std::lround(TotalFrac() * 100)), 30, 228, 14, T.text, true);
  Bar(g, 30, 252, W - 60.0f, 8, TotalFrac(), T.track, RGB(226, 232, 240));
  DS(g, g_lastXlsx.empty() ? L"Excel log could not be written (close it in Excel and finish the next sitting)" : L"Logged in " + g_lastXlsx, 30, 274, 11, T.muted, false, W - 60.0f);
  DS(g, L"click to close", W - 120.0f, 294, 10, T.track, false, 100);
  return bmp;
}
static Gdiplus::Bitmap* g_card = nullptr;
static HWND g_cardWnd = nullptr;
static LRESULT CALLBACK CardProc(HWND h, UINT m, WPARAM w, LPARAM l) {
  switch (m) {
    case WM_PAINT: {
      PAINTSTRUCT ps;
      HDC dc = BeginPaint(h, &ps);
      if (g_card) { Gdiplus::Graphics g(dc); g.SetInterpolationMode(Gdiplus::InterpolationModeHighQualityBicubic); RECT rc; GetClientRect(h, &rc); g.DrawImage(g_card, 0, 0, rc.right, rc.bottom); }
      EndPaint(h, &ps);
      return 0;
    }
    case WM_LBUTTONUP: case WM_RBUTTONUP: case WM_TIMER: DestroyWindow(h); return 0;
    case WM_DESTROY: if (g_cardWnd == h) g_cardWnd = nullptr; return 0;
  }
  return DefWindowProcW(h, m, w, l);
}
static void ShowCard(Gdiplus::Bitmap* bmp, int seconds) {
  static bool reg = false;
  if (!reg) { WNDCLASSW wc{}; wc.lpfnWndProc = CardProc; wc.hInstance = g_inst; wc.lpszClassName = L"SOSprintCard"; wc.hCursor = LoadCursor(nullptr, IDC_HAND); RegisterClassW(&wc); reg = true; }
  if (g_cardWnd) DestroyWindow(g_cardWnd);
  delete g_card;
  g_card = bmp;
  int w = D((int)bmp->GetWidth()), hh = D((int)bmp->GetHeight());
  RECT wr; GetWindowRect(g_hwnd, &wr);
  MONITORINFO mi{sizeof mi};
  GetMonitorInfoW(MonitorFromWindow(g_hwnd, MONITOR_DEFAULTTONEAREST), &mi);
  int x = std::clamp((int)wr.left, (int)mi.rcWork.left, std::max((int)mi.rcWork.left, (int)mi.rcWork.right - w)), y = wr.bottom + D(8);
  if (y + hh > mi.rcWork.bottom) y = std::max((int)mi.rcWork.top, (int)wr.top - hh - D(8));
  g_cardWnd = CreateWindowExW(WS_EX_TOPMOST | WS_EX_TOOLWINDOW, L"SOSprintCard", L"Session report", WS_POPUP, x, y, w, hh, g_hwnd, nullptr, g_inst, nullptr);
  int corner = 2;
  DwmSetWindowAttribute(g_cardWnd, 33, &corner, sizeof corner);
  ShowWindow(g_cardWnd, SW_SHOWNOACTIVATE);
  SetTimer(g_cardWnd, 1, seconds * 1000, nullptr);
}
static bool JpegClsid(CLSID* clsid) {
  UINT n = 0, size = 0;
  Gdiplus::GetImageEncodersSize(&n, &size);
  if (!size) return false;
  std::vector<BYTE> buf(size);
  auto* info = (Gdiplus::ImageCodecInfo*)buf.data();
  Gdiplus::GetImageEncoders(n, size, info);
  for (UINT i = 0; i < n; i++) if (wcscmp(info[i].MimeType, L"image/jpeg") == 0) { *clsid = info[i].Clsid; return true; }
  return false;
}
static std::wstring RenderRoundReport() {
  struct Agg { int pages = 0, secs = 0, sittings = 0; };
  std::vector<Agg> agg(S.cats.size());
  int pagesRound = 0, secsRound = 0, sittings = 0;
  std::wstring first, last;
  for (auto& r : g_log) {
    if (r.round != S.round) continue;
    sittings++; pagesRound += r.p1 - r.p0; secsRound += r.actualSec;
    if (first.empty()) first = r.date + L" " + r.start;
    last = r.date + L" " + r.end;
    int i = r.serial - 1;
    if (i >= 0 && i < (int)agg.size() && S.cats[i].name == r.name) { agg[i].pages += r.p1 - r.p0; agg[i].secs += r.actualSec; agg[i].sittings++; }
  }
  int rows = (int)S.cats.size(), W = 1200, H = 340 + rows * 62 + 70;
  Gdiplus::Bitmap bmp(W, H, PixelFormat24bppRGB);
  Gdiplus::Graphics g(&bmp);
  g.SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);
  g.SetTextRenderingHint(Gdiplus::TextRenderingHintAntiAliasGridFit);
  const Theme& T = THEMES[0];
  Gdiplus::LinearGradientBrush bg(Gdiplus::Point(0, 0), Gdiplus::Point(W, H), GC(T.bg1), GC(T.bg2));
  g.FillRectangle(&bg, 0, 0, W, H);
  Gdiplus::LinearGradientBrush top(Gdiplus::Point(0, 0), Gdiplus::Point(W, 0), GC(RGB(52, 211, 153)), GC(RGB(56, 189, 248)));
  g.FillRectangle(&top, 0, 0, W, 8);
  SYSTEMTIME now; GetLocalTime(&now);
  DS(g, Fmt(L"ROUND %d REPORT", S.round), 48, 36, 16, RGB(52, 211, 153), true);
  DS(g, S.title, 48, 58, 40, T.text, true, 800);
  DS(g, Fmt(L"Saved %ls %ls   ·   %ls", DateS(now).c_str(), TimeS(now).c_str(), first.empty() ? L"no sittings logged this round" : (first + L"  →  " + last).c_str()), 48, 114, 16, T.muted, false, 840);
  Ring(g, W - 226.0f, 30, 160, 15, TotalFrac(), T.track, RGB(52, 211, 153));
  DS(g, Fmt(L"%d%%", (int)std::lround(TotalFrac() * 100)), W - 226.0f, 82, 36, T.text, true, 160, 1);
  DS(g, L"overall", W - 226.0f, 128, 13, T.muted, false, 160, 1);
  std::wstring big[4] = {std::to_wstring(pagesRound), Mins(secsRound / 60.0), std::to_wstring(sittings), Fmt(L"%d / %d", TotalDone(), TotalTarget())};
  std::wstring small[4] = {L"pages read this round", L"study time this round", L"sittings this round", L"total pages done"};
  for (int i = 0; i < 4; i++) {
    float tx = 48.0f + i * 228.0f, ty = 166;
    Gdiplus::SolidBrush tbr(GC(T.btn));
    RoundRect(g, &tbr, tx, ty, 212, 98, 14);
    DS(g, big[i], tx + 18, ty + 12, 32, T.text, true, 190);
    DS(g, small[i], tx + 18, ty + 64, 14, T.muted, false, 190);
  }
  float y = 296;
  DS(g, L"#", 48, y, 13, T.muted, true); DS(g, L"SESSION", 88, y, 13, T.muted, true); DS(g, L"PROGRESS", 390, y, 13, T.muted, true);
  DS(g, L"DONE / TOTAL", 760, y, 13, T.muted, true); DS(g, L"THIS ROUND", 930, y, 13, T.muted, true);
  y += 30;
  Gdiplus::Pen ln(GC(T.line), 1);
  for (int i = 0; i < rows; i++) {
    const Cat& c = S.cats[i];
    COLORREF col = c.done >= c.target ? GOLD : CatColor(i);
    g.DrawLine(&ln, 48.0f, y, W - 48.0f, y);
    Gdiplus::SolidBrush dot(GC(col));
    g.FillEllipse(&dot, 48.0f, y + 25.0f, 9.0f, 9.0f);
    DS(g, std::to_wstring(i + 1), 62, y + 16, 18, T.text, true);
    DS(g, c.name, 88, y + 16, 18, T.text, true, 290);
    Bar(g, 390, y + 25, 340, 10, (double)c.done / c.target, T.track, col);
    DS(g, Fmt(L"%d / %d  (%d%%)", c.done, c.target, (int)std::lround(100.0 * c.done / c.target)), 760, y + 17, 16, T.text, false, 165);
    DS(g, agg[i].sittings ? Fmt(L"+%d p · %ls · %d×", agg[i].pages, Mins(agg[i].secs / 60.0).c_str(), agg[i].sittings) : L"—", 930, y + 17, 16, agg[i].sittings ? T.text : T.muted, false, 230);
    y += 62;
  }
  g.DrawLine(&ln, 48.0f, y, W - 48.0f, y);
  DS(g, L"SO Written Prep  ·  SO Sprint Widget", 48, H - 44.0f, 13, T.muted);
  CLSID clsid;
  if (!JpegClsid(&clsid)) return L"";
  Gdiplus::EncoderParameters ep;
  ep.Count = 1;
  ep.Parameter[0].Guid = Gdiplus::EncoderQuality;
  ep.Parameter[0].Type = Gdiplus::EncoderParameterValueTypeLong;
  ep.Parameter[0].NumberOfValues = 1;
  ULONG q = 92;
  ep.Parameter[0].Value = &q;
  std::wstring path = SOPrepDir() + Fmt(L"\\Round_%02d_report_%04d-%02d-%02d_%02d%02d.jpg", S.round, now.wYear, now.wMonth, now.wDay, now.wHour, now.wMinute);
  return bmp.Save(path.c_str(), &clsid, &ep) == Gdiplus::Ok ? path : L"";
}

// ───────────────────────── session logic ─────────────────────────
static void Redraw() { InvalidateRect(g_hwnd, nullptr, FALSE); }
static void Changed() { Save(); Redraw(); }
static void BeginSession() { SS.active = true; SS.cat = S.cur; SS.startDone = C().done; SS.secs = 0; GetLocalTime(&SS.start); }
static void EndSession(const wchar_t* status, bool report = true) {
  if (!SS.active) return;
  g_running = false;
  Cat& c = S.cats[SS.cat];
  SYSTEMTIME now; GetLocalTime(&now);
  LogRow r;
  r.round = S.round; r.serial = SS.cat + 1; r.name = c.name; r.date = DateS(SS.start); r.start = TimeS(SS.start); r.end = TimeS(now);
  r.planned = c.mins; r.actualSec = (int)SS.secs; r.p0 = SS.startDone; r.p1 = c.done; r.target = c.target; r.status = status;
  SS.active = false;
  c.rem = c.mins * 60LL;
  if (r.actualSec >= 30 || r.p1 != r.p0) {
    AppendLog(r);
    WriteXlsx();
    if (report) ShowCard(RenderSessionCard(r), 30);
  }
  Changed();
}
static void SetTime();
static void StartPause() {
  if (C().mins == 0) { SetTime(); return; }
  if (!g_running) {
    if (C().rem <= 0) C().rem = C().mins * 60LL;
    if (!SS.active || SS.cat != S.cur) { if (SS.active) EndSession(L"Switched session", false); BeginSession(); }
    g_running = true;
    g_lastTick = GetTickCount64();
  } else g_running = false;
  Changed();
}
static void SetTime() {
  bool live = SS.active && SS.cat == S.cur;
  std::wstring v = std::to_wstring(C().mins ? C().mins : 60);
  std::wstring label = live ? Fmt(L"Total minutes for this sitting (%ls already used):", Mins((C().mins * 60.0 - C().rem) / 60).c_str()) : std::wstring(L"Minutes for this sitting (e.g. 60):");
  if (!Ask(Fmt(L"Timer — #%d %ls", S.cur + 1, C().name.c_str()), label, v, true) || v.empty()) return;
  int nm = std::clamp(_wtoi(v.c_str()), 1, 1440);
  long long used = live ? std::max(0LL, C().mins * 60LL - C().rem) : 0;
  C().mins = nm;
  C().rem = std::max(0LL, nm * 60LL - used);
  if (C().rem == 0) { EndSession(L"Completed"); return; }
  Changed();
}
static void ResetTimer() {
  if (SS.active && SS.cat == S.cur && (SS.secs >= 30 || C().done != SS.startDone)) {
    int a = MessageBoxW(g_hwnd, L"Save this sitting to the Excel log before resetting the timer?", L"Reset timer", MB_YESNOCANCEL | MB_ICONQUESTION | MB_TOPMOST);
    if (a == IDCANCEL) return;
    if (a == IDYES) { EndSession(L"Ended early"); return; }
  }
  if (SS.active && SS.cat == S.cur) SS.active = false;
  g_running = false;
  C().rem = C().mins * 60LL;
  Changed();
}
static void SwitchCat(int i) {
  int n = (int)S.cats.size();
  if (!n) return;
  int nx = ((i % n) + n) % n;
  if (nx == S.cur) return;
  if (SS.active && SS.cat == S.cur) EndSession(L"Switched session");
  g_running = false;
  S.cur = nx;
  Changed();
}
static void AddPages(int d) {
  Cat& c = C();
  int nv = std::clamp(c.done + d, 0, c.target);
  if (nv == c.done) { MessageBeep(MB_OK); return; }
  c.done = nv;
  Changed();
}
static void EditDone() {
  std::wstring v = std::to_wstring(C().done);
  if (Ask(Fmt(L"Pages done — #%d %ls", S.cur + 1, C().name.c_str()), Fmt(L"Page you finished (0 – %d):", C().target), v, true) && !v.empty()) {
    C().done = std::clamp(_wtoi(v.c_str()), 0, C().target);
    Changed();
  }
}
static void EditTarget() {
  std::wstring v = std::to_wstring(C().target);
  if (Ask(Fmt(L"Total pages — #%d %ls", S.cur + 1, C().name.c_str()), L"Total pages in this session:", v, true) && !v.empty()) {
    C().target = std::clamp(_wtoi(v.c_str()), 1, 100000);
    C().done = std::min(C().done, C().target);
    Changed();
  }
}
static void EditTitle() {
  std::wstring v = S.title;
  if (Ask(L"Title", L"Widget title:", v, false) && !v.empty()) { S.title = v.substr(0, 60); Changed(); }
}
static void FinishRound() {
  if (SS.active) EndSession(L"Round finished", false);
  int n = 0; for (auto& r : g_log) if (r.round == S.round) n++;
  if (MessageBoxW(g_hwnd, Fmt(L"Finish Round %d (%d sitting%ls logged) and save the JPG report to Desktop\\SOPrep?", S.round, n, n == 1 ? L"" : L"s").c_str(), L"Finish round",
                  MB_OKCANCEL | MB_ICONQUESTION | MB_TOPMOST) != IDOK) return;
  WriteXlsx();
  std::wstring path = RenderRoundReport();
  if (path.empty()) { MessageBoxW(g_hwnd, L"Could not save the JPG report.", L"SO Sprint", MB_OK | MB_ICONERROR | MB_TOPMOST); return; }
  S.round++;
  Changed();
  ShellExecuteW(nullptr, L"open", path.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
}

// ── all sessions editor ──
struct Row { HWND name, done, target, mins, del; int orig; bool removed; };
static std::vector<Row> g_rows;
static HWND g_edDlg = nullptr, g_addBtn = nullptr, g_saveBtn = nullptr, g_cancelBtn = nullptr;
static void LayoutEditor() {
  int y = 40;
  for (auto& r : g_rows) {
    if (r.removed) continue;
    MoveWindow(r.name, D(44), D(y), D(230), D(26), TRUE); MoveWindow(r.done, D(282), D(y), D(70), D(26), TRUE);
    MoveWindow(r.target, D(360), D(y), D(80), D(26), TRUE); MoveWindow(r.mins, D(448), D(y), D(70), D(26), TRUE);
    MoveWindow(r.del, D(526), D(y), D(30), D(26), TRUE);
    y += 32;
  }
  MoveWindow(g_addBtn, D(14), D(y + 10), D(130), D(30), TRUE);
  MoveWindow(g_saveBtn, D(384), D(y + 10), D(84), D(30), TRUE);
  MoveWindow(g_cancelBtn, D(472), D(y + 10), D(84), D(30), TRUE);
  RECT r{0, 0, D(570), D(y + 54)};
  AdjustWindowRectEx(&r, WS_CAPTION | WS_SYSMENU, FALSE, WS_EX_DLGMODALFRAME);
  SetWindowPos(g_edDlg, nullptr, 0, 0, r.right - r.left, r.bottom - r.top, SWP_NOMOVE | SWP_NOZORDER);
  InvalidateRect(g_edDlg, nullptr, TRUE);
}
static void AddRow(const std::wstring& name, int done, int target, int mins, int orig) {
  Row r;
  int id = 1000 + (int)g_rows.size();
  r.name = Ctl(L"EDIT", name.c_str(), WS_BORDER | WS_TABSTOP | ES_AUTOHSCROLL, 0, 0, 10, 10, g_edDlg, 0);
  r.done = Ctl(L"EDIT", std::to_wstring(done).c_str(), WS_BORDER | WS_TABSTOP | ES_NUMBER, 0, 0, 10, 10, g_edDlg, 0);
  r.target = Ctl(L"EDIT", std::to_wstring(target).c_str(), WS_BORDER | WS_TABSTOP | ES_NUMBER, 0, 0, 10, 10, g_edDlg, 0);
  r.mins = Ctl(L"EDIT", std::to_wstring(mins).c_str(), WS_BORDER | WS_TABSTOP | ES_NUMBER, 0, 0, 10, 10, g_edDlg, 0);
  r.del = Ctl(L"BUTTON", L"X", WS_TABSTOP, 0, 0, 10, 10, g_edDlg, id);
  r.orig = orig; r.removed = false;
  g_rows.push_back(r);
}
static void EditorCmd(int id) {
  if (id == 900) { AddRow(L"New session", 0, 100, 60, -1); LayoutEditor(); SetFocus(g_rows.back().name); SendMessageW(g_rows.back().name, EM_SETSEL, 0, -1); return; }
  if (id >= 1000 && id < 1000 + (int)g_rows.size()) {
    int live = 0; for (auto& x : g_rows) if (!x.removed) live++;
    if (live <= 1) return;
    Row& r = g_rows[id - 1000];
    r.removed = true;
    for (HWND w : {r.name, r.done, r.target, r.mins, r.del}) ShowWindow(w, SW_HIDE);
    LayoutEditor();
  }
}
static LRESULT CALLBACK EdPaintSub(HWND h, UINT m, WPARAM w, LPARAM l, UINT_PTR, DWORD_PTR) {
  if (m == WM_PAINT) {
    PAINTSTRUCT ps;
    HDC dc = BeginPaint(h, &ps);
    RECT rc; GetClientRect(h, &rc);
    FillRect(dc, &rc, (HBRUSH)(COLOR_WINDOW + 1));
    HGDIOBJ o = SelectObject(dc, UiFont());
    SetBkMode(dc, TRANSPARENT);
    SetTextColor(dc, RGB(90, 100, 120));
    const wchar_t* hdr[] = {L"#", L"Session name", L"Done", L"Total pages", L"Minutes"};
    int xs[] = {16, 44, 282, 360, 448};
    for (int i = 0; i < 5; i++) TextOutW(dc, D(xs[i]), D(14), hdr[i], (int)wcslen(hdr[i]));
    SetTextColor(dc, RGB(20, 30, 50));
    int y = 40, n = 1;
    for (auto& r : g_rows) {
      if (r.removed) continue;
      std::wstring s = std::to_wstring(n++);
      TextOutW(dc, D(18), D(y + 4), s.c_str(), (int)s.size());
      y += 32;
    }
    SelectObject(dc, o);
    EndPaint(h, &ps);
    return 0;
  }
  return DefSubclassProc(h, m, w, l);
}
static void EditSessions() {
  if (SS.active) EndSession(L"Ended to edit sessions");
  g_running = false;
  g_rows.clear();
  g_edDlg = MakeDialog(L"All sessions — serial, name, pages, total, minutes", 570, 200);
  SetWindowSubclass(g_edDlg, EdPaintSub, 1, 0);
  g_dlgCmd = EditorCmd;
  g_addBtn = Ctl(L"BUTTON", L"+ Add session", WS_TABSTOP, 0, 0, 10, 10, g_edDlg, 900);
  g_saveBtn = Ctl(L"BUTTON", L"Save", WS_TABSTOP | BS_DEFPUSHBUTTON, 0, 0, 10, 10, g_edDlg, IDOK);
  g_cancelBtn = Ctl(L"BUTTON", L"Cancel", WS_TABSTOP, 0, 0, 10, 10, g_edDlg, IDCANCEL);
  for (size_t i = 0; i < S.cats.size(); i++) AddRow(S.cats[i].name, S.cats[i].done, S.cats[i].target, S.cats[i].mins, (int)i);
  LayoutEditor();
  ShowWindow(g_edDlg, SW_SHOW);
  SetForegroundWindow(g_edDlg);
  g_modalOk = false;
  RunModal(g_edDlg);
  if (g_modalOk) {
    std::vector<Cat> nc;
    int newCur = 0;
    for (auto& r : g_rows) {
      if (r.removed) continue;
      Cat c = r.orig >= 0 ? S.cats[r.orig] : Cat{};
      std::wstring nm = GetText(r.name);
      c.name = nm.empty() ? L"Session" : nm.substr(0, 40);
      c.target = std::clamp(_wtoi(GetText(r.target).c_str()), 1, 100000);
      c.done = std::clamp(_wtoi(GetText(r.done).c_str()), 0, c.target);
      int m = std::clamp(_wtoi(GetText(r.mins).c_str()), 0, 1440);
      if (m != c.mins || r.orig < 0) c.rem = m * 60LL;
      c.mins = m;
      if (r.orig == S.cur) newCur = (int)nc.size();
      nc.push_back(c);
    }
    S.cats = nc;
    S.cur = std::clamp(newCur, 0, (int)S.cats.size() - 1);
    Changed();
  }
  g_dlgCmd = nullptr;
  DestroyWindow(g_edDlg);
  g_edDlg = nullptr;
  g_rows.clear();
}

// ───────────────────────── window ─────────────────────────
static void ApplyWindowStyle() {
  LONG_PTR ex = GetWindowLongPtrW(g_hwnd, GWL_EXSTYLE);
  if (S.opacity < 100) { SetWindowLongPtrW(g_hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED); SetLayeredWindowAttributes(g_hwnd, 0, (BYTE)(S.opacity * 255 / 100), LWA_ALPHA); }
  else if (ex & WS_EX_LAYERED) SetWindowLongPtrW(g_hwnd, GWL_EXSTYLE, ex & ~WS_EX_LAYERED);
  SetWindowPos(g_hwnd, S.topmost ? HWND_TOPMOST : HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_FRAMECHANGED);
  BOOL dark = S.theme != 3;
  DwmSetWindowAttribute(g_hwnd, 20, &dark, sizeof dark);
  COLORREF border = THEMES[S.theme].line;
  DwmSetWindowAttribute(g_hwnd, 34, &border, sizeof border);
}
static void Resize() { SetWindowPos(g_hwnd, nullptr, 0, 0, S.width, Height(), SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE); }
static void SetStartup(bool on) {
  HKEY k;
  if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE, &k) != ERROR_SUCCESS) return;
  if (on) { wchar_t p[MAX_PATH]; GetModuleFileNameW(nullptr, p, MAX_PATH); std::wstring v = L"\"" + std::wstring(p) + L"\""; RegSetValueExW(k, L"SOSprintWidget", 0, REG_SZ, (const BYTE*)v.c_str(), (DWORD)((v.size() + 1) * 2)); }
  else RegDeleteValueW(k, L"SOSprintWidget");
  RegCloseKey(k);
}
static bool IsStartup() {
  HKEY k;
  if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_QUERY_VALUE, &k) != ERROR_SUCCESS) return false;
  bool on = RegQueryValueExW(k, L"SOSprintWidget", nullptr, nullptr, nullptr, nullptr) == ERROR_SUCCESS;
  RegCloseKey(k);
  return on;
}
enum { M_EDITALL = 100, M_DONE, M_TARGET, M_TIME, M_PLAY, M_RESET, M_END, M_ROUND, M_FOLDER, M_XLSX, M_TITLE, M_TOP, M_LOCK, M_START, M_BIG, M_SMALL, M_HELP, M_HIDE, M_EXIT, M_CAT0 = 200, M_THEME0 = 300, M_OP0 = 400 };
static void Help() {
  MessageBoxW(g_hwnd,
              L"SO Sprint Widget v2\n\n"
              L"PAGES   + / − or mouse wheel (Shift = 5). Click the big number to type the page, click \"/ total\" to change the total.\n"
              L"              You cannot go beyond the total pages.\n\n"
              L"TIMER   Play/Pause button starts or pauses the countdown. Click the time to edit the minutes (even while running).\n"
              L"              Wheel over the time = ±5 min (Shift ±15). Round-arrow button resets the timer. Tick button ends the sitting now.\n\n"
              L"REPORTS When the countdown reaches 0 (or you press the tick) the sitting is saved to\n"
              L"              Desktop\\SOPrep\\SO_Study_Log.xlsx and a report card appears.\n"
              L"              \"Finish round\" saves a JPG report of the whole round in Desktop\\SOPrep and starts the next round.\n\n"
              L"SESSIONS Click the #name or a chip to switch. Menu → \"Edit all sessions\" edits every session in one table.\n\n"
              L"WINDOW  Drag empty space to move, drag the left/right edge to widen, Ctrl+wheel to zoom, right-click for the menu.",
              L"How to use", MB_OK | MB_ICONINFORMATION | MB_TOPMOST);
}
static void Menu(POINT s) {
  HMENU m = CreatePopupMenu(), cats = CreatePopupMenu(), theme = CreatePopupMenu(), op = CreatePopupMenu();
  for (int i = 0; i < (int)S.cats.size(); i++)
    AppendMenuW(cats, MF_STRING | (i == S.cur ? MF_CHECKED : 0), M_CAT0 + i, Fmt(L"#%d  %ls\t%d/%d", i + 1, S.cats[i].name.c_str(), S.cats[i].done, S.cats[i].target).c_str());
  for (int i = 0; i < 4; i++) AppendMenuW(theme, MF_STRING | (i == S.theme ? MF_CHECKED : 0), M_THEME0 + i, THEMES[i].name);
  for (int v : {100, 90, 80, 70, 60}) AppendMenuW(op, MF_STRING | (v == S.opacity ? MF_CHECKED : 0), M_OP0 + v, Fmt(L"%d%%", v).c_str());
  AppendMenuW(m, MF_POPUP, (UINT_PTR)cats, L"Switch session");
  AppendMenuW(m, MF_STRING, M_EDITALL, L"Edit all sessions…");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_STRING, M_DONE, L"Set pages done…");
  AppendMenuW(m, MF_STRING, M_TARGET, L"Set total pages…");
  AppendMenuW(m, MF_STRING, M_TIME, L"Set / edit timer minutes…");
  AppendMenuW(m, MF_STRING | (C().mins ? 0 : MF_GRAYED), M_PLAY, g_running ? L"Pause timer" : L"Start timer");
  AppendMenuW(m, MF_STRING | (C().mins ? 0 : MF_GRAYED), M_RESET, L"Reset timer");
  AppendMenuW(m, MF_STRING | (SS.active ? 0 : MF_GRAYED), M_END, L"End sitting now (save + report)");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_STRING, M_ROUND, Fmt(L"Finish round %d → JPG report", S.round).c_str());
  AppendMenuW(m, MF_STRING, M_XLSX, L"Open Excel log");
  AppendMenuW(m, MF_STRING, M_FOLDER, L"Open Desktop\\SOPrep folder");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_STRING, M_TITLE, L"Edit title…");
  AppendMenuW(m, MF_POPUP, (UINT_PTR)theme, L"Theme");
  AppendMenuW(m, MF_POPUP, (UINT_PTR)op, L"Opacity");
  AppendMenuW(m, MF_STRING, M_BIG, L"Bigger\tCtrl+Wheel");
  AppendMenuW(m, MF_STRING, M_SMALL, L"Smaller");
  AppendMenuW(m, MF_STRING | (S.topmost ? MF_CHECKED : 0), M_TOP, L"Always on top");
  AppendMenuW(m, MF_STRING | (S.locked ? MF_CHECKED : 0), M_LOCK, L"Lock position and width");
  AppendMenuW(m, MF_STRING | (IsStartup() ? MF_CHECKED : 0), M_START, L"Start with Windows");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_STRING, M_HELP, L"How to use");
  AppendMenuW(m, MF_STRING, M_HIDE, L"Hide to tray");
  AppendMenuW(m, MF_STRING, M_EXIT, L"Exit");
  SetForegroundWindow(g_hwnd);
  int cmd = TrackPopupMenu(m, TPM_RETURNCMD | TPM_RIGHTBUTTON, s.x, s.y, 0, g_hwnd, nullptr);
  DestroyMenu(m);
  if (!cmd) return;
  if (cmd >= M_CAT0 && cmd < M_CAT0 + 100) { SwitchCat(cmd - M_CAT0); return; }
  if (cmd >= M_THEME0 && cmd < M_THEME0 + 4) { S.theme = cmd - M_THEME0; ApplyWindowStyle(); Changed(); return; }
  if (cmd >= M_OP0 && cmd <= M_OP0 + 100) { S.opacity = cmd - M_OP0; ApplyWindowStyle(); Changed(); return; }
  switch (cmd) {
    case M_EDITALL: EditSessions(); break;
    case M_DONE: EditDone(); break;
    case M_TARGET: EditTarget(); break;
    case M_TIME: SetTime(); break;
    case M_PLAY: StartPause(); break;
    case M_RESET: ResetTimer(); break;
    case M_END: EndSession(L"Ended early"); break;
    case M_ROUND: FinishRound(); break;
    case M_XLSX: if (g_lastXlsx.empty()) WriteXlsx(); if (!g_lastXlsx.empty()) ShellExecuteW(nullptr, L"open", g_lastXlsx.c_str(), nullptr, nullptr, SW_SHOWNORMAL); break;
    case M_FOLDER: ShellExecuteW(nullptr, L"open", SOPrepDir().c_str(), nullptr, nullptr, SW_SHOWNORMAL); break;
    case M_TITLE: EditTitle(); break;
    case M_TOP: S.topmost = !S.topmost; ApplyWindowStyle(); Changed(); break;
    case M_LOCK: S.locked = !S.locked; Changed(); break;
    case M_START: SetStartup(!IsStartup()); break;
    case M_BIG: S.zoom = std::min(1.8, S.zoom + 0.1); Resize(); Changed(); break;
    case M_SMALL: S.zoom = std::max(0.8, S.zoom - 0.1); Resize(); Changed(); break;
    case M_HELP: Help(); break;
    case M_HIDE: ShowWindow(g_hwnd, SW_HIDE); break;
    case M_EXIT: DestroyWindow(g_hwnd); break;
  }
}
static LRESULT CALLBACK WndProc(HWND h, UINT m, WPARAM w, LPARAM l) {
  switch (m) {
    case WM_NCCALCSIZE: if (w) return 0; break;
    case WM_NCHITTEST: {
      POINT p{GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      ScreenToClient(h, &p);
      RECT rc; GetClientRect(h, &rc);
      if (!S.locked) { if (p.x < Px(6)) return HTLEFT; if (p.x >= rc.right - Px(6)) return HTRIGHT; }
      const Zone* z = ZoneAt(p);
      if (z && z->hit != H_DRAG && z->hit != H_TOTAL) return HTCLIENT;
      return S.locked ? HTCLIENT : HTCAPTION;
    }
    case WM_GETMINMAXINFO: { auto* mm = (MINMAXINFO*)l; mm->ptMinTrackSize = {Px(260), Height()}; mm->ptMaxTrackSize = {Px(2200), Height()}; return 0; }
    case WM_SIZE: if (w != SIZE_MINIMIZED) { RECT r; GetWindowRect(h, &r); S.width = r.right - r.left; Redraw(); } return 0;
    case WM_EXITSIZEMOVE: { RECT r; GetWindowRect(h, &r); S.x = r.left; S.y = r.top; S.width = r.right - r.left; Save(); return 0; }
    case WM_DPICHANGED: { g_dpi = HIWORD(w); F.key = 0; RECT* r = (RECT*)l; SetWindowPos(h, nullptr, r->left, r->top, r->right - r->left, Height(), SWP_NOZORDER | SWP_NOACTIVATE); return 0; }
    case WM_ERASEBKGND: return 1;
    case WM_PAINT: { PAINTSTRUCT ps; HDC dc = BeginPaint(h, &ps); Paint(h, dc); EndPaint(h, &ps); return 0; }
    case WM_MOUSEMOVE: {
      g_mouse = {GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      if (!g_tracking) { TRACKMOUSEEVENT t{sizeof t, TME_LEAVE, h, 0}; TrackMouseEvent(&t); g_tracking = true; }
      const Zone* z = ZoneAt(g_mouse);
      SetCursor(LoadCursor(nullptr, z && z->hit != H_DRAG && z->hit != H_TOTAL ? IDC_HAND : IDC_ARROW));
      Redraw();
      return 0;
    }
    case WM_MOUSELEAVE: g_mouse = {-1, -1}; g_tracking = false; Redraw(); return 0;
    case WM_SETCURSOR: if (LOWORD(l) == HTCLIENT) return TRUE; break;
    case WM_LBUTTONUP: {
      POINT p{GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      const Zone* z = ZoneAt(p);
      if (!z) return 0;
      bool shift = GetKeyState(VK_SHIFT) < 0;
      Hit hit = z->hit;
      int idx = z->idx;
      switch (hit) {
        case H_PLUS: AddPages(shift ? 5 : 1); break;
        case H_MINUS: AddPages(shift ? -5 : -1); break;
        case H_DONE: EditDone(); break;
        case H_TARGET: EditTarget(); break;
        case H_NAME: SwitchCat(S.cur + 1); break;
        case H_CHIP: SwitchCat(idx); break;
        case H_PLAY: StartPause(); break;
        case H_TIME: SetTime(); break;
        case H_RESET: ResetTimer(); break;
        case H_END: if (SS.active && SS.cat == S.cur) EndSession(L"Ended early"); break;
        case H_ROUND: FinishRound(); break;
        case H_MENU: { POINT s = p; ClientToScreen(h, &s); Menu(s); break; }
        default: break;
      }
      return 0;
    }
    case WM_MOUSEWHEEL: {
      int d = GET_WHEEL_DELTA_WPARAM(w) > 0 ? 1 : -1;
      bool shift = GET_KEYSTATE_WPARAM(w) & MK_SHIFT;
      if (GET_KEYSTATE_WPARAM(w) & MK_CONTROL) { S.zoom = std::clamp(S.zoom + d * 0.1, 0.8, 1.8); Resize(); Changed(); return 0; }
      POINT p{GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      ScreenToClient(h, &p);
      const Zone* z = ZoneAt(p);
      if (z && (z->hit == H_TIME || z->hit == H_PLAY)) {
        int nm = std::clamp(C().mins + d * (shift ? 15 : 5), 0, 1440);
        C().rem = std::max(0LL, C().rem + (long long)(nm - C().mins) * 60);
        C().mins = nm;
        if (!nm) { g_running = false; if (SS.active && SS.cat == S.cur) SS.active = false; }
        Changed();
      } else if (z && (z->hit == H_NAME || z->hit == H_CHIP)) SwitchCat(S.cur - d);
      else AddPages(d * (shift ? 5 : 1));
      return 0;
    }
    case WM_RBUTTONUP: { POINT s{GET_X_LPARAM(l), GET_Y_LPARAM(l)}; ClientToScreen(h, &s); Menu(s); return 0; }
    case WM_NCRBUTTONUP: { POINT s{GET_X_LPARAM(l), GET_Y_LPARAM(l)}; Menu(s); return 0; }
    case WM_NCLBUTTONDBLCLK: case WM_CONTEXTMENU: return 0;
    case WM_TIMER:
      if (w == TIMER_TICK) {
        ULONGLONG now = GetTickCount64();
        if (g_running) {
          ULONGLONG ms = now - g_lastTick;
          if (ms >= 1000) {
            long long s = (long long)(ms / 1000);
            g_lastTick += s * 1000;
            SS.secs += s;
            C().secs += s;
            C().rem -= s;
            if (C().rem <= 0) {
              C().rem = 0;
              MessageBeep(MB_ICONEXCLAMATION);
              FLASHWINFO fw{sizeof fw, h, FLASHW_ALL, 4, 0};
              FlashWindowEx(&fw);
              EndSession(L"Completed");
            } else if (SS.secs % 30 == 0) Save();
          }
        } else g_lastTick = now;
        Redraw();
      } else if (w == TIMER_TOP && S.topmost && IsWindowVisible(h)) SetWindowPos(h, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE);
      return 0;
    case WM_TRAY:
      if (LOWORD(l) == WM_LBUTTONUP) ShowWindow(h, IsWindowVisible(h) ? SW_HIDE : SW_SHOWNOACTIVATE);
      else if (LOWORD(l) == WM_RBUTTONUP) { POINT s; GetCursorPos(&s); Menu(s); }
      return 0;
    case WM_QUERYENDSESSION: Save(); return TRUE;
    case WM_DESTROY: g_running = false; Save(); Shell_NotifyIconW(NIM_DELETE, &g_nid); PostQuitMessage(0); return 0;
  }
  return DefWindowProcW(h, m, w, l);
}

typedef BOOL(WINAPI* SetDpiCtx)(HANDLE);
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {
  g_inst = inst;
  HANDLE single = CreateMutexW(nullptr, TRUE, L"SOSprintWidget.Single");
  if (GetLastError() == ERROR_ALREADY_EXISTS) {
    if (HWND o = FindWindowW(L"SOSprintWidget", nullptr)) { ShowWindow(o, SW_SHOWNOACTIVATE); SetWindowPos(o, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE); }
    return 0;
  }
  if (auto f = (SetDpiCtx)GetProcAddress(GetModuleHandleW(L"user32"), "SetProcessDpiAwarenessContext")) f((HANDLE)-4);
  INITCOMMONCONTROLSEX icc{sizeof icc, ICC_STANDARD_CLASSES};
  InitCommonControlsEx(&icc);
  Gdiplus::GdiplusStartupInput gin;
  Gdiplus::GdiplusStartup(&g_gdipToken, &gin, nullptr);
  Load();
  WNDCLASSEXW wc{sizeof wc};
  wc.style = CS_HREDRAW | CS_VREDRAW; wc.lpfnWndProc = WndProc; wc.hInstance = inst;
  wc.hIcon = LoadIconW(inst, MAKEINTRESOURCEW(IDI_APP)); wc.hIconSm = wc.hIcon; wc.hCursor = LoadCursor(nullptr, IDC_ARROW); wc.lpszClassName = L"SOSprintWidget";
  RegisterClassExW(&wc);
  POINT pt{0, 0};
  HMONITOR mon = MonitorFromPoint(pt, MONITOR_DEFAULTTOPRIMARY);
  typedef HRESULT(WINAPI * GetDpiMon)(HMONITOR, int, UINT*, UINT*);
  UINT dx = 96, dy = 96;
  if (HMODULE sh = LoadLibraryW(L"shcore.dll")) if (auto gd = (GetDpiMon)GetProcAddress(sh, "GetDpiForMonitor")) gd(mon, 0, &dx, &dy);
  g_dpi = (int)dx;
  MONITORINFO mi{sizeof mi};
  GetMonitorInfoW(mon, &mi);
  int W = std::clamp(S.width, Px(260), std::max(Px(260), (int)(mi.rcWork.right - mi.rcWork.left))), H = Height(), X = S.x, Y = S.y;
  int vl = GetSystemMetrics(SM_XVIRTUALSCREEN), vt = GetSystemMetrics(SM_YVIRTUALSCREEN), vr = vl + GetSystemMetrics(SM_CXVIRTUALSCREEN), vb = vt + GetSystemMetrics(SM_CYVIRTUALSCREEN);
  if (X < vl - W / 2 || X > vr - 40 || Y < vt || Y > vb - 20) { X = mi.rcWork.left + (mi.rcWork.right - mi.rcWork.left - W) / 2; Y = mi.rcWork.top + Px(8); }
  g_hwnd = CreateWindowExW(WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE | (S.topmost ? WS_EX_TOPMOST : 0), L"SOSprintWidget", L"SO Sprint Widget", WS_POPUP | WS_THICKFRAME, X, Y, W, H, nullptr, nullptr, inst, nullptr);
  int corner = 2;
  DwmSetWindowAttribute(g_hwnd, 33, &corner, sizeof corner);
  MARGINS mg{0, 0, 1, 0};
  DwmExtendFrameIntoClientArea(g_hwnd, &mg);
  ApplyWindowStyle();
  SetWindowPos(g_hwnd, nullptr, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED | SWP_NOACTIVATE);
  ShowWindow(g_hwnd, SW_SHOWNOACTIVATE);
  g_lastTick = GetTickCount64();
  SetTimer(g_hwnd, TIMER_TICK, 250, nullptr);
  SetTimer(g_hwnd, TIMER_TOP, 2000, nullptr);
  g_nid.cbSize = sizeof g_nid; g_nid.hWnd = g_hwnd; g_nid.uID = 1; g_nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
  g_nid.uCallbackMessage = WM_TRAY; g_nid.hIcon = wc.hIcon;
  wcscpy(g_nid.szTip, L"SO Sprint Widget — click to show/hide");
  Shell_NotifyIconW(NIM_ADD, &g_nid);
  MSG msg;
  while (GetMessageW(&msg, nullptr, 0, 0)) { TranslateMessage(&msg); DispatchMessageW(&msg); }
  delete g_card;
  delete g_ff;
  Gdiplus::GdiplusShutdown(g_gdipToken);
  if (single) CloseHandle(single);
  return 0;
}
