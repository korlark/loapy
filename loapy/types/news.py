from typing import Literal, TypedDict

from .basic import DateTimeStr


class Event(TypedDict):
    Title: str
    Thumbnail: str
    Link: str
    StartDate: DateTimeStr
    EndDate: DateTimeStr
    RewardDate: DateTimeStr


NoticeType = Literal["공지", "점검", "상점", "이벤트"]


class Notice(TypedDict):
    Title: str
    Date: DateTimeStr
    Link: str
    Type: NoticeType
