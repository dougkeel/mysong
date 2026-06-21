import os
import re
import json
from collections import Counter

SONGS_DIR = "/Users/dougkeel/Library/CloudStorage/GoogleDrive-dougkeel@gmail.com/My Drive/OnSong"
CHORDS_JSON = "chords.json"

STRICT_CHORD_RULES = re.compile(r'^[A-G][b#]?(m|min|maj|maj7|M7|7M|m7|7|sus2|sus4|sus|dim|dim7|aug|6/9|69|6|m6|4|9|m9|maj9|add9|5|11|m11|7sus4|add11|\+)?(/[A-G][b#]?)?$', re.IGNORECASE)
VOCAL_BLACKLIST = ["da", "do", "bam", "ahh", "ba", "di", "ah", "la", "oh", "oooh", "aaah", "chorus", "verse", "bridge", "intro", "outro", "solo", "instrumental"]

def run_library_audit():
    print("📋 Running Aligned Global Library Audit...")
    
    if not os.path.exists(CHORDS_JSON):
        return
        
    with open(CHORDS_JSON, 'r', encoding='utf-8') as f:
        current_chords = set(json.load(f).keys())

    all_raw_tokens = []
    
    for filename in os.listdir(SONGS_DIR):
        if filename.lower().endswith('.txt'):
            filepath = os.path.join(SONGS_DIR, filename)
            for encoding in ['utf-8', 'mac-roman', 'latin-1']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        for line in f:
                            trimmed = line.strip()
                            if not trimmed or any(trimmed.startswith(h) for h in ["Verse", "Chorus", "Bridge", "Key", "Tuning", "Intro"]):
                                continue
                            
                            tokens = re.split(r'[\s\[\]\-]+', trimmed)
                            if all(re.match(r'^[A-G][A-Za-z0-9#+\/\-,\.]*$', t, re.IGNORECASE) for t in tokens if t):
                                all_raw_tokens.extend([t for t in tokens if t])
                    break
                except Exception: continue

    unmapped_counter = Counter()
    for token in all_raw_tokens:
        clean_token = token.strip()
        if clean_token and clean_token not in current_chords and clean_token.lower() not in VOCAL_BLACKLIST:
            unmapped_counter[clean_token] += 1

    exotic_candidates = []
    text_noise_candidates = []

    for token, count in unmapped_counter.most_common():
        if any(char in token for char in [',', '.', '(', ')']) and not '/' in token:
            text_noise_candidates.append((token, count, "Trailing Punctuation"))
        elif token.lower() in ['david', 'bowie', 'abba', 'coldplay', 'genesis', 'bob', 'dylan']:
            text_noise_candidates.append((token, count, "Metadata Header Line"))
        elif STRICT_CHORD_RULES.match(token):
            exotic_candidates.append((token, count))
        else:
            text_noise_candidates.append((token, count, "Ambiguous Noise"))

    print("\n=======================================================")
    print("             📊 FINAL GLOBAL AUDIT RESULTS             ")
    print("=======================================================")
    print(f"\n🔥 GENUINE MISSING CHORDS ({len(exotic_candidates)} total):")
    if not exotic_candidates:
        print("  ✅ 0 missing! Your chord store handles 100% of your library configurations.")
    else:
        for chord, count in exotic_candidates[:15]:
            print(f"  • {chord:<12} (appears {count} times)")

    print(f"\n🧹 SPOTTED GENUINE TEXT NOISE IN FILES ({len(text_noise_candidates)} total):")
    if not text_noise_candidates:
        print("  ✅ 0 text noise flags! Your files are completely optimized.")
    else:
        for token, count, reason in text_noise_candidates[:10]:
            print(f"  • {token:<12} (appears {count} times) -> [{reason}]")
    print("=======================================================\n")

if __name__ == '__main__':
    run_library_audit()