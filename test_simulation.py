import json
from simulation import PhysicsEngine

def test_physics_engine():
    """Test the physics engine functionality"""
    print("Testing Physics Engine...")
    
    # Create physics engine
    engine = PhysicsEngine(grid_size=1000)
    engine.initialize_simulation()
    
    # Test initial state
    initial_state = engine.get_state()
    print(f"Initial time step: {initial_state['time_step']}")
    print(f"Number of objects: {len(initial_state['objects'])}")
    
    # Test object types
    object_types = [obj['type'] for obj in initial_state['objects']]
    expected_types = ['wall', 'wall', 'wall', 'wall', 'center_block', 'red_block', 'blue_block']
    
    print(f"Object types: {object_types}")
    print(f"Expected types: {expected_types}")
    
    # Test mobile objects have velocity
    mobile_objects = [obj for obj in initial_state['objects'] if not obj['is_static']]
    print(f"Mobile objects: {len(mobile_objects)}")
    
    for obj in mobile_objects:
        velocity = obj['velocity']
        speed = (velocity['x']**2 + velocity['y']**2)**0.5
        print(f"{obj['type']} velocity: ({velocity['x']:.3f}, {velocity['y']:.3f}), speed: {speed:.3f}")
    
    # Test simulation update
    print("\nTesting simulation update...")
    for i in range(10):
        engine.update()
        state = engine.get_state()
        print(f"Step {state['time_step']}: Red block at ({state['objects'][5]['position']['x']:.1f}, {state['objects'][5]['position']['y']:.1f})")
    
    # Test state saving
    engine.save_state_to_file("test_state.json")
    print("\nState saved to test_state.json")
    
    print("Physics engine test completed successfully!")

if __name__ == "__main__":
    test_physics_engine() 