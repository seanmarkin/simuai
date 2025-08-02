# Causal AI Simulation

A foundational AI model that learns to causally model rule-based systems using ontological priors.

## Features

- **Physics-based simulation** with 1000x1000 grid
- **Static objects**: Green walls and center block
- **Mobile objects**: Red and blue blocks with random initial movement
- **Angle-of-incidence bounce physics** for realistic collisions
- **Real-time visualization** with Pygame
- **State output** for AI learning
- **Extensible architecture** for future enhancements

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the simulation:
```bash
python simulation.py
```

### Test the physics engine:
```bash
python test_simulation.py
```

## Controls

- **SPACE**: Pause/Resume simulation
- **R**: Restart simulation
- **S**: Save current state to JSON file
- **Close window**: Exit simulation

## Architecture

### Core Components

1. **PhysicsEngine**: Handles physics calculations, collisions, and state management
2. **SimulationController**: Manages the visual interface and user controls
3. **GameObject**: Represents simulation objects with position, velocity, and properties
4. **Vector2D**: 2D vector mathematics for physics calculations

### State Output

The simulation outputs state data in JSON format for AI learning:

```json
{
  "time_step": 123,
  "grid_size": 1000,
  "objects": [
    {
      "type": "red_block",
      "position": {"x": 150.5, "y": 200.3},
      "velocity": {"x": 0.707, "y": -0.707},
      "size": 30,
      "color": [255, 0, 0],
      "is_static": false
    }
  ]
}
```

### Extensibility

The simulation is designed to be easily extended:

- Add new object types in the `ObjectType` enum
- Implement new physics rules in `PhysicsEngine`
- Add new interaction patterns in collision handling
- Extend the visual interface for new features

## Simulation Rules

### Context
- 1000x1000 grid world

### Objects
- **Walls**: Static green boundaries
- **Center Block**: Static green block in center
- **Red Block**: Mobile block with random movement
- **Blue Block**: Mobile block with random movement

### Translation Rules
- Mobile blocks move one grid position per time step
- Static objects remain immobile

### Interaction Rules
- Mobile blocks bounce off walls and static objects
- Mobile blocks bounce off each other
- All collisions follow angle-of-incidence physics

## Troubleshooting

If you encounter issues:

1. **Pygame not found**: Make sure you've installed the requirements with `pip install -r requirements.txt`
2. **Display issues**: The simulation uses a 500x500 display window (scaled from 1000x1000)
3. **Performance**: The simulation runs at 60 FPS by default

## Next Steps

This simulation provides the foundation for:
- AI learning of causal relationships
- Extension to more complex rule-based systems
- Integration with machine learning models
- Development of more sophisticated physics rules 