import os

from flask import send_file

from app.classes.handling.storage import StorageBadRequest
from app.functions import UPLOAD_ABS_DIRECTORY, REST_GUIDE
from app.functions.handling.error_codes import STORAGE_0119
from app.functions.io.response import success
from app.functions.logging.logger import info
from app.functions.utils.file import split_path, extract_resource_name
from app.storages import DataStorage
from app.storages.data_storage import check_resource_extension

DEFAULT_FILE_PERMISSIONS = 0o777


class ServerDataStorage(DataStorage):
    init_arguments = None

    def __init__(self, init_arguments: dict):
        self.init_arguments = init_arguments

    @staticmethod
    def create_directories(path: str):
        info('server.create_directories: path %s', path)
        path_parts = split_path(path)
        resource_name = extract_resource_name(path)
        info('server.create_directories: resource_name %s', resource_name)
        os.makedirs(UPLOAD_ABS_DIRECTORY, DEFAULT_FILE_PERMISSIONS, True)
        directory_path = ''
        for path_part in path_parts:
            if resource_name not in path_part and '/' not in path_part:
                directory_path += '/' + path_part
                absolute_path = UPLOAD_ABS_DIRECTORY + directory_path
                os.makedirs(absolute_path, DEFAULT_FILE_PERMISSIONS, True)
        return directory_path

    def upload(self, path: str, data):
        check_resource_extension(path)
        info('server.upload: path %s', path)
        self.create_directories(path)
        data.save(UPLOAD_ABS_DIRECTORY + path)
        return success(path, 200, 'Success', REST_GUIDE + 'resources')

    def download(self, path: str):
        check_resource_extension(path)
        path = UPLOAD_ABS_DIRECTORY + path
        info('server.download: path %s', path)
        if not os.path.isfile(path):
            raise StorageBadRequest('resource does not exist for path ' + path, STORAGE_0119)
        attachment_file_name = extract_resource_name(path)
        return send_file(path, None, True, attachment_file_name)