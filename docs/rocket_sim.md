This is the main program.

module_engine, module_rocket, and module_structures all are classes for engines, rockets, and structures respectively.
The rocket module has instances of those classes in a list of parts. When the rocket's update function is called, it calls the update function for all parts in that list.
Any added modules must have a mass and a location attribute.

During setup, when parts are attached to the rocket, their location relative to the rocket origin is passed. However, during runtime the location will change to be relative to the center of mass.

The simulation, currently in simulation.py uses the velocity verlet algorithm to determine the rocket's position at each time step dt. This approximation is not perfect, but probably fine for our purposes.
