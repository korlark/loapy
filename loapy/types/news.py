from typing import TypedDict

from .basic import DateTimeStr


class Event(TypedDict):
    Title: str
    Thumbnail: str
    Link: str
    StartDate: DateTimeStr
    EndDate: DateTimeStr
    RewardDate: DateTimeStr
