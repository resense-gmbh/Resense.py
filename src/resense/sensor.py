from .recording import *
import serial
import time
import struct

_BAUD_RATE = 2000000


class CalibrationMatrix:

    def __init__(self, file_path: str = None):
        self.matrix = np.empty((6, 6))
        if file_path is None:
            for column in range(0, 6):
                self.matrix[column][column] = 1
        else:
            with open(file_path, 'r') as file_input:
                for row in range(0, 6):
                    line = file_input.readline()
                    values = line.split(',')
                    for column in range(0, 6):
                        self.matrix[row][column] = float(values[column])

    def process(self, raw_values):
        dest = np.empty((6,))
        for row in range(0, 6):
            result = 0.0
            for column in range(0, 6):
                result += self.matrix[row][column] * raw_values[column]
            dest[row] = result
        return dest


class HEXSensor:

    def __init__(self, com_port):
        self._serial_interface = None
        self._com_port = com_port
        self.calibration_matrix = CalibrationMatrix()

    def is_connected(self) -> bool:
        if self._serial_interface is None:
            return False
        return self._serial_interface.isOpen()

    def connect(self) -> bool:
        self._serial_interface = serial.Serial(port=self._com_port, baudrate=_BAUD_RATE, timeout=None)
        return self.is_connected()

    def disconnect(self):
        if self.is_connected():
            self._serial_interface.close()

    def record_sample(self):
        if not self.is_connected():
            return None
        serial_line = self._serial_interface.read(28)
        raw_values = [struct.unpack('f', serial_line[i * 4:(i + 1) * 4])[0] for i in range(0, 6)]
        processed_values = self.calibration_matrix.process(raw_values)
        return DataSet(time.time_ns() // 1000,
                       ForceValue(processed_values[0], processed_values[1], processed_values[2]),
                       TorqueValue(processed_values[3], processed_values[4], processed_values[5]))

    def record_duration(self, duration: float, sample_rate: int):
        num_samples = int(sample_rate * duration)
        return self.record_samples(num_samples)

    def record_samples(self, num_samples: int):
        dest_array = np.empty((num_samples,), dtype=DataSet)
        read = 0
        for i in range(0, num_samples):
            sample = self.record_sample()
            if sample is None:
                break
            dest_array[i] = sample
            read += 1
        if read == 0:
            return None
        return BufferedRecording(data_points=dest_array[0:read])
