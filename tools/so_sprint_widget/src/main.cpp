// SO Sprint Widget — a tiny always-on-top reading tracker for the SO written exam.
// Native Win32 + GDI+ (no runtime needed). Grows sideways, never vertically.
// Build (Linux → Windows):  see ../build.sh
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
#include <dwmapi.h>
#include <shlobj.h>
#include <algorithm>
#include <cmath>
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

// ───────────────────────── state ─────────────────────────
struct Cat {
  std::wstring name;
  int done = 0, target = 100;
  long long secs = 0;  // reading time spent in this category
};
struct Theme {
  const wchar_t* name;
  COLORREF bg1, bg2, text, muted, track, btn, btnHover;
};
static const Theme THEMES[] = {
    {L"Midnight", RGB(14, 20, 36), RGB(27, 36, 58), RGB(232, 237, 245), RGB(148, 163, 184), RGB(51, 65, 85), RGB(38, 50, 74), RGB(56, 72, 104)},
    {L"Ocean", RGB(8, 28, 48), RGB(14, 48, 78), RGB(226, 240, 252), RGB(140, 176, 204), RGB(34, 72, 104), RGB(22, 58, 90), RGB(34, 82, 122)},
    {L"Plum", RGB(32, 16, 38), RGB(52, 26, 58), RGB(246, 232, 246), RGB(190, 160, 196), RGB(80, 48, 88), RGB(64, 36, 72), RGB(90, 54, 100)},
    {L"Paper", RGB(250, 251, 253), RGB(236, 240, 246), RGB(17, 24, 39), RGB(100, 116, 139), RGB(214, 220, 230), RGB(226, 232, 240), RGB(203, 213, 225)},
};
static const COLORREF CAT_COLORS[] = {RGB(52, 211, 153), RGB(56, 189, 248), RGB(251, 191, 36), RGB(251, 113, 133),
                                      RGB(167, 139, 250), RGB(163, 230, 53), RGB(34, 211, 238), RGB(251, 146, 60)};
static const int NCOLORS = 8;

struct State {
  std::wstring title = L"SO Written · 27 Nov";
  std::vector<Cat> cats;
  int cur = 0, theme = 0, opacity = 100;
  bool topmost = true, countdown = true, locked = false;
  double zoom = 1.0;
  int width = 660, x = -1, y = -1;
} S;

static bool g_running = false;
static ULONGLONG g_lastTick = 0;
static long long g_sessionSecs = 0;
static int g_sessionStartDone = 0;
static HWND g_hwnd = nullptr;
static HINSTANCE g_inst = nullptr;
static NOTIFYICONDATAW g_nid{};
static std::wstring g_ini;
static int g_dpi = 96;
static POINT g_mouse{-1, -1};
static bool g_tracking = false;
static ULONG_PTR g_gdipToken = 0;

// ───────────────────────── persistence ─────────────────────────
static std::wstring IniPath() {
  wchar_t buf[MAX_PATH];
  if (SUCCEEDED(SHGetFolderPathW(nullptr, CSIDL_APPDATA, nullptr, 0, buf))) {
    std::wstring dir = std::wstring(buf) + L"\\SOSprintWidget";
    CreateDirectoryW(dir.c_str(), nullptr);
    return dir + L"\\settings.ini";
  }
  return L"SOSprintWidget.ini";
}
static void PutI(const wchar_t* sec, const wchar_t* key, long long v) {
  wchar_t b[32];
  swprintf(b, 32, L"%lld", v);
  WritePrivateProfileStringW(sec, key, b, g_ini.c_str());
}
static long long GetI(const wchar_t* sec, const wchar_t* key, long long def) {
  wchar_t b[32];
  GetPrivateProfileStringW(sec, key, L"", b, 32, g_ini.c_str());
  if (!b[0]) return def;
  return _wtoi64(b);
}
static std::wstring GetS(const wchar_t* sec, const wchar_t* key, const std::wstring& def) {
  wchar_t b[512];
  GetPrivateProfileStringW(sec, key, L"\x01", b, 512, g_ini.c_str());
  if (b[0] == 1) return def;
  return b;
}
static void Save() {
  const wchar_t* A = L"app";
  WritePrivateProfileStringW(A, L"title", S.title.c_str(), g_ini.c_str());
  PutI(A, L"cur", S.cur);
  PutI(A, L"theme", S.theme);
  PutI(A, L"opacity", S.opacity);
  PutI(A, L"topmost", S.topmost);
  PutI(A, L"countdown", S.countdown);
  PutI(A, L"locked", S.locked);
  PutI(A, L"zoom", (long long)std::lround(S.zoom * 100));
  PutI(A, L"width", S.width);
  PutI(A, L"x", S.x);
  PutI(A, L"y", S.y);
  PutI(A, L"cats", (long long)S.cats.size());
  for (size_t i = 0; i < S.cats.size(); i++) {
    wchar_t sec[16];
    swprintf(sec, 16, L"cat%zu", i);
    WritePrivateProfileStringW(sec, L"name", S.cats[i].name.c_str(), g_ini.c_str());
    PutI(sec, L"done", S.cats[i].done);
    PutI(sec, L"target", S.cats[i].target);
    PutI(sec, L"secs", S.cats[i].secs);
  }
  // drop stale sections beyond the current count
  for (size_t i = S.cats.size(); i < S.cats.size() + 4; i++) {
    wchar_t sec[16];
    swprintf(sec, 16, L"cat%zu", i);
    WritePrivateProfileStringW(sec, nullptr, nullptr, g_ini.c_str());
  }
}
static void Load() {
  g_ini = IniPath();
  const wchar_t* A = L"app";
  int n = (int)GetI(A, L"cats", -1);
  if (n < 0) {  // first run: the 77-hour plan's reading targets
    S.cats = {{L"Focus Writing", 0, 115}, {L"Math (Khairul)", 0, 170}, {L"Analytical", 0, 80}, {L"English Focus", 0, 31},
              {L"Proficiency", 0, 28},    {L"Finance (Alal)", 0, 40}, {L"Translation", 0, 18}, {L"GK 500", 0, 19}};
    Save();
    return;
  }
  S.title = GetS(A, L"title", S.title);
  S.cur = (int)GetI(A, L"cur", 0);
  S.theme = (int)GetI(A, L"theme", 0);
  S.opacity = (int)GetI(A, L"opacity", 100);
  S.topmost = GetI(A, L"topmost", 1) != 0;
  S.countdown = GetI(A, L"countdown", 1) != 0;
  S.locked = GetI(A, L"locked", 0) != 0;
  S.zoom = GetI(A, L"zoom", 100) / 100.0;
  S.width = (int)GetI(A, L"width", 660);
  S.x = (int)GetI(A, L"x", -1);
  S.y = (int)GetI(A, L"y", -1);
  for (int i = 0; i < n && i < 32; i++) {
    wchar_t sec[16];
    swprintf(sec, 16, L"cat%d", i);
    Cat c;
    c.name = GetS(sec, L"name", L"Category");
    c.done = (int)GetI(sec, L"done", 0);
    c.target = (int)GetI(sec, L"target", 100);
    c.secs = GetI(sec, L"secs", 0);
    S.cats.push_back(c);
  }
  if (S.cats.empty()) S.cats.push_back({L"Reading", 0, 100});
  S.cur = std::clamp(S.cur, 0, (int)S.cats.size() - 1);
  S.theme = std::clamp(S.theme, 0, 3);
  S.opacity = std::clamp(S.opacity, 40, 100);
  S.zoom = std::clamp(S.zoom, 0.8, 1.8);
}

