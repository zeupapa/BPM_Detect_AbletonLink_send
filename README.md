# BPM_Detect_AbletonLink_send

**This command line BPM analyzer tool is designed for live musicians like DJ-s and VJ-s who want to collaborate with other artists.**
**The program analyses the input signal of a selected sound device (in mono mode) and determines the BPM of the input by librosa lib.**
**Then this program sends the determined BPM out on the Ableton Link protocol using aalink library.**

**The relyable range is currently between 110-180 BPM.**

## Advantages:

   - Fairly accurate (good enough for what I needed it)
   - Ableton Link is integrated, allowing connection to other Link enabled softwares like other VJ tools.
   - Works with low-quality signals, such as a microphone input.

## Installation:

   1. `pip install sounddevice librosa numpy aalink asyncio`
   2. Download all the files (bpm.py) from this repository and save into a new folder.
   3. cd into the new folder via command line
   4. Run bpm.py from the command line.

## Making an executable for Windows using PyInstaller:
   1. Install PyInstaller: `pip install pyinstaller`
   2. Navigate to your script’s directory: `cd path\to\your\script`
   3. Run PyInstaller: `pyinstaller --onefile bpm.py` (The `–onefile` flag indicates that you want a single executable file instead of a bunch of files)
   
See Pyinstaller manual form more options: https://pyinstaller.org/en/stable/usage.html