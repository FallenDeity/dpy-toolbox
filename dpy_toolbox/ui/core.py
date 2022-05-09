from typing import Union
import discord

class ButtonDisplay:
    def __init__(self, emoji: Union[str] = None, label: Union[str] = None, color: Union[discord.ButtonStyle] = None):
        self.emoji = emoji
        self.label = label
        self.style = color

    def has(self, name):
        return True if getattr(self, name, None) else False

    @property
    def _attr_to_list(self):
        return self.emoji, self.label, self.style

    @property
    def _attr_to_list_filtered(self):
        return filter(lambda x: True if x else False, self._attr_to_list)

    @property
    def _attr_name_to_list(self):
        return self._attr_to_list[:-1]

    @property
    def _attr_name_to_list_filtered(self):
        return filter(lambda x: True if x else False, self._attr_name_to_list)

    @property
    def ButtonContent(self):
        return "".join(self._attr_name_to_list_filtered)

    @property
    def to_kwargs(self):
        return dict(filter(lambda val: True if val[1] else False, self.__dict__.items()))

    @property
    def to_args(self):
        return [x if x else None for x in self._attr_name_to_list]