// ───────────────────────── helpers ─────────────────────────
static double Sc() { return g_dpi / 96.0 * S.zoom; }
static int Px(double v) { return (int)std::lround(v * Sc()); }
static int Height() { return Px(54); }
static Cat& C() { return S.cats[S.cur]; }
static Gdiplus::Color GC(COLORREF c, BYTE a = 255) { return Gdiplus::Color(a, GetRValue(c), GetGValue(c), GetBValue(c)); }
static COLORREF Mix(COLORREF a, COLORREF b, double t) {
  return RGB((int)(GetRValue(a) * (1 - t) + GetRValue(b) * t), (int)(GetGValue(a) * (1 - t) + GetGValue(b) * t),
             (int)(GetBValue(a) * (1 - t) + GetBValue(b) * t));
}
static std::wstring Fmt(const wchar_t* f, ...) {
  wchar_t b[256];
  va_list ap;
  va_start(ap, f);
  vswprintf(b, 256, f, ap);
  va_end(ap);
  return b;
}
static std::wstring HMS(long long s) { return Fmt(L"%02lld:%02lld:%02lld", s / 3600, (s / 60) % 60, s % 60); }
static std::wstring Dur(double hours) {
  if (hours < 0 || !std::isfinite(hours)) return L"—";
  long long m = (long long)std::lround(hours * 60);
  if (m >= 60) return Fmt(L"%lldh %02lldm", m / 60, m % 60);
  return Fmt(L"%lldm", m);
}
static COLORREF CatColor(int i) { return CAT_COLORS[((i % NCOLORS) + NCOLORS) % NCOLORS]; }

// exam: Friday 27 Nov 2026, 09:30 (local time = Bangladesh)
static long long SecsToExam() {
  SYSTEMTIME ex{2026, 11, 5, 27, 9, 30, 0, 0}, now;
  GetLocalTime(&now);
  FILETIME fe, fn;
  SystemTimeToFileTime(&ex, &fe);
  SystemTimeToFileTime(&now, &fn);
  ULARGE_INTEGER a, b;
  a.LowPart = fe.dwLowDateTime; a.HighPart = fe.dwHighDateTime;
  b.LowPart = fn.dwLowDateTime; b.HighPart = fn.dwHighDateTime;
  return ((long long)a.QuadPart - (long long)b.QuadPart) / 10000000LL;
}
static double PaceNow() {  // pages per hour
  if (g_sessionSecs >= 300 && C().done > g_sessionStartDone) return (C().done - g_sessionStartDone) / (g_sessionSecs / 3600.0);
  if (C().secs >= 600 && C().done > 0) return C().done / (C().secs / 3600.0);
  return -1;
}

