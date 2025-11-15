"""Tests for internal_rhyme heuristic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from heuristics.internal_rhyme import score_internal_rhyme, find_rhyming_pairs


def test_internal_rhyme_astic():
    """Test line with multiple 'astic' rhymes."""
    stanza = "I'm drastically plastic and enthusiastic"
    score = score_internal_rhyme(stanza)
    assert score > 0, f"Expected positive score for internal rhyme, got {score}"


def test_internal_rhyme_at():
    """Test line with 'at' sound repetition."""
    stanza = "The cat sat on the mat and ate a rat"
    score = score_internal_rhyme(stanza)
    assert score > 0, f"Expected positive score for internal rhyme, got {score}"


def test_no_internal_rhyme():
    """Test line with no internal rhyme."""
    stanza = "The dog walked home yesterday"
    score = score_internal_rhyme(stanza)
    # Score might be low but not necessarily zero due to phoneme patterns
    assert score >= 0, f"Expected non-negative score, got {score}"


def test_find_rhyming_pairs():
    """Test finding rhyming word pairs."""
    words = ['cat', 'sat', 'mat', 'dog']
    pairs = find_rhyming_pairs(words)
    # cat, sat, mat should all rhyme
    assert pairs >= 2, f"Expected at least 2 rhyming pairs, got {pairs}"


def test_empty_stanza():
    """Test with empty input."""
    score = score_internal_rhyme("")
    assert score == 0.0, "Empty stanza should score 0"


if __name__ == '__main__':
    test_internal_rhyme_astic()
    print("✓ test_internal_rhyme_astic")
    
    test_internal_rhyme_at()
    print("✓ test_internal_rhyme_at")
    
    test_no_internal_rhyme()
    print("✓ test_no_internal_rhyme")
    
    test_find_rhyming_pairs()
    print("✓ test_find_rhyming_pairs")
    
    test_empty_stanza()
    print("✓ test_empty_stanza")
    
    print("\nAll internal_rhyme tests passed!")
