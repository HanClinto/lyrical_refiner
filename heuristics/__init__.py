"""
Poetic evaluation heuristics for analyzing lyrical quality.

This package contains various heuristics for scoring poetic attributes
such as rhyme schemes, meter, alliteration, and other poetic devices.
"""

from .end_rhyme import score_end_rhyme
from .internal_rhyme import score_internal_rhyme
from .mosaic_rhyme import score_mosaic_rhyme
from .syllable_meter import score_syllable_meter
from .alliteration import score_alliteration

__all__ = [
    'score_end_rhyme',
    'score_internal_rhyme',
    'score_mosaic_rhyme',
    'score_syllable_meter',
    'score_alliteration',
]