// ───────────────────────── fonts ─────────────────────────
struct Fonts { HFONT big = 0, title = 0, small = 0, tiny = 0; int dpiKey = 0; } F;
static HFONT MakeFont(int px, int weight) {
  HFONT f = CreateFontW(-px, 0, 0, 0, weight, 0, 0, 0, DEFAULT_CHARSET, OUT_TT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY,
                        DEFAULT_PITCH, L"Segoe UI Variable Display");
  LOGFONTW lf{};
  GetObjectW(f, sizeof lf, &lf);
  if (wcscmp(lf.lfFaceName, L"Segoe UI Variable Display") != 0) {  // older Windows
    DeleteObject(f);
    f = CreateFontW(-px, 0, 0, 0, weight, 0, 0, 0, DEFAULT_CHARSET, OUT_TT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY,
                    DEFAULT_PITCH, L"Segoe UI");
  }
  return f;
}
static void EnsureFonts() {
  int key = (int)std::lround(Sc() * 1000);
  if (F.dpiKey == key) return;
  for (HFONT f : {F.big, F.title, F.small, F.tiny})
    if (f) DeleteObject(f);
  F.big = MakeFont(Px(19), FW_SEMIBOLD);
  F.title = MakeFont(Px(13.5), FW_SEMIBOLD);
  F.small = MakeFont(Px(11.5), FW_NORMAL);
  F.tiny = MakeFont(Px(10.5), FW_SEMIBOLD);
  F.dpiKey = key;
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

// ───────────────────────── layout & hit-testing ─────────────────────────
enum Hit { H_NONE, H_DRAG, H_TITLE, H_CAT, H_MINUS, H_PLUS, H_DONE, H_TARGET, H_TIMER, H_RESET, H_COUNT, H_MENU, H_CHIP };
struct Zone { Hit hit; RECT r; int idx; };
static std::vector<Zone> g_zones;
static bool In(const RECT& r, POINT p) { return p.x >= r.left && p.x < r.right && p.y >= r.top && p.y < r.bottom; }
static const Zone* ZoneAt(POINT p) {
  for (auto it = g_zones.rbegin(); it != g_zones.rend(); ++it)
    if (In(it->r, p)) return &*it;
  return nullptr;
}
static bool Hover(const RECT& r) { return In(r, g_mouse); }

static void RoundRect(Gdiplus::Graphics& g, Gdiplus::Brush* b, float x, float y, float w, float h, float rad) {
  Gdiplus::GraphicsPath p;
  float d = rad * 2;
  if (d > h) d = h;
  if (d > w) d = w;
  p.AddArc(x, y, d, d, 180, 90);
  p.AddArc(x + w - d, y, d, d, 270, 90);
  p.AddArc(x + w - d, y + h - d, d, d, 0, 90);
  p.AddArc(x, y + h - d, d, d, 90, 90);
  p.CloseFigure();
  g.FillPath(b, &p);
}

// ───────────────────────── painting ─────────────────────────
static void Paint(HWND hwnd, HDC hdc) {
  RECT rc;
  GetClientRect(hwnd, &rc);
  int W = rc.right, H = rc.bottom;
  if (W <= 0 || H <= 0) return;
  EnsureFonts();
  const Theme& T = THEMES[S.theme];
  HDC mem = CreateCompatibleDC(hdc);
  HBITMAP bmp = CreateCompatibleBitmap(hdc, W, H);
  HGDIOBJ oldBmp = SelectObject(mem, bmp);
  g_zones.clear();

  Cat& c = C();
  COLORREF acc = CatColor(S.cur);
  bool complete = c.target > 0 && c.done >= c.target;
  COLORREF ring = complete ? RGB(250, 204, 21) : acc;
  double frac = c.target > 0 ? std::clamp((double)c.done / c.target, 0.0, 1.0) : 0;
  int left = std::max(0, c.target - c.done);

  // ── measure blocks (priority order) ──
  int pad = Px(12), gap = Px(14), mid = H / 2;
  std::wstring pctS = Fmt(L"%d%%", (int)std::lround(frac * 100));
  std::wstring doneS = std::to_wstring(c.done), targetS = Fmt(L"/ %d", c.target);
  std::wstring leftS = complete ? L"target done!" : Fmt(L"%d left", left);
  double pace = PaceNow();
  std::wstring timeS = HMS(g_sessionSecs);
  std::wstring paceS = pace > 0 ? Fmt(L"%.0f p/h · ETA %s", pace, Dur(left / pace).c_str()) : (g_running ? L"reading…" : L"paused");
  long long ex = SecsToExam();
  std::wstring cdS = ex > 0 ? Fmt(L"%lldd %02lldh %02lldm", ex / 86400, (ex / 3600) % 24, (ex / 60) % 60) : (ex > -7200 ? L"exam now" : L"exam done");
  std::wstring cdSub = L"to exam · Fri 9:30";

  int ringW = H - Px(14);
  int titleW = std::clamp((int)std::max(TextSize(mem, F.title, S.title).cx, TextSize(mem, F.small, c.name).cx + Px(26)), Px(70), Px(210));
  int btnD = Px(22);
  int numW = TextSize(mem, F.big, doneS).cx + Px(4) + TextSize(mem, F.small, targetS).cx;
  int pagesW = std::max(numW, TextSize(mem, F.small, leftS).cx) + 2 * btnD + Px(12);
  int timerW = std::max(TextSize(mem, F.title, timeS).cx + Px(22), TextSize(mem, F.small, paceS).cx);
  int cdW = std::max(TextSize(mem, F.title, cdS).cx, TextSize(mem, F.small, cdSub).cx);
  int menuW = Px(26);
  int avail = W - pad - menuW - Px(6);

  bool showTitle = true, showTimer = false, showCd = false, showChips = false;
  int x0 = pad + ringW + gap;
  int used = x0 + titleW + gap + pagesW;
  if (used > avail) { showTitle = false; used = x0 + pagesW; }
  if (used + gap + timerW <= avail) { showTimer = true; used += gap + timerW; }
  if (S.countdown && used + gap + cdW <= avail) { showCd = true; used += gap + cdW; }
  int chipsX = used + gap;
  if (S.cats.size() > 1 && avail - chipsX > Px(90)) showChips = true;

  // ── shapes (GDI+) ──
  {
    Gdiplus::Graphics g(mem);
    g.SetSmoothingMode(Gdiplus::SmoothingModeAntiAlias);
    g.SetPixelOffsetMode(Gdiplus::PixelOffsetModeHalf);
    Gdiplus::LinearGradientBrush bg(Gdiplus::Point(0, 0), Gdiplus::Point(W, H), GC(T.bg1), GC(T.bg2));
    g.FillRectangle(&bg, 0, 0, W, H);
    // subtle accent glow on the left
    Gdiplus::LinearGradientBrush glow(Gdiplus::Point(0, 0), Gdiplus::Point(Px(140), 0), GC(acc, S.theme == 3 ? 26 : 34), GC(acc, 0));
    g.FillRectangle(&glow, 0, 0, Px(140), H);
    // progress ring
    float rx = (float)pad, ry = (float)(mid - ringW / 2), rw = (float)ringW;
    float pw = (float)Px(4.2);
    Gdiplus::Pen track(GC(T.track), pw);
    g.DrawEllipse(&track, rx + pw / 2, ry + pw / 2, rw - pw, rw - pw);
    if (frac > 0) {
      Gdiplus::Pen arc(GC(ring), pw);
      arc.SetStartCap(Gdiplus::LineCapRound);
      arc.SetEndCap(Gdiplus::LineCapRound);
      g.DrawArc(&arc, rx + pw / 2, ry + pw / 2, rw - pw, rw - pw, -90.0f, (float)std::max(frac * 360.0, 2.0));
    }
    // pages buttons
    int px0 = x0 + (showTitle ? titleW + gap : 0);
    RECT minus{px0, mid - btnD / 2, px0 + btnD, mid + btnD / 2};
    RECT plus{px0 + pagesW - btnD, mid - btnD / 2, px0 + pagesW, mid + btnD / 2};
    for (RECT* r : {&minus, &plus}) {
      bool hv = Hover(*r);
      Gdiplus::SolidBrush b(GC(r == &plus ? (hv ? Mix(acc, RGB(255, 255, 255), 0.15) : acc) : (hv ? T.btnHover : T.btn)));
      g.FillEllipse(&b, (float)r->left, (float)r->top, (float)btnD, (float)btnD);
    }
    // thin progress bar under the numbers
    float bx = (float)(minus.right + Px(6)), bw = (float)(plus.left - Px(6)) - bx, by = (float)(H - Px(9)), bh = (float)Px(3.2);
    Gdiplus::SolidBrush tb(GC(T.track));
    RoundRect(g, &tb, bx, by, bw, bh, bh / 2);
    if (frac > 0) {
      Gdiplus::LinearGradientBrush pb(Gdiplus::PointF(bx, 0), Gdiplus::PointF(bx + bw + 1, 0), GC(ring), GC(Mix(ring, RGB(255, 255, 255), 0.35)));
      RoundRect(g, &pb, bx, by, (float)std::max(bw * frac, (double)bh), bh, bh / 2);
    }
    // timer play/pause glyph and category chevron (vector, so no font is needed)
    if (showTimer) {
      int tx = px0 + pagesW + gap;
      float gy = (float)(mid - Px(15)), gs = (float)Px(10);
      RECT tz{tx, mid - Px(22), tx + timerW, mid + Px(20)};
      Gdiplus::SolidBrush gb(GC(g_running ? acc : (Hover(tz) ? T.text : T.muted)));
      if (g_running) {
        g.FillRectangle(&gb, (float)tx + Px(1), gy, (float)Px(3), gs);
        g.FillRectangle(&gb, (float)tx + Px(6.5), gy, (float)Px(3), gs);
      } else {
        Gdiplus::PointF tri[3] = {{(float)tx + Px(1), gy}, {(float)tx + Px(1), gy + gs}, {(float)tx + Px(10), gy + gs / 2}};
        g.FillPolygon(&gb, tri, 3);
      }
    }
    if (showTitle) {
      int nameW = std::min(TextSize(mem, F.small, c.name).cx, titleW - Px(26));
      float cx = (float)(x0 + Px(12) + nameW + Px(6)), cy = (float)(mid + Px(10));
      Gdiplus::Pen chev(GC(acc), (float)Px(1.6));
      chev.SetStartCap(Gdiplus::LineCapRound);
      chev.SetEndCap(Gdiplus::LineCapRound);
      g.DrawLine(&chev, cx, cy - Px(1.5), cx + Px(3.5), cy + Px(2));
      g.DrawLine(&chev, cx + Px(3.5), cy + Px(2), cx + Px(7), cy - Px(1.5));
      Gdiplus::SolidBrush dotb(GC(acc));
      g.FillEllipse(&dotb, (float)x0 + Px(1), cy - Px(3), (float)Px(6), (float)Px(6));
    }
    // chips
    if (showChips) {
      int cx = chipsX, cy = mid - Px(12), ch = Px(24);
      for (int i = 0; i < (int)S.cats.size(); i++) {
        if (i == S.cur) continue;
        const Cat& k = S.cats[i];
        std::wstring s = k.name + Fmt(L"  %d/%d", k.done, k.target);
        int w = TextSize(mem, F.tiny, s).cx + Px(20);
        if (cx + w > avail) break;
        RECT r{cx, cy, cx + w, cy + ch};
        bool hv = Hover(r);
        Gdiplus::SolidBrush cb(GC(hv ? T.btnHover : T.btn));
        RoundRect(g, &cb, (float)r.left, (float)r.top, (float)w, (float)ch, ch / 2.0f);
        double f = k.target > 0 ? std::clamp((double)k.done / k.target, 0.0, 1.0) : 0;
        Gdiplus::SolidBrush fb(GC(CatColor(i), 70));
        if (f > 0) RoundRect(g, &fb, (float)r.left, (float)r.top, (float)std::max(w * f, (double)ch), (float)ch, ch / 2.0f);
        Gdiplus::SolidBrush dot(GC(CatColor(i)));
        g.FillEllipse(&dot, (float)r.left + Px(8), (float)mid - Px(3), (float)Px(6), (float)Px(6));
        g_zones.push_back({H_CHIP, r, i});
        cx += w + Px(6);
      }
    }
    // menu dots
    RECT mr{W - pad - menuW + Px(4), mid - Px(13), W - pad + Px(4), mid + Px(13)};
    if (Hover(mr)) {
      Gdiplus::SolidBrush hb(GC(T.btnHover));
      RoundRect(g, &hb, (float)mr.left, (float)mr.top, (float)(mr.right - mr.left), (float)(mr.bottom - mr.top), (float)Px(7));
    }
    Gdiplus::SolidBrush db(GC(T.muted));
    for (int i = -1; i <= 1; i++) g.FillEllipse(&db, (float)(mr.left + mr.right) / 2 - Px(1.7f), (float)mid + i * Px(5.5) - Px(1.7f), (float)Px(3.4f), (float)Px(3.4f));
    g_zones.push_back({H_MENU, mr, 0});
  }

  // ── text (GDI, ClearType, font fallback for Bangla) ──
  RECT ringR{pad, mid - ringW / 2, pad + ringW, mid + ringW / 2};
  Text(mem, F.tiny, pctS, ringR, T.text, DT_CENTER);
  g_zones.push_back({H_DRAG, ringR, 0});

  if (showTitle) {
    RECT tr{x0, mid - Px(19), x0 + titleW, mid};
    Text(mem, F.title, S.title, tr, T.text, DT_LEFT | DT_END_ELLIPSIS);
    g_zones.push_back({H_TITLE, tr, 0});
    RECT cr{x0, mid + Px(1), x0 + titleW, mid + Px(19)};
    RECT nr{x0 + Px(12), cr.top, x0 + Px(12) + std::min(TextSize(mem, F.small, c.name).cx, titleW - Px(26)), cr.bottom};
    Text(mem, F.small, c.name, nr, Hover(cr) ? T.text : acc, DT_LEFT | DT_END_ELLIPSIS);
    g_zones.push_back({H_CAT, cr, 0});
  }
  int px0 = x0 + (showTitle ? titleW + gap : 0);
  RECT minus{px0, mid - btnD / 2, px0 + btnD, mid + btnD / 2};
  RECT plus{px0 + pagesW - btnD, mid - btnD / 2, px0 + pagesW, mid + btnD / 2};
  Text(mem, F.title, L"−", minus, T.text, DT_CENTER);
  Text(mem, F.title, L"+", plus, S.theme == 3 ? RGB(255, 255, 255) : RGB(10, 20, 30), DT_CENTER);
  g_zones.push_back({H_MINUS, minus, 0});
  g_zones.push_back({H_PLUS, plus, 0});
  {
    int inner = plus.left - minus.right;
    ISize dsz = TextSize(mem, F.big, doneS), tsz = TextSize(mem, F.small, targetS);
    int nx = minus.right + (inner - (dsz.cx + Px(4) + tsz.cx)) / 2;
    RECT dr{nx, mid - Px(24), nx + dsz.cx, mid + Px(2)};
    Text(mem, F.big, doneS, dr, complete ? RGB(250, 204, 21) : T.text, DT_LEFT);
    g_zones.push_back({H_DONE, dr, 0});
    RECT trr{dr.right + Px(4), mid - Px(20), dr.right + Px(4) + tsz.cx, mid + Px(1)};
    Text(mem, F.small, targetS, trr, Hover(trr) ? T.text : T.muted, DT_LEFT);
    g_zones.push_back({H_TARGET, trr, 0});
    RECT lr{minus.right, mid + Px(1), plus.left, mid + Px(17)};
    Text(mem, F.small, leftS, lr, complete ? RGB(250, 204, 21) : T.muted, DT_CENTER);
  }
  int cursor = px0 + pagesW + gap;
  if (showTimer) {
    RECT r{cursor, mid - Px(22), cursor + timerW, mid + Px(20)};
    bool hv = Hover(r);
    (void)hv;
    RECT tr{cursor + Px(20), mid - Px(20), cursor + timerW, mid};
    Text(mem, F.title, timeS, tr, g_running ? T.text : T.muted, DT_LEFT);
    RECT sr{cursor, mid + Px(1), cursor + timerW, mid + Px(18)};
    Text(mem, F.small, paceS, sr, T.muted, DT_LEFT);
    g_zones.push_back({H_TIMER, r, 0});
    cursor += timerW + gap;
  }
  if (showCd) {
    RECT r{cursor, mid - Px(20), cursor + cdW, mid};
    Text(mem, F.title, cdS, r, ex < 86400 ? RGB(251, 113, 133) : T.text, DT_LEFT);
    RECT sr{cursor, mid + Px(1), cursor + cdW, mid + Px(18)};
    Text(mem, F.small, cdSub, sr, T.muted, DT_LEFT);
    g_zones.push_back({H_COUNT, {cursor, mid - Px(22), cursor + cdW, mid + Px(20)}, 0});
  }
  for (auto& z : g_zones)
    if (z.hit == H_CHIP) {
      const Cat& k = S.cats[z.idx];
      RECT r = z.r;
      r.left += Px(18);
      Text(mem, F.tiny, k.name + Fmt(L"  %d/%d", k.done, k.target), r, T.text, DT_LEFT);
    }

  BitBlt(hdc, 0, 0, W, H, mem, 0, 0, SRCCOPY);
  SelectObject(mem, oldBmp);
  DeleteObject(bmp);
  DeleteDC(mem);
}

// ───────────────────────── input box ─────────────────────────
struct Prompt { std::wstring title, hint, value; bool numeric, ok, done; HWND edit; };
static Prompt* g_prompt = nullptr;
static WNDPROC g_editProc = nullptr;
static HBRUSH g_editBrush = nullptr;
static LRESULT CALLBACK EditSub(HWND h, UINT m, WPARAM w, LPARAM l) {
  if (m == WM_KEYDOWN && (w == VK_RETURN || w == VK_ESCAPE)) {
    if (g_prompt) {
      g_prompt->ok = (w == VK_RETURN);
      int n = GetWindowTextLengthW(h);
      std::wstring s(n, L'\0');
      GetWindowTextW(h, s.data(), n + 1);
      g_prompt->value = s;
      g_prompt->done = true;
    }
    return 0;
  }
  if (m == WM_CHAR && (w == VK_RETURN || w == VK_ESCAPE)) return 0;
  return CallWindowProcW(g_editProc, h, m, w, l);
}
static LRESULT CALLBACK PromptProc(HWND h, UINT m, WPARAM w, LPARAM l) {
  const Theme& T = THEMES[S.theme];
  switch (m) {
    case WM_PAINT: {
      PAINTSTRUCT ps;
      HDC dc = BeginPaint(h, &ps);
      RECT rc;
      GetClientRect(h, &rc);
      HBRUSH b = CreateSolidBrush(T.bg2);
      FillRect(dc, &rc, b);
      DeleteObject(b);
      EnsureFonts();
      RECT t{Px(14), Px(8), rc.right - Px(14), Px(30)};
      Text(dc, F.title, g_prompt ? g_prompt->title : L"", t, T.text, DT_LEFT);
      RECT hr{Px(14), rc.bottom - Px(24), rc.right - Px(14), rc.bottom - Px(6)};
      Text(dc, F.small, (g_prompt ? g_prompt->hint : L"") + L"   Enter = save  ·  Esc = cancel", hr, T.muted, DT_LEFT);
      EndPaint(h, &ps);
      return 0;
    }
    case WM_CTLCOLOREDIT: {
      HDC dc = (HDC)w;
      SetTextColor(dc, T.text);
      SetBkColor(dc, T.btn);
      if (!g_editBrush) g_editBrush = CreateSolidBrush(T.btn);
      return (LRESULT)g_editBrush;
    }
    case WM_ACTIVATE:
      if (LOWORD(w) == WA_INACTIVE && g_prompt && !g_prompt->done) { g_prompt->ok = false; g_prompt->done = true; }
      return 0;
    case WM_CLOSE:
      if (g_prompt) { g_prompt->ok = false; g_prompt->done = true; }
      return 0;
  }
  return DefWindowProcW(h, m, w, l);
}
static bool Ask(const std::wstring& title, const std::wstring& hint, std::wstring& value, bool numeric) {
  static bool reg = false;
  if (!reg) {
    WNDCLASSW wc{};
    wc.lpfnWndProc = PromptProc;
    wc.hInstance = g_inst;
    wc.lpszClassName = L"SOSprintPrompt";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    RegisterClassW(&wc);
    reg = true;
  }
  if (g_editBrush) { DeleteObject(g_editBrush); g_editBrush = nullptr; }
  Prompt p{title, hint, value, numeric, false, false, nullptr};
  g_prompt = &p;
  RECT wr;
  GetWindowRect(g_hwnd, &wr);
  int w = Px(320), h = Px(96);
  int x = wr.left, y = wr.bottom + Px(6);
  HMONITOR mon = MonitorFromWindow(g_hwnd, MONITOR_DEFAULTTONEAREST);
  MONITORINFO mi{sizeof mi};
  GetMonitorInfoW(mon, &mi);
  if (y + h > mi.rcWork.bottom) y = wr.top - h - Px(6);
  x = std::clamp(x, (int)mi.rcWork.left, (int)mi.rcWork.right - w);
  HWND dlg = CreateWindowExW(WS_EX_TOPMOST | WS_EX_TOOLWINDOW, L"SOSprintPrompt", title.c_str(), WS_POPUP | WS_BORDER, x, y, w, h, g_hwnd, nullptr, g_inst, nullptr);
  int corner = 2;
  DwmSetWindowAttribute(dlg, 33, &corner, sizeof corner);
  p.edit = CreateWindowExW(0, L"EDIT", value.c_str(), WS_CHILD | WS_VISIBLE | ES_AUTOHSCROLL | (numeric ? ES_NUMBER : 0), Px(14), Px(34), w - Px(28), Px(28), dlg, nullptr, g_inst, nullptr);
  EnsureFonts();
  SendMessageW(p.edit, WM_SETFONT, (WPARAM)F.title, TRUE);
  g_editProc = (WNDPROC)SetWindowLongPtrW(p.edit, GWLP_WNDPROC, (LONG_PTR)EditSub);
  ShowWindow(dlg, SW_SHOW);
  SetForegroundWindow(dlg);
  SetFocus(p.edit);
  SendMessageW(p.edit, EM_SETSEL, 0, -1);
  MSG msg;
  while (!p.done && GetMessageW(&msg, nullptr, 0, 0)) {
    TranslateMessage(&msg);
    DispatchMessageW(&msg);
  }
  DestroyWindow(dlg);
  g_prompt = nullptr;
  if (p.ok) value = p.value;
  return p.ok;
}

// ───────────────────────── actions ─────────────────────────
static void Redraw() { InvalidateRect(g_hwnd, nullptr, FALSE); }
static void Changed() { Save(); Redraw(); }
static void ApplyWindowStyle() {
  LONG_PTR ex = GetWindowLongPtrW(g_hwnd, GWL_EXSTYLE);
  if (S.opacity < 100) {
    SetWindowLongPtrW(g_hwnd, GWL_EXSTYLE, ex | WS_EX_LAYERED);
    SetLayeredWindowAttributes(g_hwnd, 0, (BYTE)(S.opacity * 255 / 100), LWA_ALPHA);
  } else if (ex & WS_EX_LAYERED) {
    SetWindowLongPtrW(g_hwnd, GWL_EXSTYLE, ex & ~WS_EX_LAYERED);
  }
  SetWindowPos(g_hwnd, S.topmost ? HWND_TOPMOST : HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_FRAMECHANGED);
  BOOL dark = S.theme != 3;
  DwmSetWindowAttribute(g_hwnd, 20, &dark, sizeof dark);  // DWMWA_USE_IMMERSIVE_DARK_MODE
  COLORREF border = THEMES[S.theme].track;
  DwmSetWindowAttribute(g_hwnd, 34, &border, sizeof border);  // DWMWA_BORDER_COLOR
}
static void Resize() {
  RECT r;
  GetWindowRect(g_hwnd, &r);
  SetWindowPos(g_hwnd, nullptr, 0, 0, S.width, Height(), SWP_NOMOVE | SWP_NOZORDER | SWP_NOACTIVATE);
}
static void SwitchCat(int i) {
  if (S.cats.empty()) return;
  S.cur = ((i % (int)S.cats.size()) + (int)S.cats.size()) % (int)S.cats.size();
  g_sessionSecs = 0;
  g_sessionStartDone = C().done;
  Changed();
}
static void AddPages(int d) {
  C().done = std::max(0, C().done + d);
  if (!g_running && d > 0 && g_sessionSecs == 0) g_sessionStartDone = C().done - d;
  Changed();
}
static void ToggleTimer() {
  g_running = !g_running;
  g_lastTick = GetTickCount64();
  if (g_running && g_sessionSecs == 0) g_sessionStartDone = C().done;
  Redraw();
}
static bool SetStartup(bool on) {
  HKEY k;
  if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE | KEY_QUERY_VALUE, &k) != ERROR_SUCCESS) return false;
  if (on) {
    wchar_t path[MAX_PATH];
    GetModuleFileNameW(nullptr, path, MAX_PATH);
    std::wstring v = L"\"" + std::wstring(path) + L"\"";
    RegSetValueExW(k, L"SOSprintWidget", 0, REG_SZ, (const BYTE*)v.c_str(), (DWORD)((v.size() + 1) * sizeof(wchar_t)));
  } else {
    RegDeleteValueW(k, L"SOSprintWidget");
  }
  RegCloseKey(k);
  return true;
}
static bool IsStartup() {
  HKEY k;
  if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_QUERY_VALUE, &k) != ERROR_SUCCESS) return false;
  bool on = RegQueryValueExW(k, L"SOSprintWidget", nullptr, nullptr, nullptr, nullptr) == ERROR_SUCCESS;
  RegCloseKey(k);
  return on;
}
static void EditTitle() {
  std::wstring v = S.title;
  if (Ask(L"Widget title", L"Any text, e.g. SO Written · 27 Nov", v, false) && !v.empty()) { S.title = v.substr(0, 60); Changed(); }
}
static void EditDone() {
  std::wstring v = std::to_wstring(C().done);
  if (Ask(L"Pages completed — " + C().name, L"Type the page you finished", v, true) && !v.empty()) { C().done = std::clamp(_wtoi(v.c_str()), 0, 100000); Changed(); }
}
static void EditTarget() {
  std::wstring v = std::to_wstring(C().target);
  if (Ask(L"Target pages — " + C().name, L"Total pages you plan to read", v, true) && !v.empty()) { C().target = std::clamp(_wtoi(v.c_str()), 1, 100000); Changed(); }
}
static void AddCat() {
  std::wstring v = L"";
  if (!Ask(L"New category", L"e.g. Bangla Grammar", v, false) || v.empty()) return;
  std::wstring t = L"100";
  Ask(L"Target pages — " + v, L"Total pages", t, true);
  S.cats.push_back({v.substr(0, 40), 0, std::max(1, _wtoi(t.c_str()))});
  SwitchCat((int)S.cats.size() - 1);
}
static void RenameCat() {
  std::wstring v = C().name;
  if (Ask(L"Rename category", L"New name", v, false) && !v.empty()) { C().name = v.substr(0, 40); Changed(); }
}
static void DeleteCat() {
  if (S.cats.size() <= 1) return;
  std::wstring msg = L"Delete \"" + C().name + L"\" and its progress?";
  if (MessageBoxW(g_hwnd, msg.c_str(), L"SO Sprint", MB_YESNO | MB_ICONQUESTION | MB_TOPMOST) != IDYES) return;
  S.cats.erase(S.cats.begin() + S.cur);
  SwitchCat(std::min(S.cur, (int)S.cats.size() - 1));
}

