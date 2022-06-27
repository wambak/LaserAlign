# Honors Project Description
The project will consist of building software for the nEXO project at SLAC in collaboration with Skyline College. Curtis Chou will be working with Professor Wamba to build software that can aid in the alignment of a laser beam and an optical fiber cable. This is otherwise known as beam steering. The laser light is used to generate electrons that drift in liquid xenon in order to determine the xenon’s chemical purity. The best way to build this software will be what Curtis is researching. Typically, the laser is aligned with two people collaborating in two different rooms. One is looking at an oscilloscope yelling at the other person in the other room, telling the second person how to adjust the laser beam alignment knobs so that the beam is reasonably aligned with the optical fiber cable. The hope is that the completed software will allow the person in the room with the knobs to work independently by providing a visual for them on how well aligned the laser beam is.

This project relates to the computer science and physics fields. We will be building this software in Python. The only requirement for this project is to attempt to complete a draft of the proposed software by the end of the semester. More information about the nEXO project which this honors project is under can be found at https://nexo.llnl.gov/ .

# How to use the Fiber Alignment Tool
1. The tool is located in [scopeclient.py](/scopeclient.py) file therefore download the file.
2. You may need to change the address of where the client connects to the server. Therefore, if needed, change the following lines to the proper address but keep the same commands.
```python
f = urllib.request.urlopen('http://localhost:5022/?COMMAND=curve?')
f2 = urllib.request.urlopen('http://localhost:5022/?COMMAND=wfmpre?')
```
3. With the proper addresses, you can now run the code in your terminal with the following command:
```
python3 scopeclient.py
```
# Fiber Alignment Tool
- The tool should output a GUI similar to the one below:
<!-- ![Example GUI](/example_GUI.png) -->
<img src="/example_GUI.png" width="500" height="300">

- The bottom graph depicts the most recent waveform.
- The top graph is a history of the waveform upstroke/peak size.
  - **Waveform upstroke/peak** size is determined by creating a subset of the waveform consisting of values until 50 microseconds. We end the subset at 50 microseconds because the upstoke generally occurs somewhere before that time.
  - We then find the max value of this subset giving us the highest point in the upstroke. 
  - From the highest point in the upstroke, we then check either previous 50 points or all previous points to find where the upstroke begins.
  - With the max and min value of the upstroke, we subtract the min from the max to obtain our upstroke/peak size.
  - This process is shown in the code below:
```python
  fiftymus = np.argmax( np.array(t) > 50.0 )
  print("fiftymus: " , fiftymus)
  # create subset of waveform with values up until 50us:
  volt_subset = volt[:fiftymus]
  max_index = np.argmax(volt_subset)
  print("max index: ", max_index)
  # search for minimum either 50 points back or less in the subset:
  start = max_index - 50
  print("start: ", start)
  if start < 0 : start = 0
  try :
      peak = volt_subset[max_index] - np.min( np.array(volt_subset)[start:max_index] )
  except ValueError:
      print('max_index',str(max_index))
      print(volt_subset)
```

# Future Directions
- The way in which the peak is calculated can also be improved as our program assumes the upstroke occurs before 50 microseconds. Using derivatives or another technqiue may be more efficient to make peak calculation more robust for different situations. 

# Works Cited
- [Tkinter](https://docs.python.org/3/library/tk.html)
- [Matplotlib](https://matplotlib.org/3.4.3/contents.html)
# Acknowledgments 
[scopeclient.py](/scopeclient.py) was created as a collaboration between Curtis Chou and Kolo Wamba for Curtis' Fall 2021 Honors Project. A portion of the code that aided in plotting was created by Brendan Murtagh.
