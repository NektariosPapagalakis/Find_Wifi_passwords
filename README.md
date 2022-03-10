This is a simple python script that can be used to see the wifi passwords from the networks that are stored in the computer. The script uses the cmd comands :
1) netsh wlan show profile
2) netsh wlan show profile <networs name> key=clear
  
The wifi must be on in order to find the networks and their passwords
  
Requirements :
  1) The pyperclip libray
