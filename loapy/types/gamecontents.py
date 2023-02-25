from __future__ import annotations  # for postponed evaluation of annotations

from typing import List, TypedDict

from .basic import DateTimeStr


class ChallengeAbyssDungeon(TypedDict):
    Name: str
    Description: str
    MinCharacterLevel: int
    MinItemLevel: int
    AreaName: str
    StartTime: str
    EndTime: str
    Image: str
    RewardItems: List[RewardItem]


class RewardItem(TypedDict):
    Name: str
    Icon: str
    Grade: str
    StartTimes: List[DateTimeStr]


class ChallengeGuardianRaid(TypedDict):
    Raids: List[GuardianRaid]
    RewardItems: List[LevelRewardItems]


class GuardianRaid(TypedDict):
    Name: str
    Description: str
    MinCharacterLevel: int
    MinItemLevel: int
    RequiredClearRaid: str
    StartTime: str
    EndTime: str
    Image: str


class LevelRewardItems(TypedDict):
    ExpeditionItemLevel: int
    Items: List[RewardItem]


class ContentsCalendar(TypedDict):
    CategoryName: str
    ContentsName: str
    ContentsIcon: str
    MinItemLevel: int
    StartTimes: List[DateTimeStr]
    Location: str
    RewardItems: List[RewardItem]
