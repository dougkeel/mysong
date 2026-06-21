import os
from flask import Flask, jsonify, render_template, abort

app = Flask(__name__)

# The verified Google Drive path
SONGS_DIR = "/Users/dougkeel/Library/CloudStorage/GoogleDrive-dougkeel@gmail.com/My Drive/OnSong"

# Memory cache so we don't spam Google Drive on every page refresh
SONGS_CACHE = []

def load_lines_safely(filepath):
    """Reads ONLY the first two lines of a file, testing multiple encodings."""
    for encoding in ['utf-8', 'mac-roman', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                line1 = f.readline().strip()
                line2 = f.readline().strip()
                return line1, line2
        except UnicodeDecodeError:
            continue  # Try next encoding
        except Exception as e:
            print(f"Error reading headers for {os.path.basename(filepath)}: {e}")
            break
    return "", ""

def build_song_index():
    """Scans the directory once and builds a fast memory cache."""
    global SONGS_CACHE
    if SONGS_CACHE:
        return SONGS_CACHE
        
    print(f"\n⚡ Indexing Google Drive folder ({SONGS_DIR})...")
    songs = []
    
    if not os.path.exists(SONGS_DIR):
        print("❌ ERROR: Folder path not found.")
        return songs
        
    try:
        all_contents = os.listdir(SONGS_DIR)
        files = sorted([f for f in all_contents if f.lower().endswith('.txt')])
        print(f"Found {len(files)} text files. Parsing titles and artists...")
        
        for idx, filename in enumerate(files):
            filepath = os.path.join(SONGS_DIR, filename)
            
            # Fast read: only grabs the first 2 lines
            title, artist = load_lines_safely(filepath)
            
            if not title: title = filename.replace('.txt', '')
            if not artist: artist = "Unknown Artist"
            
            songs.append({
                "id": idx,
                "title": title,
                "artist": artist,
                "filename": filename
            })
    except Exception as e:
        print(f"❌ Error scanning directory: {e}")
        
    SONGS_CACHE = songs
    print(f" Successfully cached {len(SONGS_CACHE)} songs!\n")
    return SONGS_CACHE

def read_full_file_safely(filepath):
    """Reads the entire file only when a user clicks on it."""
    for encoding in ['utf-8', 'mac-roman', 'latin-1']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    return "Error: Could not decode this file layout."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/songs')
def api_songs():
    # Returns the pre-built memory cache instantly
    return jsonify(build_song_index())

@app.route('/api/song/<filename>')
def api_get_song(filename):
    if '..' in filename or filename.startswith('/'):
        abort(400)
        
    filepath = os.path.join(SONGS_DIR, filename)
    if os.path.exists(filepath):
        return read_full_file_safely(filepath)
    abort(404)

# Force Python to build the cache right when you run the script
print("Starting up...")
build_song_index()

@app.route('/api/chord-store')
def api_get_chord_store():
    """Serves the master chords.json file with strict cache-invalidation headers."""
    import json
    try:
        if os.path.exists('chords.json'):
            with open('chords.json', 'r', encoding='utf-8') as f:
                response = jsonify(json.load(f))
                # Add explicit cache-busting headers to destroy browser memory state
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                return response
    except Exception as e:
        print(f"Error reading chords.json: {e}")
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True, port=5001)