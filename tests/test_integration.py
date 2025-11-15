"""Integration tests for all heuristics working together."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from heuristics import (
    score_end_rhyme,
    score_internal_rhyme,
    score_mosaic_rhyme,
    score_syllable_meter,
    score_alliteration,
)


def test_all_heuristics_run():
    """Test that all heuristics can run without errors."""
    stanza = """The cat sat on the mat
The rat wore a fancy hat
The dog ran through the fog
The hog jumped like a frog"""
    
    # All heuristics should run without error
    end_score = score_end_rhyme(stanza)
    internal_score = score_internal_rhyme(stanza)
    mosaic_score = score_mosaic_rhyme(stanza)
    meter_score = score_syllable_meter(stanza)
    alliteration_score = score_alliteration(stanza)
    
    print(f"End Rhyme: {end_score:.2f}")
    print(f"Internal Rhyme: {internal_score:.2f}")
    print(f"Mosaic Rhyme: {mosaic_score:.2f}")
    print(f"Syllable Meter: {meter_score:.2f}")
    print(f"Alliteration: {alliteration_score:.2f}")
    
    # Basic sanity checks
    assert end_score >= 0, "End rhyme score should be non-negative"
    assert internal_score >= 0, "Internal rhyme score should be non-negative"
    assert mosaic_score >= 0, "Mosaic rhyme score should be non-negative"
    assert meter_score >= 0, "Meter score should be non-negative"
    assert alliteration_score >= 0, "Alliteration score should be non-negative"
    
    # This specific example has perfect AABB rhyme
    assert end_score >= 90, f"Expected high end rhyme score, got {end_score}"


def test_peter_piper():
    """Test famous alliteration example."""
    stanza = "Peter Piper picked a peck of pickled peppers"
    
    alliteration_score = score_alliteration(stanza)
    print(f"\nPeter Piper Alliteration: {alliteration_score:.2f}")
    
    # Should have high alliteration
    assert alliteration_score > 50, f"Expected high alliteration, got {alliteration_score}"


def test_internal_rhyme_example():
    """Test strong internal rhyme example."""
    stanza = "I'm drastically plastic and enthusiastic"
    
    internal_score = score_internal_rhyme(stanza)
    print(f"\nInternal Rhyme (astic): {internal_score:.2f}")
    
    # Should detect the internal rhyme
    assert internal_score > 50, f"Expected high internal rhyme, got {internal_score}"


def test_empty_input_all_heuristics():
    """Test all heuristics handle empty input gracefully."""
    empty = ""
    
    # None should crash on empty input
    score_end_rhyme(empty)
    score_internal_rhyme(empty)
    score_mosaic_rhyme(empty)
    score_syllable_meter(empty)
    score_alliteration(empty)
    
    print("\n✓ All heuristics handle empty input gracefully")


if __name__ == '__main__':
    test_all_heuristics_run()
    print("✓ test_all_heuristics_run")
    
    test_peter_piper()
    print("✓ test_peter_piper")
    
    test_internal_rhyme_example()
    print("✓ test_internal_rhyme_example")
    
    test_empty_input_all_heuristics()
    print("✓ test_empty_input_all_heuristics")
    
    print("\n" + "="*60)
    print("All integration tests passed!")
    print("="*60)
