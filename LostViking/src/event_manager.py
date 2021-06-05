from pygame.locals import USEREVENT


class EM(object):
    """ Event Manager which contains Events """
    _EventCount = 0
    _Events = dict()

    @classmethod
    def get_event(cls, event_name: str) -> int:
        """ Find an event id from a name
        :param event_name: name of event in string
        :return id of the event
        """
        if event_name in cls._Events:
            return cls._Events[event_name]
        else:
            raise ValueError("Error: [event_name] doesn't exist!")

    @classmethod
    def add_event(cls, event_name: str) -> int:
        """ Create an event id from a name
        :param event_name: name of event in string
        :return id of the event, used in event detection
        """
        if event_name not in cls._Events:
            event_id = USEREVENT + cls._EventCount
            cls._Events[event_name] = event_id
            cls._EventCount += 1
            return event_id
        else:
            raise ValueError("Error: [event_name] already exist!")

    @classmethod
    def del_event(cls, event_name: str) -> None:
        """ Delete an event from a name, id decrease
        :param event_name: name of event in string
        """
        if event_name in cls._Events:
            cls._Events.pop(event_name)
            cls._EventCount -= 1
        else:
            raise ValueError("Error: [event_name] doesn't exist!")
