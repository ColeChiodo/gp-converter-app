import os
import struct
import guitarpro
from typing import Optional

magic = b"BHTB"
ver = 1

import re

def sanitize_filename(name: str) -> str:
    # Replace any character not allowed in filenames with underscore
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

# -------------------------------------------------------------
# ---------- Helper binary writers ----------------------------
# -------------------------------------------------------------

def u8(v):  return struct.pack("B", v)
def u16(v): return struct.pack("<H", v)
def u32(v): return struct.pack("<I", v)


def write_str(f, s: str):
    """Writes UTF-8 string as: uint32 length + bytes."""
    if s is None:
        s = ""
    b = s.encode("utf-8")
    f.write(u32(len(b)))
    f.write(b)


# -------------------------------------------------------------
# ---------- Write META file ----------------------------------
# -------------------------------------------------------------

def write_meta(path, song):
    """
    META format:
        magic
        version
        title
        artist
        album
        year
        tab_author
    """
    with open(path, "wb") as f:
        f.write(magic)
        f.write(u8(ver))  # version

        write_str(f, song.title)
        write_str(f, song.artist)
        write_str(f, song.album)
        write_str(f, song.copyright)
        write_str(f, song.tab)


# -------------------------------------------------------------
# ---------- Write BARS file ----------------------------------
# -------------------------------------------------------------

def write_bars(path, song):
    """
    Bars format:
        magic
        version
        bar_count (uint32)
        initial_beats (uint8)
        initial_bpm   (uint16)

        For each change:
            bar_index (uint32)
            new_beats (uint8)
            new_bpm   (uint16)
    """
    headers = song.measureHeaders

    initial_beats = headers[0].timeSignature.numerator
    initial_tempo = getattr(headers[0], "tempo", song.tempo)

    changes = []
    prev_beats = initial_beats
    prev_tempo = initial_tempo

    for idx, h in enumerate(headers):
        beats = h.timeSignature.numerator
        tempo = getattr(h, "tempo", prev_tempo)

        if beats != prev_beats or tempo != prev_tempo:
            changes.append((idx, beats, tempo))

        prev_beats = beats
        prev_tempo = tempo

    with open(path, "wb") as f:
        f.write(magic)
        f.write(u8(ver))                     # version
        f.write(u32(len(headers)))         # total bars

        f.write(u8(initial_beats))
        f.write(u16(int(initial_tempo)))

        for index, beats, tempo in changes:
            f.write(u32(index))
            f.write(u8(beats))
            f.write(u16(int(tempo)))


# -------------------------------------------------------------
# ---------- Write INSTRUMENT FILE -----------------------------
# -------------------------------------------------------------

def write_instrument(path, name, string_count, events):
    """
    Instrument format:
        magic
        version
        string_count
        event_count (uint16)

        name_length (uint8)
        name_bytes

        Events (4 bytes each):
            offset   (uint8)
            duration (uint8)
            string   (uint8)
            fret     (uint8)
    """
    with open(path, "wb") as f:
        f.write(magic)
        f.write(u8(ver))                   # version
        f.write(u8(string_count))
        f.write(u16(len(events)))

        name_b = name.encode("utf-8")
        f.write(u8(len(name_b)))
        f.write(name_b)

        for ev in events:
            f.write(u8(ev["offset"]))
            f.write(u8(ev["duration"]))
            f.write(u8(ev["string"]))
            f.write(u8(ev["fret"]))


# -------------------------------------------------------------
# ---------- Main conversion function --------------------------
# -------------------------------------------------------------

def gp5_to_binary_folder(gp5_path: str, out_folder: Optional[str] = None) -> str:
    """
    Converts a .gp5 file into the custom binary folder format.
    Returns the folder path.
    """
    song = guitarpro.parse(gp5_path)

    # Output folder
    if out_folder is None:
        base = os.path.splitext(os.path.basename(gp5_path))[0]
        out_folder = base + "_bin"

    os.makedirs(out_folder, exist_ok=True)
    os.makedirs(os.path.join(out_folder, "instruments"), exist_ok=True)

    # Write META
    write_meta(os.path.join(out_folder, ".meta"), song)

    # Write BARS
    write_bars(os.path.join(out_folder, ".bars"), song)

    # Write INSTRUMENTS
    for track in song.tracks:
        events = []

        # Collect note events
        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    offset = min(max((beat.start or 0), 0), 255)
                    duration = min(max(beat.duration.time, 0), 255)

                    for note in beat.notes:
                        string_num = getattr(note.string, "value", note.string)
                        fret = note.value

                        events.append({
                            "offset": offset,
                            "duration": duration,
                            "string": int(string_num),
                            "fret": int(fret),
                        })

        # Write track file
        safe_name = sanitize_filename(track.name)
        out_path = os.path.join(out_folder, "instruments", f"{safe_name}.bin")

        write_instrument(
            out_path,
            track.name,
            len(track.strings),
            events
        )

    return out_folder

