from typing import Optional, Callable
from .errors import NoEventFunction

DEFAULT_EVENT_TAGS = {
            "pass_bot": False
        }

class EventFunction:
    def __init__(self, func: Optional[Callable] = None, events: Optional[list[str]] = None, tags: Optional[dict] = None):
        self.wait_for_events = events if events else []
        self.func = func
        self.tags = tags if tags else DEFAULT_EVENT_TAGS.copy()

    async def __call__(self, *args, **kwargs):
        if not self.func:
            raise NoEventFunction(f"{self.func} is of type {type(self.func)}")
        return await self.func(*args, **kwargs)

class EventFunctionWrapper:
    def __init__(self, events: Optional[list[str]] = None, **kwargs):
        self.wait_for_events = events if events else []

        self.tags = DEFAULT_EVENT_TAGS.copy()
        for k, v in kwargs.items():
            self.tags[k] = v

    def __call__(self, f):
        return EventFunction(f, self.wait_for_events, self.tags)