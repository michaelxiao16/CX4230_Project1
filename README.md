README for the first CX 4230 Project

# Event-Driven Simulation Project: City Simulation

First, to download this git project, DO NOT download the zip file. 
Instead, run git clone https://github.com/michaelxiao16/CX4230_Project1.git

We are using Python3. To get this to run on the PACE cluster, we did the following:
```
> module load anaconda3/2019.10
> conda activate
```

This will start a anaconda virtual environment, on which Python3+ should be the default. 
Verify that the version of python running is Python3+. In our case we had Python 3.7.4

Alternatively, you can use
```
> module load python/3.6
```

On PACE, you may have to load certain modules, including Numpy and Scipy. To do this, run
```
> module load <insert module name here>
```

All other modules needed for the project, such as bintrees, have been included and do not need
to be installed or loaded. Keep in mind, ffmpeg and matplotlib will not run on the PACE cluster,
so to generate the accompanying plots and videos, the code must be run locally. To do this,
uncomment any calls to grid_view() or matplotlib.

To run the project:
```
> cd CX4230_Project1/ 
> python main.py
```

Additionally, all the statistical analyses, including generating confidence intervals, are contained within stats_test.py.
In order to run this:
```
> cd CX4230_Project1/
> python stats_test.py
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


