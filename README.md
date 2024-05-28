# HandCam
Control screen with the force because it's cool.

## Install
* Download program.py
* Download or update Python
  >https://www.python.org/downloads/
* Open terminal [Cmd / Powershell]
```
  > pip install opencv-python <br>
  > pip install pyautogui <br>
  > pip install mediapipe
```
* Find program.py location and run
```
  > cd location
  > Python program.py
```
* Choose Yes or No for initialization questions (y/n)
```
  Show camera feed? (y/n):
  > y
  Are you in tablet mode? (y/n):
  > n
```

## Current Implementations
> Index = Mouse movement <br>
> Thumb + index = Scroll <br>
> Thumb + ring = Click / Drag

Mouse follows index finger currently. Click **space** if viewing cam feed to see hand tracking <br>
**To scroll**, hold index finger and thumb together and move hand up or down <br>
**To click or drag**, make ring finger and thumb quickly touch *or* hold fingers together and move hand

## Documentation
Please make my code better <br>
> https://ai.google.dev/edge/mediapipe/solutions/guide
> https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html
> https://pyautogui.readthedocs.io/en/latest/quickstart.html