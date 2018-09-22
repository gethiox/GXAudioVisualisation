import abc

import bpy


# abstract classes defines methods that is required to be implemented

class VisualizationInterface(metaclass=abc.ABCMeta):
    """
    Keeps all information about objects and properties that belongs to visualization entity
    Separate commot properties like raw visualization data from visuzalization mode
    """

    @abc.abstractmethod
    def clean_up(self):
        """r
        emove all related objects and data
        """
        pass

    @abc.abstractmethod
    def prepare_data(self):
        """
        prepare visualization data, eg. bake sound to f-curve or whatever
        """

    @abc.abstractmethod
    def draw(self, context, panel):
        pass


class ModeInterface(metaclass=abc.ABCMeta):
    """
    Visualization mode which contains all required logic and provides properties to user
    """

    @abc.abstractmethod
    def __init__(self, objects=12):
        self.objects: int = objects

    @abc.abstractmethod
    def clean_up(self):
        """
        remove all related objects and data of
        """
        pass
