import numpy as np
import pygame
import json
import time
import sys
import traceback
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
        try:
            length = np.sqrt(self.x**2 + self.y**2)
            if length == 0:
                return Vector2D(0, 0)
            return Vector2D(self.x / length, self.y / length)
        except Exception as e:
            print(f"Error normalizing vector: {e}")
            return Vector2D(0, 0)
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        try:
            return Vector2D(self.x + other.x, self.y + other.y)
        except Exception as e:
            print(f"Error adding vectors: {e}")
            return Vector2D(0, 0)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        try:
            return Vector2D(self.x - other.x, self.y - other.y)
        except Exception as e:
            print(f"Error subtracting vectors: {e}")
            return Vector2D(0, 0)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        try:
            return Vector2D(self.x * scalar, self.y * scalar)
        except Exception as e:
            print(f"Error multiplying vector by scalar: {e}")
            return Vector2D(0, 0)

@dataclass
class GameObject:
    obj_type: ObjectType
    position: Vector2D
    velocity: Vector2D
    size: int
    color: Tuple[int, int, int]
    is_static: bool = False
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        try:
            half_size = self.size // 2
            return (
                int(self.position.x - half_size),
                int(self.position.y - half_size),
                int(self.position.x + half_size),
                int(self.position.y + half_size)
            )
        except Exception as e:
            print(f"Error calculating bounds: {e}")
            return (0, 0, 0, 0)
    
    def check_collision(self, other: 'GameObject') -> bool:
        try:
            bounds1 = self.get_bounds()
            bounds2 = other.get_bounds()
            return not (bounds1[2] < bounds2[0] or bounds1[0] > bounds2[2] or
                        bounds1[3] < bounds2[1] or bounds1[1] > bounds2[3])
        except Exception as e:
            print(f"Error checking collision: {e}")
            return False

