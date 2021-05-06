import resense

if __name__ == '__main__':
    # Connect to sensor electronics at port COM3
    sensor = resense.HEXSensor('COM10')
    sensor.connect()

    # Record 2 seconds of F/T data. The sample rate specified must be the
    # same as the sample rate configured at the DIP-switches of the
    # electronics interface.
    recording = sensor.record_duration(duration=2.0, sample_rate=1000)

    # Display a force plot
    resense.display_force_plot(recording)

    # Write the recording to a binary file. All exported file types
    # can be imported by FTE. Supported file types are:
    # bin, dat (binary), csv, pkl (pickle), json
    resense.export_recording_to_file(recording, 'C:/Project/recording.bin')
    resense.export_recording_to_file(recording, 'C:/Project/recording.csv')
