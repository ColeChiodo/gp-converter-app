This Python Server Script is for use with **gp-converter - A BassHero Utility**.
The server runs automatically when the Electron app is opened.

### To Test The Script Alone
1. **Start and install the Environment**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. **Run Test Script**
```bash
python test_gp_parser.py <path_to_gp_file> [output_file]
```
A binary file will be generated. The standard file extension should be `.bh1`.