from board import Board
from dijkstra import shortest_path
from pedestrian import Pedestrian
from velocities import Velocities
from visualize import Visualize


class MovementPredictor:
    board: Board
    list_of_pedestrians: list

    def __init__(self):
        self.velocities = Velocities()
        self.visualizer = Visualize()
        self.board = Board([])
        self.list_of_pedestrians = []

    def update_positions(self, positions: dict):
        """Update the positions of the people based on the cellular automata rules."""
        print(positions)
        self.velocities.add(positions)
        self.dict_to_pedestrian_list(positions)
        del self.board
        self.board = Board(self.list_of_pedestrians)

    def predict_movement(self, frame):
        """Predict the future movement of the people based on the updated positions."""
        self.calculate_paths()
        self.visualizer.visualize(self.board, frame)

    def calculate_paths(self):
        for pedestrian in self.list_of_pedestrians:
            if pedestrian.destination is not None:
                try:
                    pedestrian.path = shortest_path(pedestrian.position, pedestrian.destination, self.board.grid)
                except:
                    print("Cannot allocate memory for the array.")
                    pedestrian.path = []

    def dict_to_pedestrian_list(self, positions: dict):
        list_of_pedestrians = []
        for pedestrian_id in positions:
            if pedestrian_id not in [p.id for p in self.list_of_pedestrians]:

                new_pedestrian = Pedestrian(pedestrian_id,
                                            positions[pedestrian_id][0],
                                            positions[pedestrian_id][1],
                                            self.velocities.get_velocity_pedestrian(pedestrian_id))
                list_of_pedestrians.append(new_pedestrian)
            else:
                pedestrian = [p for p in self.list_of_pedestrians if p.id == pedestrian_id][0]
                pedestrian.update_position(positions[pedestrian_id][0], positions[pedestrian_id][1],
                                           self.velocities.get_velocity_pedestrian(pedestrian_id))
                list_of_pedestrians.append(pedestrian)
        self.list_of_pedestrians = list_of_pedestrians
