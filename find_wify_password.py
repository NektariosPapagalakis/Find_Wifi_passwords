import os
from posixpath import split
import subprocess as sub
import tkinter as tk
from tkinter import messagebox
from webbrowser import get
import pyperclip as pc
from pyqrcode import create

import re
import time
import customtkinter
from pynput.keyboard import Key, Controller

# Set dark appearance mode:
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class App(customtkinter.CTk):
    BACKGROUND_COLOR = "#1F1F1F"
    BACKGROUND_COLOR_L1= "#4B4B4B"
    SECOND_COLOR = "#6F6F6F"
    MY_RED = "#BA0000"
    MY_BLUE = "#0080FF"
    MY_BLUE_2 = "#0000FF"

    APP_NAME = "Find WiFi Password"
    WIDTH = 600
    HEIGHT = 300
 
    MAIN_COLOR_DARK = "#2D5862"
    MAIN_HOVER = "#458577"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def available_networks():
            try:
                p = sub.Popen("netsh wlan show profile", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
                a=p.decode("utf-8")
                if (a == "There is no wireless interface on the system.\r\n"):
                    messagebox.showerror('error', '1. There is no wireless interface on the system')
                    return "Problem"
                a = a.split("User profiles")
                b = a[1].split("\r\n")
                cc = []
                for i in range(2,len(b)-2):
                    cc.append(b[i])
                for c in range(len(cc)):
                    cc[c] = cc[c].replace("    ","")
                    temp = cc[c].split(" : ")
                    cc[c] = temp[1]
                return cc
            except:
                messagebox.showerror('error', '2. Something went wrong')
                return "Problem"

        def wifi_on_off_check():
            p = sub.Popen("netsh wlan show interfaces", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
            state = repr(p.decode("utf-8"))
            state = state.replace("\\r","")
            state = state.replace("\\n\\n","\\n")
            state = state.replace("\\n","",1)
            state = re.sub(' +', ' ', state)
            state = state.replace("\\n ","\\n")
            state = state.replace(" \\n","\\n")
            state = state.split("\\n")
            state.pop(len(state)-1)
            if state[6]=="State : connected":
                return "On"
            elif state[6]=="State : disconnected":
                if(state[8]=="Software On"):
                    return "On"
                else:
                    return "Off"


        def wifi_switch_turn_on_off():
            os.system("explorer ms-settings:network-wifi")
            time.sleep(1)
            Controller().press(Key.tab)
            Controller().release(Key.tab)
            Controller().press(Key.space)
            Controller().release(Key.space)
            Controller().press(Key.alt)
            Controller().press(Key.f4)
            Controller().release(Key.f4)
            Controller().release(Key.alt)


        def copy_password():
            if (self.result_entery.get() == ""):
                messagebox.showerror('error', '3. You must find the password firs')
            else:
                pc.copy(self.result_entery.get())

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)
        self.configure(background=App.BACKGROUND_COLOR)
        

        def create_qr_code():
            global dta
            name_text = selected_network_name.get()
            password_text = self.result_entery.get()
            qr = create('WIFI:S:'+name_text+';T:WPA;P:'+password_text+';;')
            global xbm_image
            xbm_image = tk.BitmapImage(data=qr.xbm(scale=6), )

            self.frame_qr.pack()
            self.qr_label.pack()
            
            self.qr_label.config(image=xbm_image,fg_color=("white"))
            self.geometry("500x550")

        def connect():
            if selected_network_name.get() == "Select Network":
                messagebox.showerror('error', '4. Select a network first')
            else:
                ssid = selected_network_name.get()
                name = selected_network_name.get()
                try:
                    p = sub.Popen("netsh wlan connect ssid="+ssid+" name="+name, shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
                    a=p.decode("utf-8")
                    if( a=="Connection request was completed successfully.\r\n"):
                        messagebox.showinfo("Connected", "Connected")
                    else:
                        print(a)
                        messagebox.showerror('error', '5. Connection failed, something went wrong')
                except:
                    p = sub.Popen("netsh wlan connect ssid="+ssid+" name="+name, shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
                    string_p = str(p)
                    a = string_p.replace("b'","").split(":\\r\\n")
                    a = a[0]
                    if a =="Function WlanGetAvailableNetworkList returns error 2150899714":
                        message = messagebox.askyesno('WiFi is Off', 'Do you want me to turn the WiFi On?')
                        print(message)
                        if message == True:
                            self.wifi_switch.select()
                            time.sleep(1)
                            connect()
                    else:
                        messagebox.showerror('error', '6. Connection failed, something went wrong')

        def find_wifi_password():
            net_name = selected_network_name.get()
            if net_name == "Select Network":
                messagebox.showerror('error', '7. Select a network first')
            else:
                p = sub.Popen("netsh wlan show profile "+net_name+" key=clear", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
                a=p.decode("utf-8")
                a=a.split("Key Content            : ")
                b=a[1].split("\r\n")
                self.result_entery.delete(0, 'end')
                self.result_entery.insert(0,b[0])    
                create_qr_code()

        #Create Frames
        #---Main Frame --
        self.main_frame = customtkinter.CTkFrame(master=self, corner_radius=20)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        #--Button Frame --
        self.button_frame = customtkinter.CTkFrame(master=self, corner_radius=20)
        #--QR Frame --
        self.frame_qr = customtkinter.CTkFrame(master=self, corner_radius=20)
        #WiFi Switch
        self.wifi_switch_label = tk.Label(self, text="WiFi :", font=20, foreground=App.MY_BLUE, background=App.BACKGROUND_COLOR)
        self.wifi_switch = customtkinter.CTkSwitch(master=self,text="")
        if wifi_on_off_check() == "On":
            self.wifi_switch.select()
        self.wifi_switch.config(command= wifi_switch_turn_on_off)

        #Name Select
        self.network_name_label = customtkinter.CTkLabel(master=self.main_frame, text="Networks Name :")
        networks_names_list = available_networks()
        if (networks_names_list == "Problem"):
            networks_names_list = ["---"]

        selected_network_name = tk.StringVar(self)
        selected_network_name.set("Select Network")
        self.network_name_select = tk.OptionMenu(self.main_frame, selected_network_name, *networks_names_list)
        self.network_name_select.config(width=33,font=25,foreground=App.MY_BLUE,highlightthickness=0,bg=App.SECOND_COLOR, fg=App.MY_BLUE_2)
        self.network_name_select["highlightthickness"]=0

        #Result
        self.net_password_label =customtkinter.CTkLabel(master=self.main_frame, text="Networks Password :")
        self.result_entery = customtkinter.CTkEntry(master=self.main_frame,width=300,placeholder_text="Password")

        #Buttons
        self.find_button = customtkinter.CTkButton(master=self.button_frame,text='Find',command=find_wifi_password)
        self.copy_button = customtkinter.CTkButton(master=self.button_frame,text='Copy',command=copy_password)
        self.connect_button = customtkinter.CTkButton(master=self.button_frame,text='Connect',command=connect)

        #------------------- QR ---------------------
        self.qr_label = customtkinter.CTkLabel(master=self.frame_qr,text="",corner_radius=100)

        #Plece at Window
        self.wifi_switch_label.place(y=10,x=10)
        self.wifi_switch.place(y=13,x=65)
        self.main_frame.pack(pady=(40,10),padx=40,fill = "x")
        #row 1
        self.network_name_label.grid(row = 0, column=0,sticky=tk.W, pady=(15,5),padx=(5,10))
        self.network_name_select.grid(row = 0, column=1,sticky=tk.W, pady=(15,5),padx=(5,10))
        #row 2
        self.net_password_label.grid(row = 1, column=0,sticky=tk.W, pady=(5,15),padx=(5,10))
        self.result_entery.grid(row = 1, column=1,sticky=tk.EW, pady=(5,15),padx=(5,15))

        self.find_button.pack(pady=(10,5),expand = True, fill = tk.BOTH,padx=60)
        self.copy_button.pack(side = tk.LEFT, expand = True, fill = tk.BOTH,padx=(60,5),pady=(5,10))
        self.connect_button.pack(side = tk.LEFT, expand = True, fill = tk.BOTH,padx=(5,60),pady=(5,10))
        self.button_frame.pack(pady=(10,20),padx=40,fill = "x")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()


BACKGROUND_COLOR = "#2C2C2C"
SECOND_COLOR = "#5B5B5B"


def available_networks():
    try:
        p = sub.Popen("netsh wlan show profile", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
        a=p.decode("utf-8")
        a = a.split("User profiles")
        b = a[1].split("\r\n")
        cc = []
        for i in range(2,len(b)-2):
            cc.append(b[i])
        for c in range(len(cc)):
            cc[c] = cc[c].replace("    ","")
            temp = cc[c].split(" : ")
            cc[c] = temp[1]
        return cc
    except:
        return "Problem"

def copy_password():
    if (result_entery.get() == ""):
        messagebox.showerror('error', 'You must find the password firs')
    else:
        pc.copy(result_entery.get())


window = tk.Tk()
window.geometry("500x300")
window.title('Find Wifi Password')
window.configure(background=BACKGROUND_COLOR)


def create_qr_code():
    global dta
    name_text = selected_network_name.get()
    password_text = result_entery.get()
    qr = create('WIFI:S:'+name_text+';T:WPA;P:'+password_text+';;')
    global xbm_image
    xbm_image = tk.BitmapImage(data=qr.xbm(scale=6), )
    qr_label.config(image=xbm_image,background='white')
    window.geometry("500x600")

def find_wifi_password(): 
    net_name = selected_network_name.get()
    if net_name == "Select Network":
         messagebox.showerror('error', 'Select a network first')
    else:
        p = sub.Popen("netsh wlan show profile "+net_name+" key=clear", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
        a=p.decode("utf-8")
        a=a.split("Key Content            : ")
        b=a[1].split("\r\n")
        result_entery.delete(0, 'end')
        result_entery.insert(0,b[0])
    
        create_qr_code()

#Create Frames
frame_name_select = tk.Frame(window,background=BACKGROUND_COLOR)
frame_get_password = tk.Frame(window,background=BACKGROUND_COLOR)
frame_buttons = tk.Frame(window,background=BACKGROUND_COLOR)
frame_qr = tk.Frame(window,background=BACKGROUND_COLOR)

#Name Select
network_name_label = tk.Label(frame_name_select, text="Networks Name : ", font=20, foreground="red", background=BACKGROUND_COLOR)

networks_names_list = available_networks()
if (networks_names_list == "Problem"):
    messagebox.showerror('error', 'Something went wrong')
    networks_names_list = ["---"]

selected_network_name = tk.StringVar(window)
selected_network_name.set("Select Network")
network_name_select = tk.OptionMenu(frame_name_select, selected_network_name, *networks_names_list)
network_name_select.config(width=27,font=20,foreground="red",background=BACKGROUND_COLOR,highlightthickness=0,bg=SECOND_COLOR, fg="red")
network_name_select.config(bg=SECOND_COLOR,fg="red")
network_name_select["highlightthickness"]=0

network_name_select["menu"].config(bg=SECOND_COLOR)

#Result
net_password_label =tk.Label(frame_get_password, text="Networks Password : ", font=20,foreground="red", background=BACKGROUND_COLOR)
result_entery = tk.Entry(frame_get_password,width=27, font=20, background=SECOND_COLOR)

#Buttons
find_button = tk.Button(frame_buttons,text='Find',command=find_wifi_password, width=20,foreground="red", background=SECOND_COLOR)
copy_button = tk.Button(frame_buttons,text='Copy',command=copy_password, width=20,foreground="red", background=SECOND_COLOR)


#QR
qr_label = tk.Label(frame_qr,background=BACKGROUND_COLOR)


#Plece at Window

frame_name_select.pack(pady=20)
network_name_label.pack(side=tk.LEFT)
network_name_select.pack(side=tk.LEFT)

frame_get_password.pack(pady=20)
net_password_label.pack(side=tk.LEFT)
result_entery.pack(side=tk.LEFT)

frame_buttons.pack(pady=20)
find_button.pack(pady=5)
copy_button.pack(pady =5)

frame_qr.pack(pady=20)
qr_label.pack()

window.mainloop()
