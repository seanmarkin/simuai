import numpy as np
import pygame
import json
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ObjectType(Enum):
    WALL = "wall"
    CENTER_BLOCK = "center_block"
    RED_BLOCK = "red_block"
    BLUE_BLOCK = "blue_block"

@dataclass
class Vector2D:
    x: float
    y: float
    
    def normalize(self) -> 'Vector2D':
        length = np.sqrt(self.x**2 + self.y**2)
        if length == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / length, self.y / length)
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)

@dataclass
class GameObject:
    obj_type: ObjectType
    position: Vector2D
    velocity: Vector2D
    size: int
    color: Tuple[int, int, int]
    is_static: bool = False
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Returns (left, top, right, bottom) bounds"""
        half_size = self.size // 2
        return (
            int(self.position.x - half_size),
            int(self.position.y - half_size),
            int(self.position.x + half_size),
            int(self.position.y + half_size)
        )
    
    def check_collision(self, other: 'GameObject') -> bool:
        """Check if this object collides with another object"""
        bounds1 = self.get_bounds()
        bounds2 = other.get_bounds()
        
        return not (bounds1[2] < bounds2[0] or bounds1[0] > bounds2[2] or
                   bounds1[3] < bounds2[1] or bounds1[1] > bounds2[3])

class PhysicsEngine:
    def __init__(self, grid_size: int = 1000):
        self.grid_size = grid_size
        self.objects: List[GameObject] = []
        self.time_step = 0
        
    def initialize_simulation(self):
        """Initialize the simulation with walls, center block, and mobile blocks"""
        # Clear existing objects
        self.objects.clear()
        
        # Create walls (green)
        wall_thickness = 20
        wall_color = (0, 255, 0)
        
        # Top wall
        self.objects.append(GameObject(
            obj_type=ObjectType.WALL,
            position=Vector2D(self.grid_size // 2, wall_thickness // 2),
            velocity=Vector2D(0, 0),
            size=wall_thickness,
            color=wall_color,
            is_static=True
        ))
        
        # Bottom wall
        self.objects.append(GameObject(
            obj_type=ObjectType.WALL,
            position=Vector2D(self.grid_size // 2, self.grid_size - wall_thickness // 2),
            velocity=Vector2D(0, 0),
            size=wall_thickness,
            color=wall_color,
            is_static=True
        ))
        
        # Left wall
        self.objects.append(GameObject(
            obj_type=ObjectType.WALL,
            position=Vector2D(wall_thickness // 2, self.grid_size // 2),
            velocity=Vector2D(0, 0),
            size=wall_thickness,
            color=wall_color,
            is_static=True
        ))
        
        # Right wall
        self.objects.append(GameObject(
            obj_type=ObjectType.WALL,
            position=Vector2D(self.grid_size - wall_thickness // 2, self.grid_size // 2),
            velocity=Vector2D(0, 0),
            size=wall_thickness,
            color=wall_color,
            is_static=True
        ))
        
        # Center block (green)
        self.objects.append(GameObject(
            obj_type=ObjectType.CENTER_BLOCK,
            position=Vector2D(self.grid_size // 2, self.grid_size // 2),
            velocity=Vector2D(0, 0),
            size=50,
            color=(0, 255, 0),
            is_static=True
        ))
        
        # Red block (mobile)
        red_start_pos = Vector2D(100, 100)
        red_velocity = self._get_random_velocity()
        self.objects.append(GameObject(
            obj_type=ObjectType.RED_BLOCK,
            position=red_start_pos,
            velocity=red_velocity,
            size=30,
            color=(255, 0, 0),
            is_static=False
        ))
        
        # Blue block (mobile)
        blue_start_pos = Vector2D(900, 900)
        blue_velocity = self._get_random_velocity()
        self.objects.append(GameObject(
            obj_type=ObjectType.BLUE_BLOCK,
            position=blue_start_pos,
            velocity=blue_velocity,
            size=30,
            color=(0, 0, 255),
            is_static=False
        ))
        
        self.time_step = 0
    
    def _get_random_velocity(self) -> Vector2D:
        """Generate a random velocity vector with unit speed"""
        angle = np.random.uniform(0, 2 * np.pi)
        return Vector2D(np.cos(angle), np.sin(angle))
    
    def update(self):
        """Update simulation for one time step"""
        self.time_step += 1
        
        # Update positions of mobile objects
        for obj in self.objects:
            if not obj.is_static:
                obj.position = obj.position + obj.velocity
        
        # Handle collisions
        self._handle_collisions()
        
        # Keep objects within bounds
        self._enforce_boundaries()
    
    def _handle_collisions(self):
        """Handle all object collisions with angle-of-incidence physics"""
        for i, obj1 in enumerate(self.objects):
            if obj1.is_static:
                continue
                
            for j, obj2 in enumerate(self.objects):
                if i == j:
                    continue
                    
                if obj1.check_collision(obj2):
                    self._resolve_collision(obj1, obj2)
    
    def _resolve_collision(self, obj1: GameObject, obj2: GameObject):
        """Resolve collision between two objects using angle-of-incidence physics"""
        if obj2.is_static:
            # Collision with static object (wall or center block)
            self._bounce_off_static(obj1, obj2)
        else:
            # Collision between two mobile objects
            self._bounce_off_mobile(obj1, obj2)
    
    def _bounce_off_static(self, mobile_obj: GameObject, static_obj: GameObject):
        """Bounce mobile object off static object"""
        # Calculate normal vector from static object to mobile object
        normal = mobile_obj.position - static_obj.position
        normal = normal.normalize()
        
        # Reflect velocity vector
        dot_product = mobile_obj.velocity.x * normal.x + mobile_obj.velocity.y * normal.y
        reflected_velocity = Vector2D(
            mobile_obj.velocity.x - 2 * dot_product * normal.x,
            mobile_obj.velocity.y - 2 * dot_product * normal.y
        )
        
        mobile_obj.velocity = reflected_velocity
        
        # Move object away from collision to prevent sticking
        mobile_obj.position = mobile_obj.position + normal * 2
    
    def _bounce_off_mobile(self, obj1: GameObject, obj2: GameObject):
        """Bounce two mobile objects off each other"""
        # Calculate normal vector between objects
        normal = obj1.position - obj2.position
        normal = normal.normalize()
        
        # Reflect both velocities
        for obj in [obj1, obj2]:
            dot_product = obj.velocity.x * normal.x + obj.velocity.y * normal.y
            reflected_velocity = Vector2D(
                obj.velocity.x - 2 * dot_product * normal.x,
                obj.velocity.y - 2 * dot_product * normal.y
            )
            obj.velocity = reflected_velocity
        
        # Move objects apart to prevent sticking
        separation = normal * 2
        obj1.position = obj1.position + separation
        obj2.position = obj2.position - separation
    
    def _enforce_boundaries(self):
        """Keep objects within the grid boundaries"""
        for obj in self.objects:
            if obj.is_static:
                continue
                
            half_size = obj.size // 2
            
            # Check horizontal boundaries
            if obj.position.x - half_size < 0:
                obj.position.x = half_size
                obj.velocity.x = abs(obj.velocity.x)  # Bounce right
            elif obj.position.x + half_size > self.grid_size:
                obj.position.x = self.grid_size - half_size
                obj.velocity.x = -abs(obj.velocity.x)  # Bounce left
            
            # Check vertical boundaries
            if obj.position.y - half_size < 0:
                obj.position.y = half_size
                obj.velocity.y = abs(obj.velocity.y)  # Bounce down
            elif obj.position.y + half_size > self.grid_size:
                obj.position.y = self.grid_size - half_size
                obj.velocity.y = -abs(obj.velocity.y)  # Bounce up
    
    def get_state(self) -> Dict:
        """Get current simulation state for AI learning"""
        state = {
            "time_step": self.time_step,
            "grid_size": self.grid_size,
            "objects": []
        }
        
        for obj in self.objects:
            obj_state = {
                "type": obj.obj_type.value,
                "position": {"x": obj.position.x, "y": obj.position.y},
                "velocity": {"x": obj.velocity.x, "y": obj.velocity.y},
                "size": obj.size,
                "color": obj.color,
                "is_static": obj.is_static
            }
            state["objects"].append(obj_state)
        
        return state
    
    def save_state_to_file(self, filename: str):
        """Save current state to JSON file"""
        state = self.get_state()
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)

class SimulationController:
    def __init__(self, grid_size: int = 1000, display_scale: float = 0.5):
        self.physics_engine = PhysicsEngine(grid_size)
        self.display_scale = display_scale
        self.display_size = int(grid_size * display_scale)
        
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_size, self.display_size))
        pygame.display.set_caption("Causal AI Simulation")
        self.clock = pygame.time.Clock()
        
        # Simulation control
        self.running = False
        self.paused = False
        
        # Initialize simulation
        self.physics_engine.initialize_simulation()
    
    def start(self):
        """Start the simulation"""
        self.running = True
        self.paused = False
        self._main_loop()
    
    def pause(self):
        """Pause/unpause the simulation"""
        self.paused = not self.paused
    
    def restart(self):
        """Restart the simulation"""
        self.physics_engine.initialize_simulation()
        self.paused = False
    
    def _main_loop(self):
        """Main simulation loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause()
                    elif event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_s:
                        self.physics_engine.save_state_to_file(f"simulation_state_{self.physics_engine.time_step}.json")
            
            # Update physics if not paused
            if not self.paused:
                self.physics_engine.update()
            
            # Render
            self._render()
            
            # Control frame rate
            self.clock.tick(60)
        
        pygame.quit()
    
    def _render(self):
        """Render the simulation"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw objects
        for obj in self.physics_engine.objects:
            scaled_pos = (int(obj.position.x * self.display_scale), 
                         int(obj.position.y * self.display_scale))
            scaled_size = int(obj.size * self.display_scale)
            
            pygame.draw.rect(self.screen, obj.color,
                           (scaled_pos[0] - scaled_size//2,
                            scaled_pos[1] - scaled_size//2,
                            scaled_size, scaled_size))
        
        # Draw UI
        self._draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw UI elements"""
        font = pygame.font.Font(None, 36)
        
        # Status text
        status = "PAUSED" if self.paused else "RUNNING"
        status_text = font.render(f"Status: {status}", True, (255, 255, 255))
        self.screen.blit(status_text, (10, 10))
        
        # Time step
        time_text = font.render(f"Step: {self.physics_engine.time_step}", True, (255, 255, 255))
        self.screen.blit(time_text, (10, 50))
        
        # Controls
        controls_text = font.render("Space: Pause/Resume | R: Restart | S: Save State", True, (255, 255, 255))
        self.screen.blit(controls_text, (10, self.display_size - 40))

def main():
    """Main function to run the simulation"""
    print("Starting Causal AI Simulation...")
    print("Controls:")
    print("  SPACE - Pause/Resume")
    print("  R - Restart")
    print("  S - Save current state")
    print("  ESC/Close window - Exit")
    
    controller = SimulationController()
    controller.start()

if __name__ == "__main__":
    main() 