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
    """
    Exports the recording to the specified file path. If file_extension is None, the file type will be detected
    from the file path. If file_extension is specified, it will determine the type of file written. If the
    file type is not supported, an Exception will be raised. Recordings exported from this function can be
    imported by FTE.
    :param file_path: The file to write to
    :param file_extension: The file type. Default is None
    """
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
