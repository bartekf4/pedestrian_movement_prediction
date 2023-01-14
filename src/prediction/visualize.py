import cv2
import numpy as np

from board import Board
from config import *
from pedestrian import Pedestrian


class WriteFrameToVideo:
    def __init__(self, size, fps, filename_='warped.avi'):
        self.filename = filename_
        self.size = size
        self.out = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*'XVID'), 30, (1280 + 1, 404 + 1))

    def write(self, frame):
        frame = frame.astype(np.uint8)
        cv2.imshow("pred", frame)

        self.out.write(frame)

    def __del__(self):
        self.out.release()


class Visualize:
    height: int = 404 + 1
    width: int = 1280 + 1

    def __init__(self, height=404 + 1, width=720 + 1, fps=30):
        self.height = height
        self.width = width
        self.fps = fps
        self.stream = WriteFrameToVideo((self.height, self.width), fps)
        self.out_matrix = np.zeros((self.height, self.width, 3))

    def draw_grid(self, grid_shape, color=(174, 174, 174), thickness=1):
        rows, cols = grid_shape
        dy, dx = self.height / rows, self.width / cols

        # draw vertical lines
        for x in np.linspace(start=dx, stop=self.width - dx, num=cols - 1):
            x = int(round(x))
            cv2.line(self.out_matrix, (x, 0), (x, self.height), color=color, thickness=thickness)

        # draw horizontal lines
        for y in np.linspace(start=dy, stop=self.height - dy, num=rows - 1):
            y = int(round(y))
            cv2.line(self.out_matrix, (0, y), (self.width, y), color=color, thickness=thickness)

    def set_height_width(self, h: int, w: int):
        self.height = h
        self.width = w

    def visualize(self, board: Board, frame: np.ndarray = None):
        if frame is not None:
            self.out_matrix = frame
        else:
            self.out_matrix = np.zeros((self.height, self.width, 3))

        for x in range(board.x):
            for y in range(board.y):
                if isinstance(board.grid[x, y], Pedestrian):
                    pedestrian = board.grid[x, y]
                    self.addPedestrianToFrame(pedestrian)
                    self.addSpaceToFrame(pedestrian)
                    self.addPath(pedestrian)
        self.stream.write(self.out_matrix)

    def addSpaceToFrame(self, pedestrian: Pedestrian):
        cv2.circle(self.out_matrix, (pedestrian.x, pedestrian.y), PERSONAL_SPACE_RADIUS,
                   tuple([int(c * .6) for c in pedestrian.color]), 2)
        cv2.circle(self.out_matrix, (pedestrian.x, pedestrian.y), PRIVATE_SPACE_RADIUS,
                   tuple([int(c * .4) for c in pedestrian.color]), 2)

    def addPedestrianToFrame(self, pedestrian: Pedestrian):
        cv2.circle(self.out_matrix, (pedestrian.x, pedestrian.y), 10, pedestrian.color, 1)
        cv2.putText(self.out_matrix, "Id: " + str(pedestrian.id), (pedestrian.x, max(pedestrian.y - 30, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    pedestrian.color, 2)

        self.addDestination(pedestrian)

    def addDestination(self, pedestrian: Pedestrian):
        if pedestrian.destination is not None:
            cv2.circle(self.out_matrix, (pedestrian.destination[0], pedestrian.destination[1]), 0,
                       pedestrian.color)

    def addPath(self, pedestrian: Pedestrian):
        if pedestrian.path is None:
            return
        for point in pedestrian.path:
            if 0 < point[0] < self.out_matrix.shape[1] and 0 < point[1] < self.out_matrix.shape[0]:
                self.out_matrix[point[1], point[0]] = pedestrian.color
                cv2.circle(self.out_matrix, (point[0], point[1]), 3, pedestrian.color, -1)
