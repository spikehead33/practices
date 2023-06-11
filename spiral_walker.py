from typing import List
import unittest
from enum import Enum
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


class WalkerDirection(Enum):
    LEFT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3


@dataclass
class Boundary:
    leftbound: int
    rightbound: int
    topbound: int
    lowerbound: int
    
    def __init__(self, max_row: int, max_col: int) -> None:
        self.leftbound = 0
        self.topbound = 0
        self.rightbound = max_col
        self.lowerbound = max_row


class EdgeDetector:
    boundary: Boundary
   
    def __init__(self, boundary: Boundary) -> None:
        self.boundary = boundary

    def is_out_of_boundary(self, pos: Position) -> bool:
        return (
            pos.y < self.boundary.leftbound
            or pos.y > self.boundary.rightbound
            or pos.x < self.boundary.topbound
            or pos.x > self.boundary.lowerbound
        )

    def is_dead_end(self) -> bool:
        return (
            self.boundary.leftbound == self.boundary.rightbound
            and self.boundary.topbound == self.boundary.lowerbound
        )

    def eliminate_top(self):
        self.boundary.topbound += 1

    def eliminate_lower(self):
        self.boundary.lowerbound -= 1

    def eliminate_left(self):
        self.boundary.leftbound += 1

    def eliminate_right(self):
        self.boundary.rightbound -= 1


class SpiralWalker:
    grid: List[List[int]]
    direction: WalkerDirection
    detector: EdgeDetector
    curr_position: Position
    
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.direction = WalkerDirection.RIGHT
        self.detector = EdgeDetector(Boundary(len(grid)-1, len(grid[0])-1))
        self.curr_position = Position(0, 0)

    def get_next_position(self):
        x, y = self.curr_position.x, self.curr_position.y
        if self.direction == WalkerDirection.RIGHT:
            return Position(x, y+1)
        elif self.direction == WalkerDirection.LEFT:
            return Position(x, y-1)
        elif self.direction == WalkerDirection.UP:
            return Position(x-1, y)
        return Position(x+1, y)

    def change_direction(self):
        if self.direction == WalkerDirection.RIGHT:
            self.direction = WalkerDirection.DOWN
        elif self.direction == WalkerDirection.DOWN:
            self.direction = WalkerDirection.LEFT
        elif self.direction == WalkerDirection.LEFT:
            self.direction = WalkerDirection.UP
        else:
            self.direction = WalkerDirection.RIGHT

    def reduce_boundary(self):
        if self.direction == WalkerDirection.RIGHT:
            self.detector.eliminate_top()
        elif self.direction == WalkerDirection.DOWN:
            self.detector.eliminate_right()
        elif self.direction == WalkerDirection.LEFT:
            self.detector.eliminate_lower()
        else:
            self.detector.eliminate_left()

    def move(self) -> None:
        next_position = self.get_next_position()
        if self.detector.is_out_of_boundary(next_position):
            self.reduce_boundary()
            self.change_direction()
            next_position = self.get_next_position()
        self.curr_position = next_position
        
    def walk(self) -> None:
        if len(self.grid) == 0:
            raise ValueError("Grid size should not be 0")

        print(self.grid[0][0])
        while not self.detector.is_dead_end():
            self.move()
            x = self.curr_position.x
            y = self.curr_position.y
            print(self.grid[x][y])
 

class TestEdgeDetector(unittest.TestCase):
    def test_is_out_of_boundary(self):
        detector = EdgeDetector(Boundary(4, 4))
        self.assertFalse(detector.is_out_of_boundary(Position(1, 4)))
        
        detector.eliminate_right()
        self.assertTrue(detector.is_out_of_boundary(Position(1, 4)))
        self.assertFalse(detector.is_out_of_boundary(Position(1, 3)))

        detector.eliminate_top()
        detector.eliminate_top()
        self.assertTrue(detector.is_out_of_boundary(Position(1, 3)))
        self.assertFalse(detector.is_out_of_boundary(Position(2, 1)))
        
        detector.eliminate_left()
        self.assertTrue(detector.is_out_of_boundary(Position(0, 3)))
        
        
    def test_is_dead_end(self):
        detector = EdgeDetector(Boundary(0, 0))
        self.assertTrue(detector.is_dead_end())
        

class TestSpiralWalker(unittest.TestCase):
    def test_change_direction(self):
        ...
        
    def test_get_next_position(self):
        ...
        
    def test_move(self):
        ...
        
        
# Driver code
if __name__ == "__main__":
    print("[[1]]")
    grid = [[1]]
    walker = SpiralWalker(grid)
    walker.walk()
    print()

    print("[[0, 1], [2, 3]]")
    grid = [[0, 1],
            [2, 3]]
    walker = SpiralWalker(grid)
    walker.walk()
    print()
    
    print("[[0, 1, 2], [3, 4, 5], [6, 7, 8]]")
    grid = [[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]]
    walker = SpiralWalker(grid)
    walker.walk()
    print()
