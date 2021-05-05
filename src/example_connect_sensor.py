import resense
import datetime

if __name__ == '__main__':
    sensor = resense.HEXSensor('COM3')
    sensor.connect()

    recording = sensor.record_duration(duration=2.0, sample_rate=1000)
    resense.display_force_plot(recording)

    # TODO: write exporter
    resense.export_recording_to_file('C:/Project/recording.bin')
