import numpy as np
import pygame

COLLISION_SLOWDOWN_X = 0.5
COLLISION_SLOWDOWN_Y = 0.9


class PointCollider:
    def __init__(self, x, y) -> None:
        self.pos = np.array([x, y], dtype=float)
        self.is_active = True

    def check_collision(self, obj):
        distance = np.linalg.norm(self.pos - obj.pos)
        if distance <= obj.radius:
            return True, distance
        return False, distance

    def resolve_overlap(self, obj):
        # Calculate the distance vector and magnitude
        distance_vector = obj.pos - self.pos
        distance = np.linalg.norm(distance_vector)

        # Calculate the overlap (if any)
        overlap = obj.radius - distance

        # Normalize the distance vector to get the direction of push
        direction = distance_vector / distance

        # Resolve Overlap
        obj.pos += direction * overlap

    def handle_collision(self, obj):
        obj.vel = (
            obj.vel
            - 2
            * (obj.vel).dot(obj.pos - self.pos)
            * (obj.pos - self.pos)
            / np.linalg.norm(obj.pos - self.pos) ** 2
        )
        obj.vel[0] *= COLLISION_SLOWDOWN_X
        obj.vel[1] *= COLLISION_SLOWDOWN_Y

        if np.abs(obj.vel[1]) < 50:
            obj.vel[1] = 0
        if np.abs(obj.vel[0]) < 10:
            obj.vel[0] = 0
        #     obj.vel[0] = 0
        #     obj.vel[1] = 0

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (0, 255, 255),
            (int(self.pos[0]), int(self.pos[1])),
            1,
        )
