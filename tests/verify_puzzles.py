#!/usr/bin/env python3
"""docs/17-এর প্রতিটি পাজলের ঠিক একটি সমাধান আছে কি না, সব সম্ভাবনা মিলিয়ে যাচাই। চালান: python3 tests/verify_puzzles.py"""
from itertools import permutations, combinations
import sys

def sols(names, n, cond):
    return [dict(zip(names, p)) for p in permutations(range(1, n + 1), len(names)) if cond(dict(zip(names, p)))]

P = {
    "June 2026 interview": (sols("ABCDE", 5, lambda d: d['A'] < d['C'] and d['B'] not in (1, 5) and d['D'] == d['B'] + 1 and not d['E'] < d['A'] and d['C'] == 5 and d['E'] == 2), {'A': 1, 'E': 2, 'B': 3, 'D': 4, 'C': 5}),
    "Seating Amin…Faria": (sols(["Amin", "Bina", "Cyrus", "Dipa", "Emon", "Faria"], 6, lambda d: d['Dipa'] == 4 and d['Bina'] == d['Amin'] + 1 and d['Faria'] in (1, 6) and abs(d['Cyrus'] - d['Dipa']) != 1 and d['Emon'] > d['Dipa'] and d['Bina'] not in (1, 6) and d['Faria'] > d['Emon']), {'Cyrus': 1, 'Amin': 2, 'Bina': 3, 'Dipa': 4, 'Emon': 5, 'Faria': 6}),
    "Floors": (sols(["Credit", "Treasury", "IT", "HR", "Audit"], 5, lambda d: d['IT'] == d['HR'] + 1 and d['Audit'] % 2 == 0 and d['Credit'] < d['Treasury'] and d['HR'] != 1 and d['Treasury'] != 5), {'Credit': 1, 'Audit': 2, 'Treasury': 3, 'HR': 4, 'IT': 5}),
    "Practice 1": (sols("KLMNOP", 6, lambda d: d['M'] == 3 and d['K'] < d['M'] and d['P'] == d['K'] + 1 and d['O'] == d['M'] + 1 and d['N'] > d['O'] and d['L'] != 6), {'K': 1, 'P': 2, 'M': 3, 'O': 4, 'L': 5, 'N': 6}),
    "Practice 2": (sols(["Uttara", "Motijheel", "Gulshan", "Dhanmondi", "Banani"], 5, lambda d: d['Motijheel'] == 1 and d['Gulshan'] < d['Banani'] and d['Dhanmondi'] == d['Gulshan'] + 1 and d['Uttara'] not in (2, 5)), {'Motijheel': 1, 'Gulshan': 2, 'Dhanmondi': 3, 'Uttara': 4, 'Banani': 5}),
    "Practice 3": (sols("QRSTU", 5, lambda d: d['S'] == 3 and abs(d['Q'] - d['R']) == 1 and d['T'] < d['S'] and abs(d['U'] - d['S']) == 1 and d['U'] != 5 and d['Q'] > d['S'] and d['R'] in (1, 5)), {'T': 1, 'U': 2, 'S': 3, 'Q': 4, 'R': 5}),
    "Practice 4": (sols(["Rina", "Sohel", "Tania", "Ujjal", "Wasi", "Yasmin"], 6, lambda d: d['Yasmin'] == 4 and d['Tania'] == d['Rina'] + 2 and d['Sohel'] in (1, 6) and d['Wasi'] < d['Ujjal'] and d['Rina'] != 1 and d['Ujjal'] != 6), {'Wasi': 1, 'Ujjal': 2, 'Rina': 3, 'Yasmin': 4, 'Tania': 5, 'Sohel': 6}),
}
team = [set(c) for c in combinations("GHIJKLM", 4) if (lambda s: 'M' in s and ('G' not in s or 'H' in s) and not {'I', 'J'} <= s and ('K' not in s or 'L' in s) and (('H' in s) != ('K' in s)) and 'L' not in s and ('J' not in s or 'L' in s))(set(c))]
proj = [set(c) for c in combinations("ABCDEF", 3) if (lambda s: (('A' in s) != ('B' in s)) and ('C' not in s or 'D' in s) and 'E' not in s and ('F' in s or 'D' in s) and ('D' not in s or 'A' in s) and 'C' in s)(set(c))]
bad = 0
for name, (r, want) in P.items():
    good = len(r) == 1 and r[0] == want
    bad += not good
    print(("✓ " if good else "✗ ") + name, len(r))
for name, r, want in (("Team G,H,I,M", team, {'G', 'H', 'I', 'M'}), ("Projects A,C,D", proj, {'A', 'C', 'D'})):
    good = len(r) == 1 and r[0] == want
    bad += not good
    print(("✓ " if good else "✗ ") + name, len(r))
sys.exit(1 if bad else 0)
