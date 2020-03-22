import pytest

from rounds.base import metres_to_yards, TargetFace, TargetConfig, ScoringRing


def test_metres_conversion():
    assert round(metres_to_yards(1), 7) == 1.0936133


def test_targetface_eq():
    ring = [ScoringRing(label="hit", value=1, ratio=1)]
    face_1 = TargetFace("6cm Hit-Miss", 0.06, ring, TargetConfig.DIAMOND_3SPOT)
    face_2 = TargetFace("6cm Hit-Miss", 0.06, ring, TargetConfig.DIAMOND_3SPOT)

    assert face_1 == face_2


def test_targetface_rings_eq():
    rings = [
        ScoringRing(label="10", value=10, ratio=0.1),
        ScoringRing(label="9", value=9, ratio=0.2),
        ScoringRing(label="8", value=8, ratio=0.3),
        ScoringRing(label="7", value=7, ratio=0.4),
        ScoringRing(label="6", value=6, ratio=0.5),
    ]
    face_1 = TargetFace("40cm 5 zone 3 spot", 0.4, rings, TargetConfig.VERTICAL_3SPOT)
    face_2 = TargetFace("40cm 5 zone 3 spot", 0.4, rings, TargetConfig.VERTICAL_3SPOT)

    assert face_1 == face_2


def test_targetface_neq():
    ring = [ScoringRing(label="hit", value=1, ratio=1)]
    face_1 = TargetFace("6cm Hit-Miss", 0.06, ring, TargetConfig.DIAMOND_3SPOT)
    face_2 = TargetFace("6cm Hit-Miss", 0.06, ring, TargetConfig.VERTICAL_3SPOT)

    assert not face_1 == face_2
