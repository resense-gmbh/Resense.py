_supported_file_types = ['csv', 'json', 'pkl', 'bin', 'dat']


def is_supported_extension(file_extension: str) -> bool:
    if file_extension is None:
        return False
    return file_extension in _supported_file_types


def _validate_name_and_extension(file_path: str, file_extension: str = None) -> str:
    if file_path is None or len(file_path) == 0:
        raise Exception("no file_path provided")

    if file_extension is None:
        i = file_path.rfind('.')
        if i == -1 or i == (len(file_path) - 1):
            raise Exception("file path without extension provided")
        file_extension = file_path[(i + 1):]
    return file_extension
