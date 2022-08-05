
from turtle import goto
from ReadWriteMemory import ReadWriteMemory
import tkinter as tk
import pymem
import time
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import sys
import os

class sh2EnhancedSRT:
    def __init__(self, parent):
        rwm = ReadWriteMemory()
        process_hooked = 0;
        try:
            self.process = rwm.get_process_by_name('sh2pc.exe')
            process_hooked = 1;
        except Exception as ex:
            if(type(ex).__name__ == "ReadWriteMemoryError"):
                process_hooked = 0
            else:
                sys.exit("Not expected error, contact the developer team!!!")

        if(process_hooked == 0):
            self.p_label = tk.Label(parent, text='Game process not found ! \n Run the game first !', font=('Microsoft Sans Serif', 12), bg='black', fg='red')
            self.p_label.place(x=125,y=20,anchor="center")
            self.p_button = tk.Button(
                parent,text ="        OK        ",
                command = lambda : parent.quit(),
                font=('Microsoft Sans Serif', 12),
                bg='grey',
                fg='white', 
                borderwidth=2,
                relief="groove" ,
                cursor="hand2"  
            )
            self.p_button.place(x=125,y=100,anchor="center")    
            return
        

        self.process.open()
        handle = pymem.Pymem()
        handle.open_process_from_id(self.process.pid)

        base_address = handle.base_address

        # ADDRESSES
        actionDiff_address = 0x01DBBFF4
        riddleDiff_address = 0x01DBBFF5
        actualHp_address = 0x01FB111C-0x11C+0x13C
        saveQtd_address = base_address + 0x19BBF8A
        gameTime_address = base_address + 0x19BBF94
        itemQtd_address = base_address + 0x19BBF8E
        itemBonusQtd_address = 0x01DBBF88
        defeatByShooting_address = base_address + 0x19BBF90
        defeatByFight_address = base_address + 0x19BBF92
        boatStageTime_address = base_address + 0x19BBFA0
        totalDamage_address = base_address + 0x19BBFA8

        # POINTEROBJS
        self.actionDiff_pointer = None
        self.riddleDiff_pointer = None
        self.actualHp_pointer = None
        self.saveQtd_pointer = None
        self.gameTime_pointer = None
        self.itemQtd_pointer = None
        self.itemBonusQtd_pointer = None
        self.defeatByShooting_pointer = None
        self.defeatByFight_pointer = None
        self.boatStageTime_pointer = None
        self.totalDamage_pointer = None

        # VALUES
        self.actionDiff = 0
        self.riddleDiff = 0
        self.actualHp = 0
        self.saveQtd = 0
        self.gameTime = 0
        self.itemQtd = 0
        self.itemQtdBonus = 0
        self.defeatByShooting = 0
        self.defeatByFight = 0
        self.boatStageTime = 0
        self.totalDamage = 0

        def timer():
            """This is the TIMER function that runs every 100 milliseconds and update the Ui Info"""
            # START POINTERS
            self.actionDiff_pointer = self.process.get_pointer(
                actionDiff_address)
            self.riddleDiff_pointer = self.process.get_pointer(
                riddleDiff_address)
            self.actualHp_pointer = self.process.get_pointer(actualHp_address)
            self.saveQtd_pointer = self.process.get_pointer(saveQtd_address)
            self.gameTime_pointer = self.process.get_pointer(gameTime_address)
            self.itemQtd_pointer = self.process.get_pointer(itemQtd_address)
            self.itemBonusQtd_pointer = self.process.get_pointer(itemBonusQtd_address)
            self.defeatByShooting_pointer = self.process.get_pointer(
                defeatByShooting_address)
            self.defeatByFight_pointer = self.process.get_pointer(
                defeatByFight_address)
            self.boatStageTime_pointer = self.process.get_pointer(
                boatStageTime_address)
            self.totalDamage_pointer = self.process.get_pointer(
                totalDamage_address)
            # END POINTERS

            # self.p_label.config(text='Game Online')

            # VALUES SET
            try:
                self.actionDiff = int(self.process.readByte(self.actionDiff_pointer)[0],16)
                self.riddleDiff = int(self.process.readByte(self.riddleDiff_pointer)[0],16)
                self.actualHp = self.process.readFloat(self.actualHp_pointer)
                self.saveQtd = self.process.readInt16(self.saveQtd_pointer)
                self.gameTime = self.process.readFloat(self.gameTime_pointer)
                self.itemQtd = self.process.readInt16(self.itemQtd_pointer)
                self.itemQtdBonus = self.process.readByte(self.itemBonusQtd_pointer)[0]
                self.defeatByShooting = self.process.readInt16(
                    self.defeatByShooting_pointer)
                self.defeatByFight = self.process.readInt16(
                    self.defeatByFight_pointer)
                self.boatStageTime = self.process.readFloat(
                    self.boatStageTime_pointer)
                self.totalDamage = self.process.readFloat(self.totalDamage_pointer)
            except Exception as ex:
                sys.exit("Not expected error, contact the developer team!!!")

            # VALUES TEXT SET
            self.actionDiff_VALUE['text'] = getActionLevelById(self.actionDiff)
            self.riddleDiff_VALUE['text'] = getRiddleLevelById(self.riddleDiff)
            self.ActualHp_LABEL['text'] = "HP( "+str(round(self.actualHp)) + " / 100 )"
            self.ActualHp_bar['value'] = round(self.actualHp)
            self.saveQtd_VALUE['text'] = str(self.saveQtd)
            self.gameTime_VALUE['text'] = time.strftime(
                '%H:%M:%S', time.gmtime(self.gameTime))
            self.itemQtd_VALUE['text'] = str(self.itemQtd)
            self.defeatByShooting_VALUE['text'] = str(self.defeatByShooting)
            self.defeatByFight_VALUE['text'] = str(self.defeatByFight)
            self.boatStageTime_VALUE['text'] = time.strftime(
                '%H:%M:%S', time.gmtime(self.boatStageTime))
            self.totalDamage_VALUE['text'] = str(round(self.totalDamage))

            parent.after(100, timer)

        pad_Y = 0
        pad_X = 5

        # ACTION DIFF
        self.actionDiff_LABEL = tk.Label(parent, text="Action Level", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.actionDiff_LABEL.grid(row=1, column=0, padx=pad_X, pady=pad_Y)

        self.actionDiff_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.actionDiff_VALUE.grid(row=2, column=0, padx=pad_X, pady=pad_Y)

        # RIDDLEDIFF
        self.riddleDiff_LABEL = tk.Label(parent, text="Riddle Level", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.riddleDiff_LABEL.grid(row=1, column=1, padx=pad_X, pady=pad_Y)

        self.riddleDiff_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.riddleDiff_VALUE.grid(row=2, column=1, padx=pad_X, pady=pad_Y)

        # ACTUALHP
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("green.Horizontal.TProgressbar",foreground='white', background='red')
        self.ActualHp_bar = Progressbar(parent, orient=HORIZONTAL, length=100,value=0,style="green.Horizontal.TProgressbar", mode='determinate')
        self.ActualHp_bar.grid(row=4, column=0, padx=pad_X, pady=pad_Y)

        self.ActualHp_LABEL = tk.Label(parent, text="HP", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.ActualHp_LABEL.grid(row=3, column=0, padx=pad_X, pady=pad_Y)

        # self.ActualHp_VALUE = tk.Label(parent, text="0", font=(
        #     'Microsoft Sans Serif', 8), bg='black', fg='white')
        # self.ActualHp_VALUE.grid(row=4, column=0, padx=pad_X, pady=pad_Y)

        # SAVEQTD
        self.saveQtd_LABEL = tk.Label(parent, text="Save QTD", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.saveQtd_LABEL.grid(row=3, column=1, padx=pad_X, pady=pad_Y)

        self.saveQtd_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.saveQtd_VALUE.grid(row=4, column=1, padx=pad_X, pady=pad_Y)

        # GAMETIME
        self.gameTime_LABEL = tk.Label(parent, text="Game Time", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.gameTime_LABEL.grid(row=5, column=0, padx=pad_X, pady=pad_Y)

        self.gameTime_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.gameTime_VALUE.grid(row=6, column=0, padx=pad_X, pady=pad_Y)

        # ITEMQTD
        self.itemQtd_LABEL = tk.Label(parent, text="Item count", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.itemQtd_LABEL.grid(row=5, column=1, padx=pad_X, pady=pad_Y)

        self.itemQtd_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.itemQtd_VALUE.grid(row=6, column=1, padx=pad_X, pady=pad_Y)

        # DEFEATBYSHOOT
        self.defeatByShooting_LABEL = tk.Label(parent, text="Defeat by shooting", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.defeatByShooting_LABEL.grid(
            row=7, column=0, padx=pad_X, pady=pad_Y)

        self.defeatByShooting_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.defeatByShooting_VALUE.grid(
            row=8, column=0, padx=pad_X, pady=pad_Y)

        # DEFEATBYFIGHT
        self.defeatByFight_LABEL = tk.Label(parent, text="Defeat by fighting", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.defeatByFight_LABEL.grid(row=7, column=1, padx=pad_X, pady=pad_Y)

        self.defeatByFight_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.defeatByFight_VALUE.grid(row=8, column=1, padx=pad_X, pady=pad_Y)

        # BOATSTAGETIME
        self.boatStageTime_LABEL = tk.Label(parent, text="Boat Stage Time", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.boatStageTime_LABEL.grid(row=9, column=0, padx=pad_X, pady=pad_Y)

        self.boatStageTime_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.boatStageTime_VALUE.grid(row=10, column=0, padx=pad_X, pady=pad_Y)

        # TOTALDAMAGE
        self.totalDamage_LABEL = tk.Label(parent, text="Total Damage", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='yellow')
        self.totalDamage_LABEL.grid(row=9, column=1, padx=pad_X, pady=pad_Y)

        self.totalDamage_VALUE = tk.Label(parent, text="0", font=(
            'Microsoft Sans Serif', 10), bg='black', fg='white')
        self.totalDamage_VALUE.grid(row=10, column=1, padx=pad_X, pady=pad_Y)
        timer()


def getActionLevelById(id) -> str:
    match id:
        case 0:
            return 'Beginner'
        case 1:
            return 'Easy'
        case 2:
            return 'Normal'
        case 3:
            return 'Hard'


def getRiddleLevelById(id) -> str:
    match id:
        case 0:
            return 'Easy'
        case 1:
            return 'Normal'
        case 2:
            return 'Hard'


def main():
    root = tk.Tk()
    w = 250
    h = 230
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(width=False, height=False)
    root.title('Silent hill 2 SRT'),
    root.iconbitmap(r'C:\Users\rodri\Desktop\SilentHill2Srt\icon.ico')
    # root.tk.call('wm', 'iconphoto', root._w, image)
    root.configure(background='#000')
    sh2EnhancedSRT(root)
    root.mainloop()
    sys.exit(1)


if __name__ == '__main__':
    main()
