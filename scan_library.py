import os
import re
import json

SONGS_DIR = "/Users/dougkeel/Library/CloudStorage/GoogleDrive-dougkeel@gmail.com/My Drive/OnSong"
OUTPUT_JSON = "chords.json"

# A basic seed database of standard shapes to get us started
BASE_SEEDS = {
    "C": [{"frets": ["x", 3, 2, 0, 1, 0]}],
    "G": [{"frets": [3, 2, 0, 0, 0, 3]}],
    "D": [{"frets": ["x", "x", 0, 2, 3, 2]}],
    "A": [{"frets": ["x", 0, 2, 2, 2, 0]}],
    "E": [{"frets": [0, 2, 2, 1, 0, 0]}],
    "Am": [{"frets": ["x", 0, 2, 2, 1, 0]}],
    "Em": [{"frets": [0, 2, 2, 0, 0, 0]}],
    "Dm": [{"frets": ["x", "x", 0, 2, 3, 1]}],
    "Emaj7": [{"frets": [0, 2, 1, 1, 0, 0]}]
}

def scan_all_chords():
    print(f"Reading through files in {SONGS_DIR}...")
    unique_chords = set()
    
    # Regex rules to spot chords on dedicated chord lines or in brackets
    chord_signature = re.compile(r'\b[A-G][a-zA-Z0-9#+]*\b')
    
    if not os.path.exists(SONGS_DIR):
        print("Folder not found.")
        return

    for filename in os.listdir(SONGS_DIR):
        if filename.lower().endswith('.txt'):
            filepath = os.path.join(SONGS_DIR, filename)
            for encoding in ['utf-8', 'mac-roman', 'latin-1']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        for line in f:
                            trimmed = line.strip()
                            # Skip block headers
                            if not trimmed or any(trimmed.startswith(h) for h in ["Verse", "Chorus", "Bridge", "Key", "Tuning"]):
                                continue
                            
                            # Test if line looks purely like a chord row
                            tokens = trimmed.split()
                            is_chord_line = all(re.match(r'^[A-G][a-zA-Z0-9#+]*$', t) for t in tokens)
                            
                            if is_chord_line:
                                for token in tokens:
                                    unique_chords.add(token)
                    break
                except UnicodeDecodeError:
                    continue
                except Exception:
                    break

    print(f"\n🎉 Discovery Complete! Found {len(unique_chords)} unique chords across your songs.")
    
    # Build or update the chords.json layout mapping
    master_chord_store = {}
    for chord in sorted(unique_chords):
        # If we have a fallback seed shape, use it, otherwise leave an empty variation array
        master_chord_store[chord] = BASE_SEEDS.get(chord, [{"frets": ["x", "x", "x", "x", "x", "x"], "baseFret": 1}])
        
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as json_file:
        json.dump(master_chord_store, json_file, indent=2)
        
    print(f"💾 Master blueprint successfully written to local file: '{OUTPUT_JSON}'")

if __name__ == '__main__':
    scan_all_chords()