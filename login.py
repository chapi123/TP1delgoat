#macro para loguear

import keyboard as kb
import pyautogui as gui
import time
import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

password = simpledialog.askstring("Contraseña", "Ingresá la contraseña:")
cisco_input = simpledialog.askstring("Cisco", "Ingresa cualquier cosa para entrar:")
password2 = simpledialog.askstring("Contraseña", "Ingresá la contraseña:", show='*')

if password == "":
    password = None

if password2 == "":
    password2 = None

cisco = cisco_input != ""

def enter() :
    kb.press_and_release('enter')

if password or password2:
    kb.press_and_release('win')
    time.sleep(2)
    kb.write('Google', delay=0.1)
    time.sleep(2)
    enter()
    time.sleep(3.5)
    kb.press_and_release('ctrl+shift+n')
    time.sleep(2)
    if password: 
        kb.write('gmail.com', delay=0.1)
        enter()
        time.sleep(4)     
        for i in range(4):
            time.sleep(0.3)
            kb.press_and_release('tab')
        time.sleep(1)
        enter()
        time.sleep(5.5)
        kb.write('schaparro@alumno.huergo.edu.ar', delay=0.1)
        time.sleep(1)
        enter()
        time.sleep(4.5)
        kb.write(password, delay=0.1)
        time.sleep(1)
        enter()
        time.sleep(9)
        gui.click(1176, 119)
        time.sleep(1)

        for i in range(4) :
            time.sleep(0.3)
            kb.press_and_release('tab')                             

        enter()
        time.sleep(1)       


        gui.hotkey('alt', 'tab')
        time.sleep(1)
        gui.hotkey('alt', 'f4') 
        gui.hotkey('ctrl', 'tab')
        gui.hotkey('ctrl', 'w')
        gui.hotkey('ctrl', 'tab')

    if password and cisco :
        time.sleep (1)
        gui.hotkey('ctrl', 'tab')
        time.sleep(1)
        gui.click(203, 279)
        time.sleep(2)
        gui.click(800, 277)
        time.sleep(2)
        gui.click(655, 610)
        time.sleep(5.5)
        gui.click(197, 498)
        time.sleep(4.5)
        gui.click(934, 616)
        time.sleep(4.5)
        gui.click(215, 566)

    if password2: 
        time.sleep(1)
        kb.press_and_release('ctrl+t')
        time.sleep(2)
        kb.write('spotify.com', delay=0.1)
        enter()
        time.sleep(6)
        gui.click(1275, 127)
        time.sleep(4)
        kb.press_and_release('tab')
        kb.write('santiago09.chaparro@gmail.com', delay=0.1)
        enter()
        time.sleep(3)
        gui.click(688, 572)
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
