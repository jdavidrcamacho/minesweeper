#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
from  base64 import encodebytes
from functools import partial
from itertools import product

#plt.close('all')


##### Functions ################################################################
def _coord(xend, yend):
    """ 
        Random coordinates for the mines
    """
    x = np.random.randint(0, xend)
    y = np.random.randint(0, yend)
    return x, y

def _setNumber(x, y, xsize, ysize, field):
    """
        Counting the number of mines around a certain house
    """
    count = 0
    xarray = np.array([x-1, x-1, x-1, x, x, x+1, x+1, x+1])
    yarray = np.array([y-1, y, y+1, y-1, y+1, y-1, y, y+1])
    for i in range(8):
        if (xarray[i] < 0) or (yarray[i] < 0):
            pass
        elif (xarray[i] > xsize-1) or (yarray[i] > ysize-1):
            pass
        else:
            if field[xarray[i], yarray[i]] == np.inf:
                count += 1
    return count

def _minefield(xsize, ysize, mines):
    """
        Creates a minefield of size xsize per ysize with a n number of mines
    """
    #empty field
    field = np.zeros((xsize, ysize))
    #adding mines
    for i in range(mines):
        x, y = _coord(xsize, ysize)
        while field[x, y] == np.inf:
            x, y = _coord(xsize, ysize)
        else:
            field[x, y] = np.inf
    #adding number of mines
    for x in range(xsize):
        for y in range(ysize):
            if field[x, y] == np.inf:
                pass
            else:
                field[x, y] = _setNumber(x, y, xsize, ysize, field)
    return field

def _clicked():
    """
        Starts the minefield
    """
    x, y, mines = int(e1.get()), int(e2.get()), int(e3.get())
    minefield = _minefield(x, y, mines)
    _minesWindow(x, y, minefield)

button_ids = []
def _check(i, minefield):
    #item, minefield = args
    bname = (button_ids[i])
    row    = bname.grid_info()['row']       # Row of the button
    column = bname.grid_info()['column']    # Column of the button
    if minefield[row, column] == np.inf:
        newWindow = tk.Tk()
        newWindow.title("GAME OVER")
        frame1 = tk.Frame(newWindow)
        frame1.grid(row=0,column=0)
        tk.Label(frame1, 
                 text="BUUUM!! \n \n You have hit a mine").grid(row = 1, 
                                                                column = 1)
        tk.Button(frame1, 
                  text="Close", command = newWindow.destroy).grid(row = 2, 
                                                               column = 1)
    else:
        bname.configure(text = str(int(minefield[row, column])))
        #bname.destroy()

def _minesWindow(xvalue, yvalue, minefield):
    """
        Final minesweeper window
    """
    window = tk.Tk()
    window.title("Kalimotxo's minesweeper")
    frame = tk.Frame(window)
    frame.grid(row=0,column=0)
    
    positions = product(range(xvalue), range(yvalue))
    for i, item in enumerate(positions):
        button = tk.Button(frame, command = partial(_check, i = i, 
                                                    minefield = minefield))
        button.grid(row = item[0], column = item[1], sticky = "n,e,s,w")
        button.configure(text = "?")
        button_ids.append(button)
 
    tk.Label(window, text = " ").grid(row = yvalue+1, column = 0)
    btn2 = tk.Button(window, text="Close", command = window.destroy)
    btn2.grid(row = yvalue+2, column = 0)
    window.mainloop()

    
#def _minesWindow(xvalue, yvalue, minefield):
#    """
#        Final minesweeper window
#    """
#    window = tk.Tk()
#    window.title("Kalimotxo's minesweeper")
#    frame = tk.Frame(window)
#    frame.grid(row=0,column=0)
#
#    btn = [[0 for y in range(yvalue)] for x in range(xvalue)] 
#    for x in range(xvalue):
#         for y in range(yvalue):
#            btn[x][y] = tk.Button(frame, 
#               command= _check(minefield, btn, x, y)).grid(column = x, row = y)
#            
#    tk.Label(window, text = " ").grid(row = yvalue+1, column = 0)
#    btn2 = tk.Button(window, text="close", command = window.destroy)
#    btn2.grid(row = yvalue+2, column = 0)
#    window.mainloop()
#
#def _check(minesfield, bnt, x, y):
#    if minesfield[x, y] != np.inf:
#        bnt[x][y].destroy


##### GUI ######################################################################
root = tk.Tk()
root.title("Welcome to Kalimotxo's minesweeper")
root.geometry('700x400')

left = tk.Frame(root, borderwidth = 2, relief = "solid")
right = tk.Frame(root, borderwidth = 2, relief = "solid")
box1 = tk.Frame(left, borderwidth = 2, relief = "solid")
box2 = tk.Frame(right, borderwidth = 2, relief = "solid")

tk.Label(box1, text = " ").grid(row = 0, column = 0)
tk.Label(box1, text = " ").grid(row = 1, column = 1)
image_url = "https://i.imgur.com/H1ISNCU.png"
image_byt = urlopen(image_url).read()
image_b64 = encodebytes(image_byt)
img = tk.PhotoImage(data = image_b64)
tk.Label(box1, image = img).grid(row = 2, column = 2)

mainText = "\n   Please enter the field characteristics \n"
tk.Label(box2, text = mainText).grid(row = 0, column = 0)

tk.Label(box2, text = "Number of rows\n").grid(row = 2, column = 0)
e1 = tk.Entry(box2)
e1.grid(row = 3, column = 0)
tk.Label(box2, text = "Number of lines\n").grid(row = 4, column = 0)
e2 = tk.Entry(box2)
e2.grid(row = 5, column = 0)
tk.Label(box2, text = "Number of mines\n").grid(row = 6, column = 0)
e3 = tk.Entry(box2)
e3.grid(row = 7, column = 0)
tk.Label(box2, text = " \n \n ").grid(row = 8, column = 1)

btn1 = tk.Button(box2, text="Click to start", command = _clicked)
btn1.grid(row = 9, column = 0)
tk.Label(box2, text = " ").grid(row = 10, column = 0)
btn2 = tk.Button(box2, text="Close game", command = root.destroy)
btn2.grid(row = 11, column = 0)

left.pack(side="left", expand=True, fill="both")
right.pack(side="right", expand=True, fill="both")
box1.pack(expand=True, fill="both", padx=5, pady=5)
box2.pack(expand=True, fill="both", padx=5, pady=5)
root.mainloop()












