from enum import Enum
from typing import List, Callable

from functools import reduce

from collections import namedtuple

# RoundValidator defines a standard way to check for Round/RoundClass identity
RoundValidator = Callable[["RoundClass", "Round"], bool]


class Season(Enum):
    """The archery shooting season(s)."""

    OUTDOORS = "OD"
    INDOORS = "IN"


# TODO: Turn this into a derivable property
class ScoringType(Enum):
    """The different round scoring types in archery.
    
    ``ScoringType`` is a tag with the purpose of making it easier for a user
    to understand the kind of scoring used for a round. For example, a
    Worcester round is an imperial round but scores with values 5-1 instead
    of 9-1 (with decrements of 2).

    """

    IMPERIAL = "IM"  #: Imperial scoring (9, 7, 5, 3, 1)
    METRIC = "ME"  #: Metric scoring (10-1 with or without Xs)
    WORCESTER = "WO"  #: Worcester scoring (Imperial scoring with 5-1 values)
    HIT_MISS = "HM"  #: Hit or miss scoring (1 or 0)

    def __str__(self) -> str:
        return {"IM": "Imperial", "ME": "Metric", "WO": "Worcester", "HM": "Hit-Miss",}[
            self.value
        ]


class DistanceType(Enum):
    """An Enum class to help mark whether a ``SubRound`` is shot in metres or yards."""

    METRES = "M"
    YARDS = "Y"


class TargetConfig(Enum):
    """The different kinds of target face configurations that can be found.
    
    ``TargetConfig`` mostly makes a difference when calculating the handicap
    for indoor rounds (e.g.: WA 18m) where there are different handicap values
    when shooting on either a vertical 3-spot or a single spot face.
    
    """

    SINGLE_FACE = 1  #: A single spot or target face
    VERTICAL_3SPOT = 2  #: A vertical arrangement of 3 target faces
    DIAMOND_3SPOT = 3  #: A diamond arrangement of 3 target faces

    def __str__(self) -> str:
        return {1: "Single spot", 2: "Vertical 3-spot", 3: "Diamond 3-spot",}[
            self.value
        ]


# TODO: Turn this into a concrete class
ScoringRing = namedtuple("ScoringRing", ["label", "value", "ratio"])


def metres_to_yards(distance: float) -> float:
    """A standard function to convert between the metres and yards.

    Parameters
    ----------
    distance : float
        The distance in metres to convert to yards

    Returns
    -------
    float
        The distance converted from metres to yards, precise to 7 decimal places.

    """
    return distance * 1.0936133


class TargetFace(object):
    """
    Represent the target face shot at for (part of) an archery round.

    This class allows for you to encode the key aspects of a target face
    (e.g.: diameter, number of scoring rings) that can be leveraged for
    calculating handicaps for the round. 

    Parameters
    ----------
    name : str
        The name of this target face, e.g.: "40cm 10 zone".
    diameter : float
        The diameter of the largest scoring zone on the face. Note that for 
        target faces that use inner scoring zones (e.g.: 40cm 5-zone 3 spot) 
        you should still give the diameter of the face as if it wasn't an 
        inner target face (40cm).
    rings : :obj:`list` of :obj:`ScoringRing`
        The scoring rings that are used by this target face, ordered from 
        highest to lowest value scored.
    config : :obj:`TargetConfig`
        The target face arrangement as printed on the paper.
    
    """

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
    """ """

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
        """

        :param decimal_places: int:  (Default value = 2)

        """
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
    """ """

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
        """ """
        return reduce(lambda x, y: x + y.num_arrows, self.subrounds, 0)

    @property
    def distances(self) -> List[float]:
        """ """
        return list(map(lambda x: x.distance, self.subrounds))

    def readable_distances(self, decimal_places: int = 2) -> List[str]:
        """

        :param decimal_places: int:  (Default value = 2)

        """
        return list(map(lambda x: x.readable_distance(decimal_places), self.subrounds))

    def belongs_to(self, round_class: "RoundClass") -> bool:
        """

        :param round_class: "RoundClass": 

        """
        return round_class.validate_round(self)


def valid_subround_choices(round_class: "RoundClass", r: "Round") -> bool:
    """

    :param round_class: "RoundClass": 
    :param r: "Round": 

    """
    return reduce(
        lambda x, y: x and y,
        [a in b for (a, b) in zip(r.subrounds, round_class.subrounds)],
        True,
    )


class RoundClass(object):
    """ """

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
        """

        :param round: Round: 

        """
        return reduce(lambda x, y: x and y(self, round), self.validators, True)
