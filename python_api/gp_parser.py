import guitarpro
import json
import msgpack

def to_dict_safe(obj, _visited=None, _depth=0, _max_depth=10):
    """
    Convert an object to dict safely, avoiding cycles and excessive recursion.
    """
    if _visited is None:
        _visited = set()
    if id(obj) in _visited or _depth > _max_depth:
        return str(obj)
    _visited.add(id(obj))
    if isinstance(obj, list):
        return [to_dict_safe(o, _visited, _depth + 1, _max_depth) for o in obj]
    elif isinstance(obj, dict):
        return {k: to_dict_safe(v, _visited, _depth + 1, _max_depth) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        result = {}
        for k, v in vars(obj).items():
            if k.startswith("_"):
                continue
            result[k] = to_dict_safe(v, _visited, _depth + 1, _max_depth)
        return result
    else:
        return obj

def parse_gp_file(file_path: str) -> bytes:
    song = guitarpro.parse(file_path)

    # song_dict = to_dict_safe(song)
    # json_str = json.dumps(song_dict, indent=2, ensure_ascii=False)

    # # save json to file
    # with open("output.json", "w", encoding="utf-8") as f:
    #     f.write(json_str)
    
    version = song.versionTuple
    print(f"Detected Version: {version[0]}.{version[1]}.{version[2]}")

    result = {
        "metadata": {
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "year": song.copyright,
            "tab_author": song.tab,
        },
        "bars": [],
        "tracks": []
    }

    # Bars / measures
    for idx, header in enumerate(song.measureHeaders, 1):
        bar_info = {
            "bar_number": idx,
            "beats_per_bar": header.timeSignature.numerator,
            "tempo": getattr(header, 'tempo', song.tempo)
        }
        result["bars"].append(bar_info)

    # Tracks
    for track in song.tracks:

        track_dict = {
            "name": track.name,
            "notes": []
        }

        # Measures → voices → beats → notes
        for measure_idx, measure in enumerate(track.measures, 1):
            for voice in measure.voices:
                for beat_idx, beat in enumerate(voice.beats, 1):
                    for note in beat.notes:
                        # safely get string number
                        string_number = note.string.value if hasattr(note.string, "value") else note.string
                        note_info = {
                            "bar": measure_idx,
                            "beat": beat_idx,
                            "string": string_number,
                            "fret": note.value,
                            "duration": beat.duration.time,
                            "dynamics": note.velocity
                        }
                        track_dict["notes"].append(note_info)

        result["tracks"].append(track_dict)

    binary_data = msgpack.packb(result, use_bin_type=True)
    return binary_data
