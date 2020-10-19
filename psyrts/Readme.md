# PsyRTS Model

## Summary

A simple model, consisting of three agent types: participant, competitor, and predators. The participant, predator and competitors wander around the grid at random. Participants and Competitors forage for resources, and predators preys participants and competitors if they end up on the same grid cell.


The model is tests and demonstrates several concepts a:
 -  Impact of Visibility in Exploration
 -  Multiple agent types affecting Exploitation
 
## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

## Files

* ``psyrts/random_walker.py``: This defines the ``RandomWalker`` agent, which implements the behavior of moving randomly across a grid, one cell at a time. Both the Wolf and Sheep agents will inherit from it.
* ``psyrts/test_random_walk.py``: Defines a simple model and a text-only visualization intended to make sure the RandomWalk class was working as expected. This doesn't actually model anything, but serves as an ad-hoc unit test. To run it, ``cd`` into the ``wolf_sheep`` directory and run ``python test_random_walk.py``. You'll see a series of ASCII grids, one per model step, with each cell showing a count of the number of agents in it.
* ``psyrts/agents.py``: Defines the Participant, Competitor, Predator, Central Place and Resources agent classes.
* ``psyrts/schedule.py``: Defines a custom variant on the RandomActivation scheduler, where all agents of one class are activated (in random order) before the next class goes -- e.g. all the wolves go, then all the sheep, then all the grass.
* ``psyrts/model.py``: Defines the psyrts model itself
* ``psyrts/server.py``: Sets up the interactive visualization server
* ``psyrts/BatchRunnerPsyRTS.py``: Sets a Batch process to run the model for different number of iterations
* ``run.py``: Launches a model visualization server.

## Further Reading

This model is based on some of these ideas:

 Osman, M & Verduga, O (2019) The future of problem solving research is not complexity, but dynamic uncertainty https://journals.ub.uni-heidelberg.de/index.php/jddm/article/view/69300
 Verduga, O & Osman, M (2019) PsyRTS: a Web Platform for Experiments in Human Decision-Making in RTS Environments https://ieeexplore.ieee.org/document/8848101

