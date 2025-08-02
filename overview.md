# intro
we are building a new foundational model for artificial intelligence (ai).  

# what makes this model unique
this model is unique because instead of learning to output human plausible language, recognize images, or generate images, it instead learned to causally model any rule based system at any level of detail. 

# whats the benefit
unlike probabilistic systems like llms, that struggle to create causally plausible out of distribution predictions, this system will be able to create out of distribution predictions.

# how does this model work
the system does not use probabilistic association (e.g, seeing enough examples) instead it assumes a minimal set of ontological priors that constrain models in a way that allows for arbitrary simulation at an arbitrary level of abstraction.

the ontological priors include:

- context - this defines the translation options for the various objects.  example: racetrack
- objects - these define the various concepts that are critical to that simulation.  example: race cars, race flags
- object translation rules - these define the how the object can move throughout the context. example: friction 
- object interaction rules - these define how objects react to interactions with objects. example: collisions

# what gets built first
first we need to build a simple simultaion that can be extended over time.  

## initial simulation features
this simulation will be a physics based simulation.

context: 
- the context will be a square consisting of 1000 by 1000 smaller squares.

objects:
- four green walls surrounding the simulation
- a center green block
- one mobile red block
- one mobile blue block

object translation rules:
    four green walls:
        - these walls are immobile
    a center green block:
        - this block is immobile
    mobile red block:
        - this block moves straight unless to the next block each turn of the simulation
    mobile blue block
        - this block moves straight unless to the next block each turn of the simulation

object interaction rules
    four green walls:
        - these walls do not change state with they interact with another object
    a center green block:
        - this block does not change state with they interact with another object
    mobile red block:
        - if this block interacts with another object, it reflects or 'bounces' incident to the interaction.
    mobile blue block
        - if this block interacts with another object, it reflects or 'bounces' incident to the interaction.

# instruction to cursor agent
1. please review all content and let me know if the plan makes sense.:  

    if the plan makes sense: 
        2. please build the simulation
        3. please test the simulation to make sure it adheres to the spec.  

    if the plan does not make sense:
        2. please ask me clarification questions.  

# cursor questions:
Q1: Movement Direction: For the mobile blocks, should they start moving in random directions, or do you want to specify initial directions?

A1: 
blocks should start by moving in random directions but at the same speed.

Q2: Movement Speed: Should both blocks move at the same speed (one grid position per turn), or can they have different speeds?

A2: both blocks should move at the same speed.  Speed = one block per turn.  

Q3: Bounce Physics: When blocks bounce off walls/objects, should they follow realistic angle-of-incidence physics, or use a simpler reflection rule?

A3: the blocks should follow angle-of-incidence physics. 

Q4: Block-Object Collisions: When the red and blue blocks collide with each other, should they both bounce, or do you want different interaction rules?

A4: when the red and blue blocks collide with each other, they should both bounce. 

Q5: Simulation Control: Do you want the ability to pause/resume the simulation, or should it run continuously?

A5: great catch.  yes, i should be able to pause/resume/restart the simulation.

Q6: Visualization: Should this be a real-time visual simulation, or do you want to output the state at each turn?

A6: both.  the simulation should be visual as well as outputing the state.  

the state output will be used by the ai to learn the simulation so it should be returned and then a human readable interface should be built on top of that data that could be output to a text file.  this architecture should allow for the ai simulation to ingest the simulation output while still allowing for a me to view the output.

Additional criteria based on your questions:

- the simulation should be developed in python. 
- the simulation should be designed to be extended and enhanced.  