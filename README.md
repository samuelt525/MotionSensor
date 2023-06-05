# MotionSensor

## Installation:
The program does not require any installation. Simply run your OS-specific executable file here: https://github.com/samuelt525/MotionTracker54/releases/tag/v1.0.0

## How to contribute
<p>This program runs on Python 3, therefore you will need to install Python 3 before you are able to add to the code.</p>
<p>All of the necessary Python modules are found in the requirements.txt file. You can install all the modules by running "pip install -r requirements.txt". If you install any additional modules, the requirements.txt file can be updated by running "pip freeze > requirements.txt"</p>
<p>To run the Motion Tracker program, run "python3 Controller.py"</p>

## How to build/compile the program
<p>Pyinstaller is used to compile the program into an executable file.</p>
<p>To compile the program on Windows, run "pyinstaller --onefile --name MotionTracker --add-data "media.qml;." --add-data "Logo.png;." Controller.py --noconsole"</p>
<p>To compile the program on Mac, run "pyinstaller --onefile --name MotionTracker --add-data "media.qml:." --add-data "Logo.png:." Controller.py --noconsole --icon=SalvageLogo.icns"</p>
<p>The compiled program will be outputted to the build directory.</p>
