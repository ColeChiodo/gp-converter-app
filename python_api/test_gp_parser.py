# test_gp_parser.py
import sys
from gp_parser import parse_gp_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_gp_parser.py <gp5_file_path>")
        sys.exit(1)

    gp5_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.bh1"

    # Parse the GP5 file and get binary MessagePack data
    binary_song = parse_gp_file(gp5_file)

    # Save to .bh1 file
    with open(output_file, "wb") as f:
        f.write(binary_song)

    print(f"Saved parsed binary to {output_file}")

if __name__ == "__main__":
    main()
