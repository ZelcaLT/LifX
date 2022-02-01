@ECHO OFF
START python "C:\Users\ZelcaLT\OneDrive - Northfield School and Sports College\Documents\LifX\Spex\spex.py"
ECHO Bot started
START python "C:\Users\ZelcaLT\OneDrive - Northfield School and Sports College\Documents\LifX\Spex\dashboard.py"
ECHO Server started
START http://127.0.0.1:5000/
PAUSE