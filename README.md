# What is it?
Simple SRT for silent hill 2 pc, shows some important information to get the 10-star rank (like number of enemies killed by fighting and shooting, total damage taken etc.)

# How was it done?
The part that reads the RAM values was made based on the code available in the repository below, I just made some small modifications to interpret the values as different types (int16, int 8 etc):
https://github.com/vsantiago113/ReadWriteMemory

For the UI the TK lib was used:
https://docs.python.org/pt-br/3/library/tk.html

# How to use
To use it just run the game and then the SRT, you should see a small window with the values already being displayed:

![alt text](https://github.com/rod-amorim/SilentHill2pcSRT/blob/main/Main_screen.PNG)

If the game is not running an error will be displayed:

![alt text](https://github.com/rod-amorim/SilentHill2pcSRT/blob/main/Main_screen_error.PNG)

Clicking OK will terminate the app

# Download

The download of the .exe is available in the releases section of this page

# Build your own EXE (only if you choose to clone the repository )
```
python -m PyInstaller --onefile -w -F --add-binary "icon.ico;." --noconsole --icon="Full path to the .ico file inside the project folder ex:E:\desenv\SilentHill2Srt\icon.ico" Sh2SRTApp.py
```
