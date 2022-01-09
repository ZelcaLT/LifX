@ECHO OFF
START python "D:/Nextcord/main.py"
ECHO Bot starting 
START python "D:/Nextcord/dashboard.py"
ECHO Dashboard starting
START http://127.0.0.1:5000/
PAUSE