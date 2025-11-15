"""Tests for end_rhyme heuristic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from heuristics.end_rhyme import score_end_rhyme, detect_rhyme_scheme


def test_perfect_aabb():
    """Test perfect AABB rhyme scheme."""
    stanza = """The cat sat on the mat
The rat wore a fancy hat
The dog ran through the fog
The frog jumped on a log"""
    
    score = score_end_rhyme(stanza, expected_scheme=['A', 'A', 'B', 'B'])
    assert score > 70, f"Expected high score for AABB, got {score}"


def test_perfect_abab():
    """Test perfect ABAB rhyme scheme."""
    stanza = """The cat wore a hat
The dog ran in the fog
The rat was very fat
The frog sat on a log"""
    
    score = score_end_rhyme(stanza, expected_scheme=['A', 'B', 'A', 'B'])
    assert score > 70, f"Expected high score for ABAB, got {score}"


def test_no_rhyme():
    """Test stanza with no rhymes."""
    stanza = """The cat ran
The dog walked
The bird flew
The fish swam"""
    
    score = score_end_rhyme(stanza)
    assert score < 50, f"Expected low score for non-rhyming text, got {score}"


def test_detect_aabb_scheme():
    """Test rhyme scheme detection for AABB."""
    lines = [
        "The cat sat on the mat",
        "The rat wore a hat",
        "The dog ran through the fog",
        "The hog jumped like a frog"
    ]
    
    scheme = detect_rhyme_scheme(lines)
    # Should detect AABB pattern
    assert scheme[0] == scheme[1], f"First two lines should rhyme, got {scheme}"
    assert scheme[2] == scheme[3], f"Last two lines should rhyme, got {scheme}"
    assert scheme[0] != scheme[2], f"First and third lines should not rhyme, got {scheme}"


def test_empty_stanza():
    """Test with empty input."""
    score = score_end_rhyme("")
    assert score == 0.0, "Empty stanza should score 0"


def test_single_line():
    """Test with single line."""
    score = score_end_rhyme("The cat sat on the mat")
    assert score == 0.0, "Single line should score 0"


if __name__ == '__main__':
    test_perfect_aabb()
    print("✓ test_perfect_aabb")
    
    test_perfect_abab()
    print("✓ test_perfect_abab")
    
    test_no_rhyme()
    print("✓ test_no_rhyme")
    
    test_detect_aabb_scheme()
    print("✓ test_detect_aabb_scheme")
    
    test_empty_stanza()
    print("✓ test_empty_stanza")
    
    test_single_line()
    print("✓ test_single_line")
    
    print("\nAll end_rhyme tests passed!")
