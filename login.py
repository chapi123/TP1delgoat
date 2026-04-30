#macro para loguear

import keyboard as kb
import pyautogui as gui
import time
import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

password = simpledialog.askstring("Contraseña", "Ingresá la contraseña:")
password2 = simpledialog.askstring("Contraseña", "Ingresá la contraseña:", show='*')

if password2 == "":
    password2 = None

def enter() :
    kb.press_and_release('enter')

kb.press_and_release('win')
time.sleep(2)
kb.write('Google', delay=0.1)
time.sleep(2)
enter()
time.sleep(3.5)
kb.press_and_release('ctrl+shift+n')
time.sleep(2)
kb.write('gmail.com', delay=0.1)
time.sleep(1)
enter()
time.sleep(4.5)
kb.write('schaparro@alumno.huergo.edu.ar', delay=0.1)
time.sleep(1)
enter()
time.sleep(3)
kb.write(password, delay=0.1)
time.sleep(1)
enter()
time.sleep(9)

for i in range(12) :
    time.sleep(0.3)
    kb.press_and_release('tab')

enter()
time.sleep(2)

for i in range(4) :
    time.sleep(0.3)
    kb.press_and_release('tab')

enter()
time.sleep(1)

gui.hotkey('alt', 'tab')
time.sleep(1)
gui.hotkey('alt', 'f4') 


if password2: 
    time.sleep(1)
    kb.press_and_release('ctrl+t')
    kb.write('spotify.com', delay=0.1)
    enter()
    time.sleep(6)
    gui.click(1277, 155)
    time.sleep(4)schaparro@alumn
    kb.press_and_release('tab')
    kb.write('santiago09.chaparro@gmail.com', delay=0.1)
    enter()
    time.sleep(3)
    gui.click(677,617)
    time.sleep(4)
    for i in range(3):
        time.sleep(0.3)
        kb.press_and_release('tab')
    time.sleep(0.3)
    kb.write(password2, delay=0.1)
    enter()
    time.sleep(5)
    gui.click(1332, 692)
    kb.press_and_release('ctrl+tab')
    time.sleep(0.1)
    kb.press_and_release('ctrl+tab')
    gui.moveTo(667, 378)
