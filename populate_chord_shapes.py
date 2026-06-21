import os
import re
import json

SONGS_DIR = "/Users/dougkeel/Library/CloudStorage/GoogleDrive-dougkeel@gmail.com/My Drive/OnSong"
OUTPUT_FILE = "chords.json"

CHORD_REGEX = re.compile(r'^([A-G][b#]?)(m|min|maj|maj7|M7|7M|m7|7|sus2|sus4|sus|dim|dim7|aug|6/9|69|6|m6|4|9|m9|maj9|add9|5|11|m11|7sus4|add11|\+)?(/[A-G][b#]?)?$', re.IGNORECASE)

ROOT_OFFSETS = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 
    'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

VOCAL_BLACKLIST = ["da", "do", "bam", "ahh", "ba", "di", "ah", "la", "oh", "oooh", "aaah"]

def generate_movable_shapes(root, modifier):
    offset = ROOT_OFFSETS.get(root.upper(), 0)
    variations = []
    
    raw_mod = modifier or ""
    if raw_mod in ["M7", "7M"]: raw_mod = "maj7"
    
    mod = raw_mod.lower()
    if mod == "min": mod = "m"
    if mod in ["sus", "sus4", "4"]: mod = "sus4"
    if mod == "+": mod = "aug"
    if mod == "maj": mod = ""

    # --- VOICE 1: Low E-String Root ---
    e_fret = offset - 4
    if e_fret < 0: e_fret += 12
    
    if e_fret == 0:
        if mod == "": variations.append({"frets": [0, 2, 2, 1, 0, 0], "baseFret": 1})
        elif mod == "m": variations.append({"frets": [0, 2, 2, 0, 0, 0], "baseFret": 1})
        elif mod == "7": variations.append({"frets": [0, 2, 0, 1, 0, 0], "baseFret": 1})
        elif mod == "m7": variations.append({"frets": [0, 2, 0, 0, 0, 0], "baseFret": 1})
        elif mod == "maj7": variations.append({"frets": [0, 1, 1, 1, 0, 0], "baseFret": 1})
        elif mod == "sus4": variations.append({"frets": [0, 2, 2, 2, 0, 0], "baseFret": 1})
        elif mod == "sus2": variations.append({"frets": [0, 2, 4, 4, 0, 0], "baseFret": 1})
        elif mod == "6": variations.append({"frets": [0, 2, 2, 1, 2, 0], "baseFret": 1})
        elif mod == "5": variations.append({"frets": [0, 2, 2, "x", "x", "x"], "baseFret": 1})
        elif mod == "m9": variations.append({"frets": [0, 2, 0, 0, 0, 2], "baseFret": 1})
        elif mod == "aug": variations.append({"frets": [0, 3, 2, 1, 1, 0], "baseFret": 1})
    elif 1 <= e_fret <= 11:
        if mod == "": 
            variations.append({"frets": [e_fret, e_fret+2, e_fret+2, e_fret+1, e_fret, e_fret], "baseFret": e_fret, "barre": {"fret": e_fret, "startStr": 0, "endStr": 5}})
        elif mod == "m": 
            variations.append({"frets": [e_fret, e_fret+2, e_fret+2, e_fret, e_fret, e_fret], "baseFret": e_fret, "barre": {"fret": e_fret, "startStr": 0, "endStr": 5}})
        elif mod == "7": 
            variations.append({"frets": [e_fret, e_fret+2, e_fret, e_fret+1, e_fret, e_fret], "baseFret": e_fret, "barre": {"fret": e_fret, "startStr": 0, "endStr": 5}})
        elif mod == "m7": 
            variations.append({"frets": [e_fret, e_fret+2, e_fret, e_fret, e_fret, e_fret], "baseFret": e_fret, "barre": {"fret": e_fret, "startStr": 0, "endStr": 5}})
        elif mod in ["sus4", "7sus4"]: 
            variations.append({"frets": [e_fret, e_fret+2, e_fret+2, e_fret+2, e_fret, e_fret], "baseFret": e_fret, "barre": {"fret": e_fret, "startStr": 0, "endStr": 5}})
        elif mod == "sus2":
            variations.append({"frets": [e_fret, e_fret+2, e_fret+4, e_fret+4, e_fret, e_fret], "baseFret": e_fret})
        elif mod == "6":
            variations.append({"frets": [e_fret, e_fret+2, e_fret, e_fret+1, e_fret+2, e_fret], "baseFret": e_fret})
        elif mod in ["m6", "m6/bb", "m6/d"]:
            variations.append({"frets": [e_fret, "x", e_fret+2, e_fret, e_fret+2, e_fret], "baseFret": e_fret})
        elif mod == "5":
            variations.append({"frets": [e_fret, e_fret+2, e_fret+2, "x", "x", "x"], "baseFret": e_fret})
        elif mod == "add9":
            variations.append({"frets": [e_fret, e_fret+2, e_fret+2, e_fret+1, e_fret, e_fret+2], "baseFret": e_fret})
        elif mod == "aug":
            variations.append({"frets": [e_fret, e_fret+3, e_fret+2, e_fret+1, e_fret+1, e_fret], "baseFret": e_fret})
        elif mod in ["dim", "dim7"]:
            variations.append({"frets": [e_fret, "x", e_fret+1, e_fret, e_fret+1, "x"], "baseFret": e_fret})
        elif mod in ["11", "m11", "add11"]:
            variations.append({"frets": [e_fret, e_fret+2, e_fret, e_fret, e_fret, e_fret], "baseFret": e_fret})
        elif mod == "m9":
            variations.append({"frets": [e_fret, e_fret+2, e_fret, e_fret, e_fret, e_fret+2], "baseFret": e_fret})

    # --- VOICE 2: A-String Root Vector ---
    a_fret = offset - 9
    if a_fret < 0: a_fret += 12
    
    if a_fret == 0:
        if mod == "": variations.append({"frets": ["x", 0, 2, 2, 2, 0], "baseFret": 1})
        elif mod == "m": variations.append({"frets": ["x", 0, 2, 2, 1, 0], "baseFret": 1})
        elif mod == "7": variations.append({"frets": ["x", 0, 2, 0, 2, 0], "baseFret": 1})
        elif mod == "m7": variations.append({"frets": ["x", 0, 2, 0, 1, 0], "baseFret": 1})
        elif mod == "maj7": variations.append({"frets": ["x", 0, 2, 1, 2, 0], "baseFret": 1})
        elif mod in ["sus4", "7sus4"]: variations.append({"frets": ["x", 0, 2, 2, 3, 0], "baseFret": 1})
        elif mod == "sus2": variations.append({"frets": ["x", 0, 2, 2, 0, 0], "baseFret": 1})
        elif mod == "6": variations.append({"frets": ["x", 0, 2, 2, 2, 2], "baseFret": 1})
        elif mod == "5": variations.append({"frets": ["x", 0, 2, 2, "x", "x"], "baseFret": 1})
        elif mod == "aug": variations.append({"frets": ["x", 0, 3, 2, 2, 1], "baseFret": 1})
        elif mod == "9": variations.append({"frets": ["x", 0, 2, 4, 2, 3], "baseFret": 1})
        elif mod == "m9": variations.append({"frets": ["x", 0, 2, 4, 1, 3], "baseFret": 1})
    elif 1 <= a_fret <= 11:
        if mod == "": 
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+2, a_fret+2, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 5}})
        elif mod == "m": 
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+2, a_fret+1, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 5}})
        elif mod == "7": 
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret, a_fret+2, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 5}})
        elif mod == "m7": 
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret, a_fret+1, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 5}})
        elif mod == "maj7": 
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+1, a_fret+2, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 5}})
        elif mod in ["sus4", "7sus4"]: 
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+2, a_fret+3, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 5}})
        elif mod == "sus2":
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+2, a_fret, a_fret], "baseFret": a_fret, "barre": {"fret": a_fret, "startStr": 1, "endStr": 3}})
        elif mod == "6":
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret, a_fret+2, a_fret], "baseFret": a_fret})
        elif mod in ["m6", "m6/bb", "m6/d"]:
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+2, a_fret+1, a_fret+2], "baseFret": a_fret})
        elif mod == "5":
            variations.append({"frets": ["x", a_fret, a_fret+2, a_fret+2, "x", "x"], "baseFret": a_fret})
        elif mod == "add9":
            variations.append({"frets": ["x", a_fret, a_fret-1, a_fret+2, a_fret, a_fret], "baseFret": a_fret-1})
        elif mod in ["9", "6/9", "maj9", "69"]:
            variations.append({"frets": ["x", a_fret, a_fret-1, a_fret, a_fret, a_fret], "baseFret": a_fret-1})
        elif mod in ["11", "m11", "b11", "add11", "bm11", "f#m11", "13"]:
            variations.append({"frets": ["x", a_fret, a_fret, a_fret, a_fret, a_fret], "baseFret": a_fret})
        elif mod in ["dim", "dim7"]:
            variations.append({"frets": ["x", a_fret, a_fret+1, a_fret, a_fret+1, "x"], "baseFret": a_fret})
        elif mod == "m9":
            variations.append({"frets": ["x", a_fret, a_fret-2, a_fret, a_fret, a_fret], "baseFret": a_fret-2})

    if mod == "6" and a_fret == 0: variations.append({"frets": ["x", 0, 2, 2, 2, 2], "baseFret": 1})
    elif mod == "6" and e_fret == 0: variations.append({"frets": [0, 2, 2, 1, 2, 0], "baseFret": 1})
    elif mod == "6" and e_fret > 0: variations.append({"frets": [e_fret, e_fret+2, e_fret, e_fret+1, e_fret+2, e_fret], "baseFret": e_fret})
    elif mod == "6" and a_fret > 0: variations.append({"frets": ["x", a_fret, a_fret+2, a_fret, a_fret+2, a_fret], "baseFret": a_fret})

    variations.sort(key=lambda x: x.get("baseFret", 1))
    return variations

