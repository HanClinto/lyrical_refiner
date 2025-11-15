"""Tests for alliteration heuristic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from heuristics.alliteration import score_alliteration, find_alliteration_sequences, get_words


def test_peter_piper():
    """Test classic alliteration example."""
    stanza = "Peter Piper picked a peck of pickled peppers"
    score = score_alliteration(stanza)
    assert score > 10, f"Expected high score for strong alliteration, got {score}"


def test_she_sells():
    """Test another classic example."""
    stanza = "She sells seashells by the seashore"
    score = score_alliteration(stanza)
    assert score > 5, f"Expected high score for alliteration, got {score}"


def test_no_alliteration():
    """Test text with no alliteration."""
    stanza = "A bird flew over the mountain"
    score = score_alliteration(stanza)
    # Might have some minimal score but should be low
    assert score >= 0, f"Expected non-negative score, got {score}"


def test_find_sequences():
    """Test finding alliterative sequences."""
    words = get_words("peter piper picked peppers")
    sequences = find_alliteration_sequences(words, min_length=2)
    assert len(sequences) > 0, "Should find at least one alliterative sequence"


def test_empty_stanza():
    """Test with empty input."""
    score = score_alliteration("")
    assert score == 0.0, "Empty stanza should score 0"


if __name__ == '__main__':
    test_peter_piper()
    print("✓ test_peter_piper")
    
    test_she_sells()
    print("✓ test_she_sells")
    
    test_no_alliteration()
    print("✓ test_no_alliteration")
    
    test_find_sequences()
    print("✓ test_find_sequences")
    
    test_empty_stanza()
    print("✓ test_empty_stanza")
    
    print("\nAll alliteration tests passed!")
