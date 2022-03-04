import subprocess as sub
import tkinter as tk
import os

#find the names of the available networks
os.system('cmd /c "netsh wlan show profile"')


def available_networks():
    p = sub.Popen("netsh wlan show profile", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
    p = p.split("-------------")
    print(p[1])

available_networks()

window = tk.Tk()
window.geometry("300x100")
window.title('Find Wify Password')

text = "..."
# find button
def find_wify_password(): 
    net_name = network_name_entery.get()
    p = sub.Popen("netsh wlan show profile "+net_name+" key=clear", shell=True, stdout=sub.PIPE, stderr=sub.PIPE).communicate()[0]
    a=p.decode("utf-8")
    a=a.split("Key Content            : ")
    b=a[1].split("\r\n")
    resul_entery.insert(0,b[0])

find_button = tk.Button(window,text='find',command=find_wify_password)
result_lable = tk.Label(window,text=text)

tk.Label(window, text="Networks Name : ").grid(row=0)
tk.Label(window, text="Networks Password : ").grid(row=1)

network_name_entery = tk.Entry(window)
network_name_entery.grid(row=0, column=1)

resul_entery = tk.Entry(window)
resul_entery.grid(row=1, column=1)

find_button.grid(row=2, column=1)
result_lable.grid(row=1, column=1)

window.mainloop()