def harvest_and_build():
    if not os.path.exists(SONGS_DIR):
        print("❌ Error: Target folder path missing.")
        return

    # Filter down immediately to valid txt targets
    all_files = [f for f in os.listdir(SONGS_DIR) if f.lower().endswith('.txt')]
    total_files = len(all_files)
    
    print(f"🚀 Initializing high-speed harvest over {total_files} files inside Google Drive stream...")
    discovered_tokens = set()

    # High-speed unified streaming loop block
    for idx, filename in enumerate(all_files, 1):
        filepath = os.path.join(SONGS_DIR, filename)
        
        # Open exactly ONCE per file, ignoring corrupt byte frames instantly
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    tokens = re.split(r'[\s\[\]\-]+', line.strip())
                    for t in tokens:
                        if t and t.lower() not in VOCAL_BLACKLIST: 
                            discovered_tokens.add(t)
        except Exception:
            pass

        # Visual Heartbeat counter ensuring you see active progress
        if idx % 100 == 0 or idx == total_files:
            print(f"   ⚡ Parsed {idx}/{total_files} songs...")

    clean_store = {}
    
    open_seeds = {
        "C": [{"frets": ['x', 3, 2, 0, 1, 0], "baseFret": 1}],
        "G": [{"frets": [3, 2, 0, 0, 0, 3], "baseFret": 1}],
        "D": [{"frets": ['x', 'x', 0, 2, 3, 2], "baseFret": 1}],
        "A": [{"frets": ['x', 0, 2, 2, 2, 0], "baseFret": 1}],
        "E": [{"frets": [0, 2, 2, 1, 0, 0], "baseFret": 1}],
        "Am": [{"frets": ['x', 0, 2, 2, 1, 0], "baseFret": 1}],
        "Em": [{"frets": [0, 2, 2, 0, 0, 0], "baseFret": 1}],
        "Dm": [{"frets": ['x', 'x', 0, 2, 3, 1], "baseFret": 1}],
        "Cadd9": [
            {"frets": ['x', 3, 2, 0, 3, 3], "baseFret": 1},
            {"frets": ['x', 3, 2, 0, 3, 0], "baseFret": 1}
        ],
        "Fadd9": [
            {"frets": [1, 3, 3, 2, 1, 3], "baseFret": 1},
            {"frets": ['x', 'x', 3, 2, 1, 3], "baseFret": 1}
        ]
    }

    print("🧩 Generating geometric fingerboard vectors...")
    for token in sorted(discovered_tokens):
        match = CHORD_REGEX.match(token)
        if not match: continue

        base_chord = token.split('/')[0]
        base_match = CHORD_REGEX.match(base_chord)
        
        root_note = base_match.group(1) if base_match else match.group(1)
        modifier = base_match.group(2) if base_match else (match.group(2) or "")
        
        calculated_voicings = generate_movable_shapes(root_note, modifier)

        master_list = list(open_seeds[token]) if token in open_seeds else []

        for cv in calculated_voicings:
            if not any(v["frets"] == cv["frets"] for v in master_list):
                master_list.append(cv)

        master_list.sort(key=lambda x: x.get("baseFret", 1))
        if master_list:
            clean_store[token] = master_list

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(clean_store, f, indent=2)
    print(f"💾 Clean database successfully updated with {len(clean_store)} profiles inside '{OUTPUT_FILE}'.")

if __name__ == '__main__':
    harvest_and_build()