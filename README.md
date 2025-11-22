# gp-converter - BassHero Utility
The purpose of this utility app is to convert `.gp5` files into a format that is suitable for use in the BassHero ESP32 Game.

## Why `.gp5` files?
There are lots of website that host `.gp5` files, so it is very supported and easy to find your favorite songs tab. Some websites include:
[UltimateGuitar](https://www.ultimate-guitar.com/explore?type%5B%5D=Pro), [Songsterr](https://www.songsterr.com/)*, [GuitarPro](https://www.guitar-pro.com/tabs), [GProTab](https://gprotab.net/), [GuitarProTabs](https://guitarprotabs.org/)
  *paid service

## How to use
1. **Have the nessessary hardware**:
    * [BassHero Guitar Pedal](https://github.com/ColeChiodo/esp32-instrument-practice-pedal)
      * **Important!**: SD card must be formatted as FAT32
2. **Download a `.gp5` file from the web.**
3. **Upload the `.gp5` file to the app.**
4. **Wait for the file to convert to a BassHero tab file.**
5. **Get the BassHero tab File. You have 2 options:**
   * A. Download from the App, upload to SD Card.
     * a
   * B. Upload the file directly to the ESP32 over WiFi.
     * b

## Build and Run Yourself
1. 
```bash
npm install
```

```bash
npm run dev
```

```bash
npm run build
```

```bash
npm run pack
```

```bash
npm run dist
```

## Behind the scenes
A glimps at how the code functions for those that want to know.
### How does the file conversion work?
A python script `python_api/main.py` uses the [PyGuitarPro Package](https://github.com/Perlence/PyGuitarPro) to read `.gp5` files.
* This only works for `gp3` `gp4` and `gp5` files. 

It then turns it into the following format:
```json
{
    song title
    author
    tuning
    per bar time signature
    per bar bpm
    tab ascii (per string)
}
```
### How does the file transfer over WiFi work.
The ESP runs a small HTTP server on startup with `POST` endpoint to upload a file.
Also on startup, the ESP announces itself to the local network using an mDNS.
* This means that the ESP is accessable on the local network at `basshero.local`

***
**© 2025 [colechiodo.cc](https://colechiodo.cc) | MIT License**