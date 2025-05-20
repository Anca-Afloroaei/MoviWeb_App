from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """ docstring """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """ docstring """
        pass

