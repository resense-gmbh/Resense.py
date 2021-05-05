import numpy as np
from enum import Enum
import pickle
import os
from pathlib import Path
from math import sqrt


class ForceValue:

    def __init__(self, x, y, z, parse: bool = False, decimal_separator: str = '.'):
        if parse:
            self.x = float(x.replace(decimal_separator, '.'))
            self.y = float(y.replace(decimal_separator, '.'))
            self.z = float(z.replace(decimal_separator, '.'))
        else:
            self.x = x
            self.y = y
            self.z = z

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return sqrt(self.length_squared())


class TorqueValue:

    def __init__(self, x, y, z, parse: bool = False, decimal_separator: str = '.'):
        if parse:
            self.x = float(x.replace(decimal_separator, '.'))
            self.y = float(y.replace(decimal_separator, '.'))
            self.z = float(z.replace(decimal_separator, '.'))
        else:
            self.x = x
            self.y = y
            self.z = z

    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self) -> float:
        return sqrt(self.length_squared())


class Variable(Enum):
    FORCE = 1
    TORQUE = 2


class Direction(Enum):
    X = 1
    Y = 2
    Z = 3


class DataSet:

    def __init__(self, time_offset: int = 0, force: ForceValue = None, torque: TorqueValue = None):
        self.time_offset = time_offset
        self.force = force
        self.torque = torque

    def get_time_stamp(self, seconds: bool = True) -> float:
        # timestamp is in microseconds
        return self.time_offset / 1000000.0 if seconds else self.time_offset

    def get_time_offset(self, first_time_offset: int, seconds: bool = True) -> float:
        # delta is in microseconds
        delta = self.time_offset - first_time_offset
        return delta / 1000000.0 if seconds else delta


class BufferedRecording:

    def __init__(self, data_points: np.ndarray = None, file: str = None):
        if data_points is None and file is None:
            raise Exception('specify either data_points or input_file')
        if data_points is not None:
            self.data_points = data_points
            self.name = ""
        else:
            with open(file, 'rb') as fin:
                obj = pickle.load(fin)
            self.data_points = obj.data_points
            self.name = os.path.basename(file)

        if len(self.data_points) == 0:
            raise Exception("no data points given")

        self.first_time_offset = self.data_points[0].time_offset
        self.length = len(self.data_points)

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def get_time_duration(self, seconds: bool = True) -> float:
        last_index = len(self.data_points) - 1
        duration_micro_seconds = self.data_points[last_index].time_offset - self.first_time_offset
        return duration_micro_seconds / 1000000.0 if seconds else duration_micro_seconds

    def get_average_frequency(self) -> float:
        average_distance = self.get_time_duration() / self.get_data_point_count()
        return 1.0 / average_distance

    def get_data_point_count(self) -> int:
        return self.length

    def get_data_point(self, index: int):
        if index < 0 or index >= self.length:
            return None
        return self.data_points[index]

    def get_data_point_offset_seconds(self, data_point: DataSet, seconds: bool = True):
        return data_point.get_time_offset(self.first_time_offset, seconds)

    def get_array_of_timestamps(self, relative: bool = True, seconds: bool = True):
        return np.array([
            (self.get_data_point_offset_seconds(point, seconds) if relative else point.get_time_stamp(seconds))
            for point in self.data_points])

    def get_array_of_values(self, variable: Variable, direction: Direction) -> np.ndarray:
        if variable is Variable.FORCE:
            if direction is Direction.X:
                return np.array([point.force.x for point in self.data_points])
            elif direction is Direction.Y:
                return np.array([point.force.y for point in self.data_points])
            elif direction is Direction.Z:
                return np.array([point.force.z for point in self.data_points])
        elif variable is Variable.TORQUE:
            if direction is Direction.X:
                return np.array([point.torque.x for point in self.data_points])
            elif direction is Direction.Y:
                return np.array([point.torque.y for point in self.data_points])
            elif direction is Direction.Z:
                return np.array([point.torque.z for point in self.data_points])

    def get_array_of_vectors(self, variable: Variable) -> np.ndarray:
        if variable is Variable.FORCE:
            return np.array([[point.torque.data_point, point.torque.y, point.torque.z] for point in self.data_points])
        elif variable is Variable.FORCE:
            return np.array([[point.force.data_point, point.force.y, point.force.z] for point in self.data_points])

    def get_data_points(self, start, end) -> np.ndarray:
        return np.array(self.data_points[start:end])

    def save(self, file: str):
        with open(file, 'wb') as file_output:
            pickle.dump(self, file_output)


class BufferedRecordingSet:

    def __init__(self, recordings: list = None):
        self.recordings = [] if recordings is None else recordings

    def add_recording(self, recording: BufferedRecording):
        self.recordings.append(recording)

    def set_recording_names(self, name: str):
        index = 0
        for recording in self.recordings:
            recording.set_name(name + "-" + str(index))
            index += 1

    def add_recordings(self, other):
        for recording in other.recordings:
            self.recordings.append(recording)

    def get_recordings(self) -> list:
        return self.recordings

    def get_recording_count(self) -> int:
        return len(self.recordings)

    def get_recording(self, index) -> BufferedRecording:
        return self.recordings[index]

    def save(self, folder: str):
        unnamed_index = 0
        Path(folder).mkdir(parents=True, exist_ok=True)
        for recording in self.recordings:
            recording_name = recording.get_name()
            if len(recording_name) == 0:
                recording_name = "unnamed-" + str(unnamed_index)
                unnamed_index += 1
            file_path = os.path.join(folder, recording_name + '.bin')
            recording.save(file_path)

    def load(self, folder: str):
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            recording = BufferedRecording(file=file_path)
            self.add_recording(recording)


def concatenate_recordings(first: BufferedRecording, seconds: BufferedRecording) -> BufferedRecording:
    data_points = first.data_points + seconds.data_points
    return BufferedRecording(data_points=data_points)
