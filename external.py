from pyray import *
from time import sleep
from helper import *
from ctypes import *
from tkinter import *
from pymem import *
from pymem.process import *
from PIL import ImageTk, Image
import time
import datetime
import keyboard
import tkinter
import customtkinter

BOX_WIDTH = 20
BOX_HEIGHT = 40

def init():
    win = get_window_info("AssaultCube")
    set_trace_log_level(5)
    set_target_fps(0)
    set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED)
    set_config_flags(ConfigFlags.FLAG_WINDOW_MOUSE_PASSTHROUGH)
    set_config_flags(ConfigFlags.FLAG_WINDOW_TRANSPARENT)
    set_config_flags(ConfigFlags.FLAG_WINDOW_TOPMOST)
    init_window(win[2], win[3], "AssaultCube ESP")
    set_window_position(win[0], win[1])

def draw_box(x, y, color):
    half_width = BOX_WIDTH // 2
    half_height = BOX_HEIGHT // 2
    
    x1 = int(x - half_width)
    y1 = int(y - half_height)
    x2 = int(x + half_width)
    y2 = int(y + half_height)
    
    draw_line(x1, y1, x2, y1, color)
    draw_line(x2, y1, x2, y2, color)
    draw_line(x2, y2, x1, y2, color)
    draw_line(x1, y2, x1, y1, color)

def main():
    proc = Pymem("ac_client.exe")
    base = proc.base_address

    while not window_should_close():
        matrix = proc.read_ctype(base + Pointer.view_matrix, (16 * c_float)())[:]
        player_count = proc.read_int(base + Pointer.player_count)
        
        begin_drawing()
        clear_background(BLANK)
        draw_fps(0, 0)
        
        if player_count > 1:
            ents = proc.read_ctype(proc.read_int(base + Pointer.entity_list), (player_count * c_int)())[1:]
            for ent_addr in ents:
                ent_obj = proc.read_ctype(ent_addr, Entity())
                if ent_obj.health > 0:
                    try:
                        wts = world_to_screen(matrix, ent_obj.pos)
                    except:
                        continue
                    draw_line(get_screen_width() // 2, get_screen_height() // 2, wts.x, wts.y, RED)
                    draw_text(ent_obj.name, wts.x, wts.y, 12, WHITE)
                    BOX_COLOR = RED
                    draw_box(wts.x, wts.y, BOX_COLOR)

        end_drawing()

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x240")

pm = pymem.Pymem("ac_client.exe")
gameModule = module_from_name(pm.process_handle, "ac_client.exe").lpBaseOfDll

def ButtonFunction1():
    pm.write_int(GetPtrAddr(gameModule + 0x17E0A8, [0xEC]), 6969)

def ButtonFunction2():
    pm.write_int(GetPtrAddr(gameModule + 0x0017E0A8, [0x144]), 6969)

    
def ButtonFunction3():
    pm.write_int(GetPtrAddr(gameModule + 0x00195404, [0x140]), 6969)

def ButtonFunction4():
    pm.write_int(GetPtrAddr(gameModule + 0x00195404, [0x12c]), 6969)
    
def ButtonFunction5():
    pm.write_int(GetPtrAddr(gameModule + 0x00195404, [0xF0]), 6969)

def GetPtrAddr(base, offsets):
    addr = pm.read_int(base)
    for i in offsets:
        if i != offsets[-1]:
            addr = pm.read_int(addr + i)
    return addr + offsets[-1]

button = customtkinter.CTkButton(master=app, text="Health (Z)", command=ButtonFunction1)
button.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Grenade (C)", command=ButtonFunction2)
button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Rifle Ammo (F)", command=ButtonFunction3)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Pistol Ammo (R)", command=ButtonFunction4)
button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

button = customtkinter.CTkButton(master=app, text="Shield (X)", command=ButtonFunction5)
button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

checkbox_1 = customtkinter.CTkCheckBox(master=app, text="ESP", command=lambda: [init(), main()])
checkbox_1.pack(side="left", padx=10, pady=0)

def on_hotkey_press_z():
    ButtonFunction1()

def on_hotkey_press_c():
    ButtonFunction2()
    
def on_hotkey_press_f():
    ButtonFunction3()

def on_hotkey_press_r():
    ButtonFunction4()

def on_hotkey_press_x():
    ButtonFunction5()

keyboard.add_hotkey("z", on_hotkey_press_z)
keyboard.add_hotkey("c", on_hotkey_press_c)
keyboard.add_hotkey("f", on_hotkey_press_f)
keyboard.add_hotkey("r", on_hotkey_press_r)
keyboard.add_hotkey("x", on_hotkey_press_x)

app.mainloop()