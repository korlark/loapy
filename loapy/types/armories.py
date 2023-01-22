from __future__ import annotations  # for postponed evaluation of annotations

from typing import List, TypedDict


class ArmoryProfile(TypedDict):
    CharacterImage: str
    ExpeditionLevel: int
    PvpGradeName: str
    TownLevel: int
    TownName: str
    Title: str
    GuildMemberGrade: str
    GuildName: str
    UsingSkillPoint: int
    TotalSkillPoint: int
    Stats: List[Stat]
    Tendencies: List[Tendency]
    ServerName: str
    CharacterName: str
    CharacterLevel: int
    CharacterClassName: str
    ItemAvgLevel: str
    ItemMaxLevel: str


class Stat(TypedDict):
    Type: str
    Value: str
    Tooltip: List[str]


class Tendency(TypedDict):
    Type: str
    Point: int
    MaxPoint: int


class ArmoryEquipment(TypedDict):
    Type: str
    Name: str
    Icon: str
    Grade: str
    Tooltip: str


class ArmoryAvatar(TypedDict):
    Type: str
    Name: str
    Icon: str
    Grade: str
    IsSet: bool
    IsInner: bool
    Tooltip: str


class ArmorySkill(TypedDict):
    Name: str
    Icon: str
    Level: int
    Type: str
    IsAwakening: bool
    Tripods: List[SkillTripod]
    Rune: SkillRune
    Tooltip: str


class SkillTripod(TypedDict):
    Tier: int
    Slot: int
    Name: str
    Icon: str
    Level: int
    IsSelected: bool
    Tooltip: str


class SkillRune(TypedDict):
    Name: str
    Icon: str
    Grade: str
    Tooltip: str


class ArmoryEngraving(TypedDict):
    Engravings: List[Engraving]
    Effects: List[Effect]


class Engraving(TypedDict):
    Slot: int
    Name: str
    Icon: str
    Tooltip: str


class Effect(TypedDict):
    Name: str
    Description: str


class ArmoryCard(TypedDict):
    Cards: List[Card]
    Effects: List[CardEffect]


class Card(TypedDict):
    Slot: int
    Name: str
    Icon: str
    AwakeCount: int
    AwakeTotal: int
    Grade: str
    Tooltip: str


class CardEffect(TypedDict):
    Index: int
    CardSlots: List[int]
    Items: List[Effect]


class ArmoryGem(TypedDict):
    Gems: List[Gem]
    Effects: List[GemEffect]


class Gem(TypedDict):
    Slot: int
    Name: str
    Icon: str
    Level: int
    Grade: str
    Tooltip: str


class GemEffect(TypedDict):
    GemSlot: int
    Name: str
    Description: str
    Icon: str
    Tooltip: str


class ColosseumInfo(TypedDict):
    Rank: int
    PreRank: int
    Exp: int
    Colosseums: List[Colosseum]


class Colosseum(TypedDict):
    SeasonName: str
    Competitive: AggregationTeamDeathMatchRank
    TeamDeathMatch: Aggregation
    DeathMatch: Aggregation
    TeamElimination: AggregationElimination
    CoOpBattle: Aggregation


class AggregationTeamDeathMatchRank(TypedDict):
    Rank: int
    RankName: str
    RankIcon: str
    RankLastMmr: int
    PlayCount: int
    VictoryCount: int
    LoseCount: int
    TieCount: int
    KillCount: int
    AceCount: int
    DeathCount: int


class Aggregation(TypedDict):
    PlayCount: int
    VictoryCount: int
    LoseCount: int
    TieCount: int
    KillCount: int
    AceCount: int
    DeathCount: int


class AggregationElimination(TypedDict):
    FirstWinCount: int
    SecondWinCount: int
    ThirdWinCount: int
    FirstPlayCount: int
    SecondPlayCount: int
    ThirdPlayCount: int
    AllKillCount: int
    PlayCount: int
    VictoryCount: int
    LoseCount: int
    TieCount: int
    KillCount: int
    AceCount: int
    DeathCount: int


class Collectible(TypedDict):
    Type: str
    Icon: str
    Point: int
    MaxPoint: int
    CollectiblePoints: List[CollectiblePoint]


class CollectiblePoint(TypedDict):
    PointName: str
    Point: int
    MaxPoint: int
