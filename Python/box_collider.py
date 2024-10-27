from point_collider import PointCollider

class BoxCollider:
    def __init__(self, x, y, w, h, gap=2) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.gap = gap

    def generate_point_colliders(self):
        point_colliders = []
        for i in  range(0, self.w+1, self.gap):
            point_colliders.append(PointCollider(self.x + i, self.y))
            point_colliders.append(PointCollider(self.x + i, self.y + self.h))
        for i in  range(0, self.h+1, self.gap):
            point_colliders.append(PointCollider(self.x, self.y + i))
            point_colliders.append(PointCollider(self.x + self.w, self.y + i))

        return point_colliders
