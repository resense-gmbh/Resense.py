from .recording import *
from .io_util import _validate_name_and_extension


def _export_recording_to_csv(file_path):
    pass


def _export_recording_to_json(file_path):
    pass


def _export_recording_to_pkl(file_path):
    pass


def _export_recording_to_bin(file_path):
    pass


def export_recording_to_file(file_path: str, file_extension: str = None):
    file_extension = _validate_name_and_extension(file_path, file_extension)

    if file_extension == 'csv':
        _export_recording_to_csv(file_path)
    elif file_extension == 'json':
        _export_recording_to_json(file_path)
    elif file_extension == 'pkl':
        _export_recording_to_pkl(file_path)
    elif file_extension == 'bin' or file_extension == 'dat':
        _export_recording_to_bin(file_path)
    else:
        raise Exception("extension not supported: ." + file_extension)
