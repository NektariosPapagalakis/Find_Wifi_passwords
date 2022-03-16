import subprocess as sub
import tkinter as tk
from tkinter import messagebox
import pyperclip as pc
from pyqrcode import create

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
window.title('Find Wify Password')
window.configure(background=BACKGROUND_COLOR)


def create_qr_code():
    global dta
    name_text = seleted_network_name.get()
    password_text = result_entery.get()
    qr = create('WIFI:S:'+name_text+';T:WPA;P:'+password_text+';;')
    global xbm_image
    xbm_image = tk.BitmapImage(data=qr.xbm(scale=6), )
    qr_label.config(image=xbm_image,background='white')
    window.geometry("500x600")

    

def find_wify_password(): 
    net_name = seleted_network_name.get()
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
networck_name_label = tk.Label(frame_name_select, text="Networks Name : ", font=20, foreground="red", background=BACKGROUND_COLOR)

networks_names_list = available_networks()
if (networks_names_list == "Problem"):
    messagebox.showerror('error', 'Something went wrong')
    networks_names_list = ["---"]

seleted_network_name = tk.StringVar(window)
seleted_network_name.set("Select Network")
network_name_select = tk.OptionMenu(frame_name_select, seleted_network_name, *networks_names_list)
network_name_select.config(width=27,font=20,foreground="red",background=BACKGROUND_COLOR,highlightthickness=0,bg=SECOND_COLOR, fg="red")
network_name_select.config(bg=SECOND_COLOR,fg="red")
network_name_select["highlightthickness"]=0

network_name_select["menu"].config(bg=SECOND_COLOR)

#Result
net_password_label =tk.Label(frame_get_password, text="Networks Password : ", font=20,foreground="red", background=BACKGROUND_COLOR)
result_entery = tk.Entry(frame_get_password,width=27, font=20, background=SECOND_COLOR)

#Buttons
find_button = tk.Button(frame_buttons,text='Find',command=find_wify_password, width=20,foreground="red", background=SECOND_COLOR)
copy_button = tk.Button(frame_buttons,text='Copy',command=copy_password, width=20,foreground="red", background=SECOND_COLOR)

#QR
qr_label = tk.Label(frame_qr,background=BACKGROUND_COLOR)


#Plece at Window

frame_name_select.pack(pady=20)
networck_name_label.pack(side=tk.LEFT)
network_name_select.pack(side=tk.LEFT)

frame_get_password.pack(pady=20)
net_password_label.pack(side=tk.LEFT)
result_entery.pack(side=tk.LEFT)

frame_buttons.pack(pady=20)
find_button.pack(pady=5)
copy_button.pack(pady = 5)

frame_qr.pack(pady=20)
qr_label.pack()

window.mainloop()