README for the first CX 4230 Project

# Event-Driven Simulaion Project: City Simulation


We are using Python3.

If TAs want to run chart

To run the project:
- navigate to CX4230_Project1/ directory
- run python main.py


## Project Files

- main.py is the main functionality containing all globals and running the events

- grid.py contains all the code for the city Grid and each square (location) in the city called GridSquare

- person.py contains all the code for moving a person in and out and relevant data for each person

- event.py implements Comparable interface so the events can be placed in a queue and holds metadata about each event

- grid_view.py contains the code for drawing plots and producing the animation

- Statistics for generating distributions are saved in csv files and read in using prob_distributions.py



- Grid system
- Number of people living in Grid determines population density

