from enum import Enum
from typing import List, Callable

from functools import reduce

from collections import namedtuple


class Season(Enum):
    OUTDOORS = "OD"
    INDOORS = "IN"


# TODO: Turn this into a derivable property
class ScoringType(Enum):
    IMPERIAL = "IM"
    METRIC = "ME"
    WORCESTER = "WO"
    HIT_MISS = "HM"

    def __str__(self) -> str:
        return {"IM": "Imperial", "ME": "Metric", "WO": "Worcester", "HM": "Hit-Miss",}[
            self.value
        ]


class DistanceType(Enum):
    METRES = "M"
    YARDS = "Y"


class TargetConfig(Enum):
    SINGLE_FACE = 1
    VERTICAL_3SPOT = 2
    DIAMOND_3SPOT = 3

    def __str__(self) -> str:
        return {1: "Single face", 2: "Vertical 3-spot", 3: "Diamond 3-spot",}[
            self.value
        ]


ScoringRing = namedtuple("ScoringRing", ["label", "value", "ratio"])


RoundValidator = Callable[["RoundClass", "Round"], bool]


def metres_to_yards(val) -> float:
    return val * 1.093613


class TargetFace(object):
    def __init__(
        self, name: str, diameter: float, rings: List[ScoringRing], config: TargetConfig
    ):
        self.name = name
        self.diameter = diameter
        self.rings = rings
        self.config = config

    def __eq__(self, other) -> bool:
        if isinstance(other, TargetFace):
            return (
                self.name == other.name
                and self.diameter == other.diameter
                and self.rings == other.rings
                and self.config == other.config
            )

        return False

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<TargetFace name: {self.name}, diameter: {self.diameter}m, rings: {self.rings}, config: {self.config}>"


class SubRound(object):
    def __init__(
        self,
        num_arrows: str,
        distance: float,
        scoring_type: ScoringType,
        target_face: TargetFace,
        distance_type: DistanceType,
    ):
        self.scoring_type = scoring_type
        self.num_arrows = num_arrows
        self.distance = distance
        self.target_face = target_face
        self.distance_type = distance_type

    def readable_distance(self, decimal_places: int = 2) -> str:
        if self.distance_type is DistanceType.METRES:
            return (
                "{val}m".format(val=round(self.distance, decimal_places))
                .rstrip("0")
                .rstrip(".")
            )
        else:
            return (
                "{val}yd".format(
                    val=round(metres_to_yards(self.distance), decimal_places)
                )
                .rstrip("0")
                .rstrip(".")
            )

    def __str__(self) -> str:
        return f"{self.num_arrows} arrows at {self.readable_distance()} on a {self.target_face} using {self.scoring_type} scoring"

    def __repr__(self) -> str:
        return f"<SubRound num_arrows: {self.num_arrows}, distance: {self.distance}m, scoring_type: {self.scoring_type}, target_face: {repr(self.target_face)}, distance_type: {self.distance_type}>"

    def __eq__(self, other) -> bool:
        if isinstance(other, SubRound):
            return (
                self.target_face == other.target_face
                and self.distance == other.distance
                and self.num_arrows == other.num_arrows
                and self.scoring_type == other.scoring_type
                and self.distance_type == other.distance_type
            )

        return False


class Round(object):
    def __init__(self, name: str, season: Season, subrounds: List[SubRound]):
        self.name = name
        self.season = season
        self.subrounds = subrounds

    def __eq__(self, other) -> bool:
        if isinstance(other, Round):
            return (
                self.subrounds == other.subrounds
                and self.name == other.name
                and self.season == other.season
            )

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<Round name: {self.name}, season: {self.season}, subrounds: {repr(self.subrounds)}>"

    @property
    def num_arrows(self) -> int:
        return reduce(lambda x, y: x + y.num_arrows, self.subrounds, 0)

    @property
    def distances(self) -> List[float]:
        return list(map(lambda x: x.distance, self.subrounds))

    def readable_distances(self, decimal_places: int = 2) -> List[str]:
        return list(map(lambda x: x.readable_distance(decimal_places), self.subrounds))

    def belongs_to(self, round_class: "RoundClass") -> bool:
        return round_class.validate_round(self)


def valid_subround_choices(round_class: "RoundClass", r: "Round") -> bool:
    return reduce(
        lambda x, y: x and y,
        [a in b for (a, b) in zip(r.subrounds, round_class.subrounds)],
        True,
    )


class RoundClass(object):
    def __init__(
        self,
        name: str,
        season: Season,
        subrounds: List[List[SubRound]],
        validators: List[RoundValidator] = [valid_subround_choices],
    ):
        self.name = name
        self.season = season
        self.subrounds = subrounds
        self.validators = validators

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"<RoundClass name: {self.name}, season: {self.season}, subrounds: {repr(self.subrounds)}>"

    def validate_round(self, round: Round):
        return reduce(lambda x, y: x and y(self, round), self.validators, True)
