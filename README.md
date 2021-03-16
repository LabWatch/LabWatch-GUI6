Hello
# LabWatch-GUI6
This is our 3rd Year Enginnering Project 

We Have Created Lab Watch a Local and cloud based logging system using a Pi

The File included are: 

DHT22ReadOnly_Cloud.py  #This reads to terminal and to thingSpeak

GUI_interface.py #main GUI code that is our completed version including cloud logging 
gaguelib.py     #support lib for GUI handles gagues 


runme.sh  #auto restart code which needs to be edited so that it points to the corret path for both the GUI_interface code and this               file
  
  
  Edits need to be made to Code for personal Running:
  
  GUI_interface.py 
  
  line 67: myAPI = 'YOUR API CODE'  #add your API code from thingspeak here 
  
  line 431: subprocess.run('/home/LabWatchGUI6/runme.sh', shell=True)  # Edit path to correct path to your file
  
  
  runme.sh 
  
  line 3: python3 ~/LabWatchGUI6/GUI_interface.py #change path to point at your script 
  
  
  
  
  
 To see Git Branch: 
 
 git config --global alias.lgb "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset%n' --abbrev-commit --date=relative --branches"

git lgb