class PhysicsEngine:
    def __init__(self, grid_size: int = 1000):
        self.grid_size = grid_size
        self.objects: List[GameObject] = []
        self.time_step = 0
        self.error_count = 0
        self.max_errors = 10
    
    def initialize_simulation(self):
        try:
            self.objects.clear()
            wall_thickness = 20
            wall_color = (0, 255, 0)
            self.objects.append(GameObject(ObjectType.WALL, Vector2D(self.grid_size // 2, wall_thickness // 2), Vector2D(0, 0), wall_thickness, wall_color, True))
            self.objects.append(GameObject(ObjectType.WALL, Vector2D(self.grid_size // 2, self.grid_size - wall_thickness // 2), Vector2D(0, 0), wall_thickness, wall_color, True))
            self.objects.append(GameObject(ObjectType.WALL, Vector2D(wall_thickness // 2, self.grid_size // 2), Vector2D(0, 0), wall_thickness, wall_color, True))
            self.objects.append(GameObject(ObjectType.WALL, Vector2D(self.grid_size - wall_thickness // 2, self.grid_size // 2), Vector2D(0, 0), wall_thickness, wall_color, True))
            self.objects.append(GameObject(ObjectType.CENTER_BLOCK, Vector2D(self.grid_size // 2, self.grid_size // 2), Vector2D(0, 0), 50, (0, 255, 0), True))
            red_start_pos = Vector2D(100, 100)
            red_velocity = self._get_random_velocity()
            self.objects.append(GameObject(ObjectType.RED_BLOCK, red_start_pos, red_velocity, 30, (255, 0, 0), False))
            blue_start_pos = Vector2D(900, 900)
            blue_velocity = self._get_random_velocity()
            self.objects.append(GameObject(ObjectType.BLUE_BLOCK, blue_start_pos, blue_velocity, 30, (0, 0, 255), False))
            self.time_step = 0
            self.error_count = 0
            print("Simulation initialized successfully")
        except Exception as e:
            print(f"Error initializing simulation: {e}")
            traceback.print_exc()
            raise
    
    def _get_random_velocity(self) -> Vector2D:
        try:
            angle = np.random.uniform(0, 2 * np.pi)
            return Vector2D(np.cos(angle), np.sin(angle))
        except Exception as e:
            print(f"Error generating random velocity: {e}")
            return Vector2D(1, 0)
    
    def update(self):
        try:
            self.time_step += 1
            for obj in self.objects:
                if not obj.is_static:
                    obj.position = obj.position + obj.velocity
            self._handle_collisions()
            self._enforce_boundaries()
        except Exception as e:
            self.error_count += 1
            print(f"Error in physics update (step {self.time_step}): {e}")
            if self.error_count >= self.max_errors:
                print("Too many errors, stopping simulation")
                raise
    
    def _handle_collisions(self):
        try:
            for i, obj1 in enumerate(self.objects):
                if obj1.is_static:
                    continue
                for j, obj2 in enumerate(self.objects):
                    if i == j:
                        continue
                    if obj1.check_collision(obj2):
                        self._resolve_collision(obj1, obj2)
        except Exception as e:
            print(f"Error handling collisions: {e}")
    
    def _resolve_collision(self, obj1: GameObject, obj2: GameObject):
        try:
            if obj2.is_static:
                self._bounce_off_static(obj1, obj2)
            else:
                self._bounce_off_mobile(obj1, obj2)
        except Exception as e:
            print(f"Error resolving collision: {e}")
    
    def _bounce_off_static(self, mobile_obj: GameObject, static_obj: GameObject):
        try:
            normal = mobile_obj.position - static_obj.position
            normal = normal.normalize()
            dot_product = mobile_obj.velocity.x * normal.x + mobile_obj.velocity.y * normal.y
            reflected_velocity = Vector2D(
                mobile_obj.velocity.x - 2 * dot_product * normal.x,
                mobile_obj.velocity.y - 2 * dot_product * normal.y
            )
            mobile_obj.velocity = reflected_velocity
            mobile_obj.position = mobile_obj.position + normal * 2
        except Exception as e:
            print(f"Error bouncing off static object: {e}")
    
    def _bounce_off_mobile(self, obj1: GameObject, obj2: GameObject):
        try:
            normal = obj1.position - obj2.position
            normal = normal.normalize()
            for obj in [obj1, obj2]:
                dot_product = obj.velocity.x * normal.x + obj.velocity.y * normal.y
                reflected_velocity = Vector2D(
                    obj.velocity.x - 2 * dot_product * normal.x,
                    obj.velocity.y - 2 * dot_product * normal.y
                )
                obj.velocity = reflected_velocity
            separation = normal * 2
            obj1.position = obj1.position + separation
            obj2.position = obj2.position - separation
        except Exception as e:
            print(f"Error bouncing off mobile object: {e}")
    
    def _enforce_boundaries(self):
        try:
            for obj in self.objects:
                if obj.is_static:
                    continue
                half_size = obj.size // 2
                if obj.position.x - half_size < 0:
                    obj.position.x = half_size
                    obj.velocity.x = abs(obj.velocity.x)
                elif obj.position.x + half_size > self.grid_size:
                    obj.position.x = self.grid_size - half_size
                    obj.velocity.x = -abs(obj.velocity.x)
                if obj.position.y - half_size < 0:
                    obj.position.y = half_size
                    obj.velocity.y = abs(obj.velocity.y)
                elif obj.position.y + half_size > self.grid_size:
                    obj.position.y = self.grid_size - half_size
                    obj.velocity.y = -abs(obj.velocity.y)
        except Exception as e:
            print(f"Error enforcing boundaries: {e}")
    
    def get_state(self) -> Dict:
        try:
            state = {
                "time_step": self.time_step,
                "grid_size": self.grid_size,
                "error_count": self.error_count,
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
        except Exception as e:
            print(f"Error getting state: {e}")
            return {"error": str(e), "time_step": self.time_step}
    
    def save_state_to_file(self, filename: str):
        try:
            state = self.get_state()
            with open(filename, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"State saved to {filename}")
        except Exception as e:
            print(f"Error saving state to {filename}: {e}")

class SimulationController:
    def __init__(self, grid_size: int = 1000, display_scale: float = 0.5):
        try:
            self.physics_engine = PhysicsEngine(grid_size)
            self.display_scale = display_scale
            self.display_size = int(grid_size * display_scale)
            pygame.init()
            self.screen = pygame.display.set_mode((self.display_size, self.display_size))
            pygame.display.set_caption("Causal AI Simulation")
            self.clock = pygame.time.Clock()
        except Exception as e:
            print(f"Error initializing Pygame: {e}")
            raise
        self.running = False
        self.paused = False
        self.render_errors = 0
        self.max_render_errors = 5
        self.physics_engine.initialize_simulation()
    
    def start(self):
        try:
            self.running = True
            self.paused = False
            self._main_loop()
        except Exception as e:
            print(f"Fatal error in simulation: {e}")
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def pause(self):
        self.paused = not self.paused
    
    def restart(self):
        try:
            self.physics_engine.initialize_simulation()
            self.paused = False
            self.render_errors = 0
            print("Simulation restarted")
        except Exception as e:
            print(f"Error restarting simulation: {e}")
    
    def cleanup(self):
        try:
            pygame.quit()
            print("Simulation cleaned up")
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    def _main_loop(self):
        while self.running:
            try:
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
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
                if not self.paused:
                    self.physics_engine.update()
                self._render()
                self.clock.tick(60)
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.render_errors += 1
                if self.render_errors >= self.max_render_errors:
                    print("Too many render errors, stopping simulation")
                    break
                time.sleep(0.1)
    
    def _render(self):
        try:
            self.screen.fill((0, 0, 0))
            for obj in self.physics_engine.objects:
                scaled_pos = (int(obj.position.x * self.display_scale), int(obj.position.y * self.display_scale))
                scaled_size = int(obj.size * self.display_scale)
                pygame.draw.rect(self.screen, obj.color,
                                 (scaled_pos[0] - scaled_size//2,
                                  scaled_pos[1] - scaled_size//2,
                                  scaled_size, scaled_size))
            self._draw_ui()
            pygame.display.flip()
        except Exception as e:
            print(f"Error rendering: {e}")
            raise
    
    def _draw_ui(self):
        try:
            font = pygame.font.Font(None, 36)
            status = "PAUSED" if self.paused else "RUNNING"
            status_text = font.render(f"Status: {status}", True, (255, 255, 255))
            self.screen.blit(status_text, (10, 10))
            time_text = font.render(f"Step: {self.physics_engine.time_step}", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 50))
            if self.physics_engine.error_count > 0:
                error_text = font.render(f"Errors: {self.physics_engine.error_count}", True, (255, 0, 0))
                self.screen.blit(error_text, (10, 90))
            controls_text = font.render("Space: Pause/Resume | R: Restart | S: Save State | ESC: Exit", True, (255, 255, 255))
            self.screen.blit(controls_text, (10, self.display_size - 40))
        except Exception as e:
            print(f"Error drawing UI: {e}")

def main():
    print("Starting Causal AI Simulation...")
    print("Controls:")
    print("  SPACE - Pause/Resume")
    print("  R - Restart")
    print("  S - Save current state")
    print("  ESC - Exit")
    print("  Close window - Exit")
    try:
        controller = SimulationController()
        controller.start()
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
    finally:
        print("Simulation ended")

if __name__ == "__main__":
    main() 