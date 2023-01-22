from typing import TypedDict

from .basic import DateTimeStr


class GuildRanking(TypedDict):
    Rank: int
    GuildName: str
    GuildMessage: str
    MasterName: str
    Rating: int
    MemberCount: int
    MaxMemberCount: int
    UpdatedDate: DateTimeStr
