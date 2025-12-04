# test_gp_parser.py

import sys
from gp_parser import gp5_to_binary_folder

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_gp_parser.py <gp5_file_path> [output_folder]")
        sys.exit(1)

    gp5_file = sys.argv[1]
    out_folder = sys.argv[2] if len(sys.argv) > 2 else None

    # Convert the GP5 file into the custom binary folder format
    result_folder = gp5_to_binary_folder(gp5_file, out_folder)

    print(f"Saved parsed binary folder to: {result_folder}")

if __name__ == "__main__":
    main()

