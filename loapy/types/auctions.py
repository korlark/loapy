from __future__ import annotations  # for postponed evaluation of annotations

from typing import List, Literal, TypedDict

from .basic import DateTimeStr


class AuctionOption(TypedDict):
    MaxItemLevel: int
    ItemGradeQualities: List[int]
    SkillOptions: List[SkillOption]
    EtcOptions: List[EtcOption]
    Categories: List[Category]
    ItemGrades: List[str]
    ItemTiers: List[int]
    Classes: List[str]


class SkillOption(TypedDict):
    Value: int
    Class: str
    Text: str
    IsSkillGroup: bool
    Tripods: List[Tripod]


class Tripod(TypedDict):
    Value: int
    Text: str
    IsGem: bool


class EtcOption(TypedDict):
    Value: int
    Text: str
    EtcSubs: List[EtcSub]


class EtcSub(TypedDict):
    Value: int
    Text: str
    Class: str


class Category(TypedDict):
    Subs: List[CategoryItem]
    Code: int
    CodeName: str


class CategoryItem(TypedDict):
    Code: int
    CodeName: str


class RequestAuctionItems(TypedDict):
    ItemLevelMin: int
    ItemLevelMax: int
    ItemGradeQuality: int
    SkillOptions: List[SearchDetailOption]
    EtcOptions: List[SearchDetailOption]
    Sort: Literal[
        "BIDSTART_PRICE",
        "BUY_PRICE",
        "EXPIREDATE",
        "ITEM_GRADE",
        "ITEM_LEVEL",
        "ITEM_QUALITY",
    ]
    CategoryCode: int
    CharacterClass: str
    ItemTier: int
    ItemGrade: str
    ItemName: str
    PageNo: int
    SortCondition: Literal["ASC", "DESC"]


class SearchDetailOption(TypedDict):
    FirstOption: int
    SecondOption: int
    MinValue: int
    MaxValue: int


class Auction(TypedDict):
    PageNo: int
    PageSize: int
    TotalCount: int
    Items: List[AuctionItem]


class AuctionItem(TypedDict):
    Name: str
    Grade: str
    Tier: int
    Level: int
    Icon: str
    GradeQuality: int
    AuctionInfo: AuctionInfo
    Options: List[ItemOption]


class AuctionInfo(TypedDict):
    StartPrice: int
    BuyPrice: int
    BidPrice: int
    EndDate: DateTimeStr
    BidCount: int
    BidStartPrice: int
    IsCompetitive: bool
    TradeAllowCount: int


class ItemOption(TypedDict):
    Type: Literal[
        "None",
        "SKILL",
        "STAT",
        "ABILITY_ENGRAVE",
        "BRACELET_SPECIAL_EFFECTS",
        "GEM_SKILL_COOLDOWN_REDUCTION",
        "GEM_SKILL_COOLDOWN_REDUCTION_IDENTITY",
        "GEM_SKILL_DAMAGE",
        "GEM_SKILL_DAMAGE_IDENTITY",
        "BRACELET_RANDOM_SLOT",
    ]
    OptionName: str
    OptionNameTripod: str
    Value: int
    IsPenalty: bool
    ClassName: str
