import subprocess as sub
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

#find the names of the available networks
os.system('cmd /c "netsh wlan show profile"')


def available_networks():
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
        #c.replace("All User Profile     : ","")
    return cc
     

window = tk.Tk()
window.geometry("500x500")
window.title('Find Wify Password')

text = "..."
# find button
def find_wify_password(): 
    net_name = net_name_select.get()
    if net_name == "Pick a Networck":
         messagebox.showerror('error', 'Select a network first')
    else:
        p = sub.Popen("netsh wlan show profile "+net_name+" key=clear", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
        a=p.decode("utf-8")
        a=a.split("Key Content            : ")
        b=a[1].split("\r\n")
        result_entery.insert(0,b[0])


find_button = tk.Button(window,text='find',command=find_wify_password)
result_lable = tk.Label(window,text=text)

tk.Label(window, text="Networks Name : ").grid(row=0)
tk.Label(window, text="Networks Password : ").grid(row=1)


networks_names_list = available_networks()
net_name_select = ttk.Combobox(window, values=networks_names_list,width=27)
net_name_select.set("Pick a Networck")
net_name_select.grid(row=0, column=1)


result_entery = tk.Entry(window,width=30)
result_entery.grid(row=1, column=1)

find_button.grid(row=2, column=1)
result_lable.grid(row=1, column=1)

window.mainloop()
