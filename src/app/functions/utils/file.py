import ntpath
import os

from app.constants import ATTACHMENT_DIRECTORY
from app.functions import ALLOWED_EXTENSIONS, UPLOAD_DIRECTORY
from app.functions.logging.logger import info


def is_allowed_extension(path):
    return get_file_extension(path) in ALLOWED_EXTENSIONS


def get_file_extension(path):
    return extract_resource_name(path).rsplit('.', 1)[1].lower()


def extract_resource_name(path):
    return ntpath.basename(path)


def save_file(file_name, content, directory=ATTACHMENT_DIRECTORY):
    info('save_file: file_name %s', file_name)
    mode = 0o777
    os.makedirs(UPLOAD_DIRECTORY, mode, True)
    os.makedirs(UPLOAD_DIRECTORY + '/' + directory, mode, True)
    file_path = os.path.join(UPLOAD_DIRECTORY + '/' + directory, file_name)
    with open(file_path, "w") as file:
        file.write(str(content))
    return file_path


def split_path(path):
    all_parts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            all_parts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            all_parts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            all_parts.insert(0, parts[1])
    return all_parts