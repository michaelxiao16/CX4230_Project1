README for the first CX 4230 Project

# Event-Driven Simulation Project: City Simulation


We are using Python3. To get this to run on the PACE cluster, we did the following:
```
> module load anaconda3/2019.10
> conda activate
```
And verify that the version of python running is Python3+, in our case we had Python 3.7.4


To run the project:
```
> cd CX4230_Project1/ 
> python main.py
```

Images and video are produced by our simulation and viewable as "chart.mp4". If TAs want to run our images and video, 
they will need to download and install ffmpeg at https://www.ffmpeg.org/download.html

## Project Files

- main.py is the main functionality containing all globals and running the events

- grid.py contains all the code for the city Grid and each square (location) in the city called GridSquare

- person.py contains all the code for moving a person in and out and relevant data for each person

- event.py implements Comparable interface so the events can be placed in a queue and holds metadata about each event

- grid_view.py contains the code for drawing plots and producing the animation

- Statistics for generating distributions are saved in csv files and read in using prob_distributions.py



## Other Notes
- Grid system
- Number of people living in Grid determines population density

