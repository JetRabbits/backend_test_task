import pydoc
from abc import ABC, abstractmethod

from werkzeug.exceptions import BadRequest

from app.classes.handling.storage import StorageBadRequest
from app.constants import SERVER_DATA_PROVIDER
from app.functions.handling.error_codes import STORAGE_0118
from app.functions.utils.file import is_allowed_extension

payment_providers = {
    SERVER_DATA_PROVIDER: 'app.storages.server.server_data_storage.ServerDataStorage'
}


class DataStorage(ABC):
    @abstractmethod
    def upload(self, path: str, data):
        pass

    @abstractmethod
    def download(self, path: str):
        pass


def check_resource_extension(path):
    if not is_allowed_extension(path):
        raise StorageBadRequest('use allowed file extensions: json, png, jpg, jpeg, gif, txt', STORAGE_0118)


class DataStorageFactory(ABC):
    @staticmethod
    def create_storage(arguments: dict) -> DataStorage:
        storage_provider = arguments.get('provider')
        for (provider, provider_clazz) in payment_providers.items():
            if storage_provider == provider:
                provider_clazz = pydoc.locate(provider_clazz)
                return provider_clazz(arguments)

        raise BadRequest('please specify class for provider ' + storage_provider)