enum {
  M_TITLE = 100, M_DONE, M_TARGET, M_ADDCAT, M_RENCAT, M_DELCAT, M_RESETCAT, M_RESETTIME, M_TIMER, M_TOP, M_CD, M_LOCK, M_START,
  M_HIDE, M_EXIT, M_BIGGER, M_SMALLER, M_HELP, M_CAT0 = 200, M_THEME0 = 300, M_OP0 = 400
};
static void ShowHelp() {
  MessageBoxW(g_hwnd,
              L"SO Sprint Widget — quick guide\n\n"
              L"• +  /  −  or mouse wheel over the numbers: pages done (Shift = ±5)\n"
              L"• Click the big number to type the page; click \"/ target\" to set the target\n"
              L"• Click the category (▾) or a chip to switch; wheel over it to cycle\n"
              L"• Click the timer to start/pause reading time; pace and ETA appear after 5 min\n"
              L"• Drag empty space or the ring to move; drag the left/right edge to widen\n"
              L"• Ctrl + wheel: whole widget bigger/smaller\n"
              L"• Right-click or ⋮ for themes, opacity, categories, startup\n"
              L"• Tray icon: click to show/hide\n\n"
              L"Data: %APPDATA%\\SOSprintWidget\\settings.ini",
              L"SO Sprint Widget", MB_OK | MB_ICONINFORMATION | MB_TOPMOST);
}
static void Menu(POINT screen) {
  HMENU m = CreatePopupMenu(), cats = CreatePopupMenu(), theme = CreatePopupMenu(), op = CreatePopupMenu();
  for (int i = 0; i < (int)S.cats.size(); i++) {
    std::wstring s = S.cats[i].name + Fmt(L"\t%d/%d", S.cats[i].done, S.cats[i].target);
    AppendMenuW(cats, MF_STRING | (i == S.cur ? MF_CHECKED : 0), M_CAT0 + i, s.c_str());
  }
  AppendMenuW(cats, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(cats, MF_STRING, M_ADDCAT, L"Add category…");
  AppendMenuW(cats, MF_STRING, M_RENCAT, L"Rename current…");
  AppendMenuW(cats, MF_STRING | (S.cats.size() > 1 ? 0 : MF_GRAYED), M_DELCAT, L"Delete current");
  AppendMenuW(cats, MF_STRING, M_RESETCAT, L"Reset current to 0 pages");
  for (int i = 0; i < 4; i++) AppendMenuW(theme, MF_STRING | (i == S.theme ? MF_CHECKED : 0), M_THEME0 + i, THEMES[i].name);
  for (int v : {100, 90, 80, 70, 60}) AppendMenuW(op, MF_STRING | (v == S.opacity ? MF_CHECKED : 0), M_OP0 + v, Fmt(L"%d%%", v).c_str());
  AppendMenuW(m, MF_STRING, M_DONE, L"Set pages done…");
  AppendMenuW(m, MF_STRING, M_TARGET, L"Set target…");
  AppendMenuW(m, MF_POPUP, (UINT_PTR)cats, L"Category");
  AppendMenuW(m, MF_STRING, M_TITLE, L"Edit title…");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_STRING, M_TIMER, g_running ? L"Pause timer\tSpace" : L"Start timer\tSpace");
  AppendMenuW(m, MF_STRING, M_RESETTIME, L"Reset session timer");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_POPUP, (UINT_PTR)theme, L"Theme");
  AppendMenuW(m, MF_POPUP, (UINT_PTR)op, L"Opacity");
  AppendMenuW(m, MF_STRING, M_BIGGER, L"Bigger\tCtrl+Wheel");
  AppendMenuW(m, MF_STRING, M_SMALLER, L"Smaller");
  AppendMenuW(m, MF_STRING | (S.topmost ? MF_CHECKED : 0), M_TOP, L"Always on top");
  AppendMenuW(m, MF_STRING | (S.countdown ? MF_CHECKED : 0), M_CD, L"Show exam countdown");
  AppendMenuW(m, MF_STRING | (S.locked ? MF_CHECKED : 0), M_LOCK, L"Lock position and width");
  AppendMenuW(m, MF_STRING | (IsStartup() ? MF_CHECKED : 0), M_START, L"Start with Windows");
  AppendMenuW(m, MF_SEPARATOR, 0, nullptr);
  AppendMenuW(m, MF_STRING, M_HELP, L"How to use");
  AppendMenuW(m, MF_STRING, M_HIDE, L"Hide to tray");
  AppendMenuW(m, MF_STRING, M_EXIT, L"Exit");
  SetForegroundWindow(g_hwnd);
  int cmd = TrackPopupMenu(m, TPM_RETURNCMD | TPM_RIGHTBUTTON, screen.x, screen.y, 0, g_hwnd, nullptr);
  DestroyMenu(m);
  if (!cmd) return;
  if (cmd >= M_CAT0 && cmd < M_CAT0 + 100) SwitchCat(cmd - M_CAT0);
  else if (cmd >= M_THEME0 && cmd < M_THEME0 + 4) { S.theme = cmd - M_THEME0; ApplyWindowStyle(); Changed(); }
  else if (cmd >= M_OP0 && cmd <= M_OP0 + 100) { S.opacity = cmd - M_OP0; ApplyWindowStyle(); Changed(); }
  else switch (cmd) {
      case M_TITLE: EditTitle(); break;
      case M_DONE: EditDone(); break;
      case M_TARGET: EditTarget(); break;
      case M_ADDCAT: AddCat(); break;
      case M_RENCAT: RenameCat(); break;
      case M_DELCAT: DeleteCat(); break;
      case M_RESETCAT:
        if (MessageBoxW(g_hwnd, (L"Reset \"" + C().name + L"\" to 0 pages and 0 time?").c_str(), L"SO Sprint", MB_YESNO | MB_TOPMOST) == IDYES) {
          C().done = 0; C().secs = 0; g_sessionSecs = 0; g_sessionStartDone = 0; Changed();
        }
        break;
      case M_RESETTIME: g_sessionSecs = 0; g_sessionStartDone = C().done; Redraw(); break;
      case M_TIMER: ToggleTimer(); break;
      case M_TOP: S.topmost = !S.topmost; ApplyWindowStyle(); Changed(); break;
      case M_CD: S.countdown = !S.countdown; Changed(); break;
      case M_LOCK: S.locked = !S.locked; Changed(); break;
      case M_START: SetStartup(!IsStartup()); break;
      case M_BIGGER: S.zoom = std::min(1.8, S.zoom + 0.1); Resize(); Changed(); break;
      case M_SMALLER: S.zoom = std::max(0.8, S.zoom - 0.1); Resize(); Changed(); break;
      case M_HELP: ShowHelp(); break;
      case M_HIDE: ShowWindow(g_hwnd, SW_HIDE); break;
      case M_EXIT: DestroyWindow(g_hwnd); break;
    }
}

