# artisoc-traffic-model2018

Traffic model for the effect of lane changing on road throughput. New repository for MS2.

## Simulation elements:
* Road
The Space in which the simulation agents move and interact. 
Road size is 3x300 where the length of a car is 1, and obeys cyclic boundary conditions. 
Stop lights are placed at uniform intervals along the road.
The user can define an Ideal speed for the road that determines the speed distribution of cars and the stop light timings.

* Cars
The primary agents used in the simulation.
All cars have a maximum speed taken from a normal distribution centered at the simulation's ideal speed.
The number of cars on the road and the probability that a car will be asocial can be defined by the user.

Dimensions are  1x1, and cars are divided into two types: Social and Asocial (apathetic).

    + Social
Social cars (as the name implies) try to minimize their own negative effect on the road throughput. 
They will only change lanes when no car behind them will be forced to slow down.

    + Asocial
Asocial (apathetic) cars do not pay attention to their effect on the other cars on the road.
They change lanes whenever they seen an opportunity to speed up, ignoring cars behind them.

All cars attempt to accelerate to their ideal speed whenever possible.

* Stop lights
Placed in uniform intervals along the road.
Cycles between "red" and "green" states, with the "green" state allowing cars to pass through.
Spacing of lights and cycle length are calibrated to create a "Green Wave" based on the road's defined Ideal Speed.
Number of "Green Waves" and "green" signal active time are user-defined.

## Car behavior

# Initial conditions

Cars begin the simulation with these initial parameters:
* Random (x,y) position on the road
* Random (normal distribution around road ideal speed) starting speed, equal to their maximum speed
* Fixed per-step acceleration (currently fixed at 5m/s^2)
* Fixed starting "patience" value, which determines how long they will wait before changing lanes (currently fixed at 0)
* Target lane that they tend to lane change towards *(not currently active)*

# Simulation step
Each car step will proceed as follows, in order:

1. If the car is not at its maximum speed, it will accelerate (increment its speed by its acceleration).

2. Check its "headway" (open space ahead of them).

    1. Check the distance to the next red light. This determines the maximum distance it can possibly move this step.

    2. Check the distance to the nearest cars in front, on the current lane and neighboring lanes.

    3. Headway is the lowest value among the distances checked.

3. Depending on conditions, action will be taken:

    * If headway is greater than current speed, then continue forward.

    * If headway is less than current speed, check patience value.

        * If patience != 0, then decelerate to a speed = headway\*0.6 and decrement patience.

        * If patience == 0, change lanes to most open lane if asocial. If social, one last check:

            * If there is a car behind on the target lane, do not lane change. Decrement patience.

            * Otherwise, change lanes.

4. Move forward equal to current speed.

## Green Wave

The stop lights are timed in such a way that a car moving at the ideal speed going through a green light will *never* hit a red light.
This gives the appearance of a "wave" of green signals.