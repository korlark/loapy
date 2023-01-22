from __future__ import annotations  # for postponed evaluation of annotations

from typing import List, Literal, TypedDict


class MarketOption(TypedDict):
    Categories: List[Category]
    ItemGrades: List[str]
    ItemTiers: List[int]
    Classes: List[str]


class Category(TypedDict):
    Subs: List[CategoryItem]
    Code: int
    CodeName: str


class CategoryItem(TypedDict):
    Code: int
    CodeName: str


class MarketItemStats(TypedDict):
    Name: str
    TradeRemainCount: int
    BundleCount: int
    Stats: List[MarketStatsInfo]
    Tooltip: str


class MarketStatsInfo(TypedDict):
    Date: str
    AvgPrice: int
    TradeCount: int


class RequestMarketItems(TypedDict):
    Sort: Literal["GRADE", "YDAY_AVG_PRICE", "RECENT_PRICE", "CURRENT_MIN_PRICE"]
    CategoryCode: int
    CharacterClass: str
    ItemTier: int
    ItemGrade: str
    ItemName: str
    PageNo: int
    SortCondition: Literal["ASC", "DESC"]


class MarketList(TypedDict):
    PageNo: int
    PageSize: int
    TotalCount: int
    Items: List[MarketItem]


class MarketItem(TypedDict):
    Id: int
    Name: str
    Grade: str
    Icon: str
    BundleCount: int
    TradeRemainCount: int
    YDayAvgPrice: int
    RecentPrice: int
    CurrentMinPrice: int