// ───────────────────────── window procedure ─────────────────────────
static LRESULT CALLBACK WndProc(HWND h, UINT m, WPARAM w, LPARAM l) {
  switch (m) {
    case WM_NCCALCSIZE:
      if (w) return 0;  // client area = whole window (keeps DWM shadow and rounded corners)
      break;
    case WM_NCHITTEST: {
      POINT p{GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      ScreenToClient(h, &p);
      RECT rc;
      GetClientRect(h, &rc);
      int edge = Px(6);
      if (!S.locked) {
        if (p.x < edge) return HTLEFT;
        if (p.x >= rc.right - edge) return HTRIGHT;
      }
      const Zone* z = ZoneAt(p);
      if (z && z->hit != H_DRAG) return HTCLIENT;
      return S.locked ? HTCLIENT : HTCAPTION;
    }
    case WM_GETMINMAXINFO: {
      auto* mm = (MINMAXINFO*)l;
      mm->ptMinTrackSize = {Px(240), Height()};
      mm->ptMaxTrackSize = {Px(1800), Height()};
      return 0;
    }
    case WM_SIZE:
      if (w != SIZE_MINIMIZED) { RECT r; GetWindowRect(h, &r); S.width = r.right - r.left; Redraw(); }
      return 0;
    case WM_EXITSIZEMOVE: {
      RECT r;
      GetWindowRect(h, &r);
      S.x = r.left; S.y = r.top; S.width = r.right - r.left;
      Save();
      return 0;
    }
    case WM_DPICHANGED: {
      g_dpi = HIWORD(w);
      F.dpiKey = 0;
      RECT* r = (RECT*)l;
      SetWindowPos(h, nullptr, r->left, r->top, r->right - r->left, Height(), SWP_NOZORDER | SWP_NOACTIVATE);
      return 0;
    }
    case WM_ERASEBKGND: return 1;
    case WM_PAINT: {
      PAINTSTRUCT ps;
      HDC dc = BeginPaint(h, &ps);
      Paint(h, dc);
      EndPaint(h, &ps);
      return 0;
    }
    case WM_MOUSEMOVE: {
      g_mouse = {GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      if (!g_tracking) { TRACKMOUSEEVENT t{sizeof t, TME_LEAVE, h, 0}; TrackMouseEvent(&t); g_tracking = true; }
      const Zone* z = ZoneAt(g_mouse);
      SetCursor(LoadCursor(nullptr, z && z->hit != H_DRAG ? IDC_HAND : IDC_ARROW));
      Redraw();
      return 0;
    }
    case WM_MOUSELEAVE: g_mouse = {-1, -1}; g_tracking = false; Redraw(); return 0;
    case WM_SETCURSOR:
      if (LOWORD(l) == HTCLIENT) return TRUE;
      break;
    case WM_LBUTTONUP: {
      POINT p{GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      const Zone* z = ZoneAt(p);
      if (!z) return 0;
      bool shift = GetKeyState(VK_SHIFT) < 0;
      switch (z->hit) {
        case H_PLUS: AddPages(shift ? 5 : 1); break;
        case H_MINUS: AddPages(shift ? -5 : -1); break;
        case H_DONE: EditDone(); break;
        case H_TARGET: EditTarget(); break;
        case H_TITLE: EditTitle(); break;
        case H_CAT: SwitchCat(S.cur + 1); break;
        case H_CHIP: SwitchCat(z->idx); break;
        case H_TIMER: ToggleTimer(); break;
        case H_MENU: { POINT s = p; ClientToScreen(h, &s); Menu(s); break; }
        default: break;
      }
      return 0;
    }
    case WM_MOUSEWHEEL: {
      int d = GET_WHEEL_DELTA_WPARAM(w) > 0 ? 1 : -1;
      if (GET_KEYSTATE_WPARAM(w) & MK_CONTROL) {
        S.zoom = std::clamp(S.zoom + d * 0.1, 0.8, 1.8);
        Resize();
        Changed();
        return 0;
      }
      POINT p{GET_X_LPARAM(l), GET_Y_LPARAM(l)};
      ScreenToClient(h, &p);
      const Zone* z = ZoneAt(p);
      if (z && (z->hit == H_CAT || z->hit == H_CHIP || z->hit == H_TITLE)) SwitchCat(S.cur - d);
      else AddPages(d * ((GET_KEYSTATE_WPARAM(w) & MK_SHIFT) ? 5 : 1));
      return 0;
    }
    case WM_KEYDOWN:
      if (w == VK_ADD || w == VK_OEM_PLUS || w == VK_UP) AddPages(1);
      else if (w == VK_SUBTRACT || w == VK_OEM_MINUS || w == VK_DOWN) AddPages(-1);
      else if (w == VK_SPACE) ToggleTimer();
      else if (w == VK_LEFT) SwitchCat(S.cur - 1);
      else if (w == VK_RIGHT) SwitchCat(S.cur + 1);
      return 0;
    case WM_RBUTTONUP: { POINT s{GET_X_LPARAM(l), GET_Y_LPARAM(l)}; ClientToScreen(h, &s); Menu(s); return 0; }
    case WM_NCRBUTTONUP: { POINT s{GET_X_LPARAM(l), GET_Y_LPARAM(l)}; Menu(s); return 0; }
    case WM_NCLBUTTONDBLCLK: return 0;  // never maximise
    case WM_CONTEXTMENU: return 0;
    case WM_TIMER:
      if (w == TIMER_TICK) {
        ULONGLONG now = GetTickCount64();
        if (g_running) {
          ULONGLONG ms = now - g_lastTick;
          if (ms >= 1000) {
            long long s = (long long)(ms / 1000);
            g_sessionSecs += s;
            C().secs += s;
            g_lastTick += s * 1000;
            if (g_sessionSecs % 60 == 0) Save();
          }
        } else g_lastTick = now;
        Redraw();
      } else if (w == TIMER_TOP && S.topmost && IsWindowVisible(h)) {
        SetWindowPos(h, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE);
      }
      return 0;
    case WM_TRAY:
      if (LOWORD(l) == WM_LBUTTONUP) { ShowWindow(h, IsWindowVisible(h) ? SW_HIDE : SW_SHOWNOACTIVATE); }
      else if (LOWORD(l) == WM_RBUTTONUP) { POINT s; GetCursorPos(&s); Menu(s); }
      return 0;
    case WM_DESTROY:
      Save();
      Shell_NotifyIconW(NIM_DELETE, &g_nid);
      PostQuitMessage(0);
      return 0;
  }
  return DefWindowProcW(h, m, w, l);
}

// ───────────────────────── entry ─────────────────────────
typedef BOOL(WINAPI* SetDpiCtx)(HANDLE);
int WINAPI wWinMain(HINSTANCE inst, HINSTANCE, PWSTR, int) {
  g_inst = inst;
  HANDLE single = CreateMutexW(nullptr, TRUE, L"SOSprintWidget.Single");
  if (GetLastError() == ERROR_ALREADY_EXISTS) {
    HWND other = FindWindowW(L"SOSprintWidget", nullptr);
    if (other) { ShowWindow(other, SW_SHOWNOACTIVATE); SetWindowPos(other, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE); }
    return 0;
  }
  if (auto f = (SetDpiCtx)GetProcAddress(GetModuleHandleW(L"user32"), "SetProcessDpiAwarenessContext")) f((HANDLE)-4);  // per-monitor v2
  Gdiplus::GdiplusStartupInput gin;
  Gdiplus::GdiplusStartup(&g_gdipToken, &gin, nullptr);
  Load();

  WNDCLASSEXW wc{sizeof wc};
  wc.style = CS_HREDRAW | CS_VREDRAW;
  wc.lpfnWndProc = WndProc;
  wc.hInstance = inst;
  wc.hIcon = LoadIconW(inst, MAKEINTRESOURCEW(IDI_APP));
  wc.hIconSm = wc.hIcon;
  wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
  wc.lpszClassName = L"SOSprintWidget";
  RegisterClassExW(&wc);

  POINT pt{0, 0};
  HMONITOR mon = MonitorFromPoint(pt, MONITOR_DEFAULTTOPRIMARY);
  typedef HRESULT(WINAPI * GetDpiMon)(HMONITOR, int, UINT*, UINT*);
  HMODULE shcore = LoadLibraryW(L"shcore.dll");
  UINT dx = 96, dy = 96;
  if (shcore) if (auto gd = (GetDpiMon)GetProcAddress(shcore, "GetDpiForMonitor")) gd(mon, 0, &dx, &dy);
  g_dpi = (int)dx;
  MONITORINFO mi{sizeof mi};
  GetMonitorInfoW(mon, &mi);
  int W = std::clamp(S.width, Px(240), Px(1800)), H = Height();
  int X = S.x, Y = S.y;
  RECT virt{GetSystemMetrics(SM_XVIRTUALSCREEN), GetSystemMetrics(SM_YVIRTUALSCREEN), GetSystemMetrics(SM_XVIRTUALSCREEN) + GetSystemMetrics(SM_CXVIRTUALSCREEN),
            GetSystemMetrics(SM_YVIRTUALSCREEN) + GetSystemMetrics(SM_CYVIRTUALSCREEN)};
  if (X < virt.left - W / 2 || X > virt.right - 40 || Y < virt.top || Y > virt.bottom - 20) {  // first run or off-screen: top centre
    X = mi.rcWork.left + (mi.rcWork.right - mi.rcWork.left - W) / 2;
    Y = mi.rcWork.top + Px(8);
  }
  g_hwnd = CreateWindowExW(WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE | (S.topmost ? WS_EX_TOPMOST : 0), L"SOSprintWidget", L"SO Sprint Widget",
                           WS_POPUP | WS_THICKFRAME, X, Y, W, H, nullptr, nullptr, inst, nullptr);
  int corner = 2;  // DWMWCP_ROUND
  DwmSetWindowAttribute(g_hwnd, 33, &corner, sizeof corner);
  MARGINS mg{0, 0, 1, 0};
  DwmExtendFrameIntoClientArea(g_hwnd, &mg);
  ApplyWindowStyle();
  SetWindowPos(g_hwnd, nullptr, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED | SWP_NOACTIVATE);
  ShowWindow(g_hwnd, SW_SHOWNOACTIVATE);
  g_sessionStartDone = C().done;
  g_lastTick = GetTickCount64();
  SetTimer(g_hwnd, TIMER_TICK, 250, nullptr);
  SetTimer(g_hwnd, TIMER_TOP, 2000, nullptr);

  g_nid.cbSize = sizeof g_nid;
  g_nid.hWnd = g_hwnd;
  g_nid.uID = 1;
  g_nid.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP;
  g_nid.uCallbackMessage = WM_TRAY;
  g_nid.hIcon = wc.hIcon;
  wcscpy(g_nid.szTip, L"SO Sprint Widget — click to show/hide");
  Shell_NotifyIconW(NIM_ADD, &g_nid);

  MSG msg;
  while (GetMessageW(&msg, nullptr, 0, 0)) {
    TranslateMessage(&msg);
    DispatchMessageW(&msg);
  }
  Gdiplus::GdiplusShutdown(g_gdipToken);
  if (single) CloseHandle(single);
  return 0;
}
