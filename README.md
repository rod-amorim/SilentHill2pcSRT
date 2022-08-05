# H1 What is it?
Simple SRT for silent hill 2 pc, shows some important information to get the 10-star rank (like number of enemies killed by fighting and shooting, total damage taken etc.)

# H1 How was it done?
The part that reads the RAM values was made based on the code available in the repository below, I just made some small modifications to interpret the values as different types (int16, int 8 etc):
https://github.com/vsantiago113/ReadWriteMemory

For the UI the TK lib was used:
https://docs.python.org/pt-br/3/library/tk.html

# H1 How to use:
To use it just run the game and then the SRT, you should see a small window with the values already being displayed:

If the game is not running an error will be displayed:

Clicking OK will terminate the app
