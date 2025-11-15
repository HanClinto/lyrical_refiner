#!/usr/bin/env python3
"""
Basic tests for core functionality of Lyrical Refiner.
"""

import sys
import re

# Import the core classes (without GUI)
import pronouncing


class RhymeDetector:
    """Handles rhyme detection using phonetic analysis."""
    
    def __init__(self):
        self.word_cache = {}
    
    def get_rhymes(self, word: str):
        """Get all words that rhyme with the given word."""
        word_clean = word.lower().strip('.,!?;:"\'-')
        if not word_clean:
            return set()
            
        if word_clean in self.word_cache:
            return self.word_cache[word_clean]
        
        rhymes = set(pronouncing.rhymes(word_clean))
        self.word_cache[word_clean] = rhymes
        return rhymes
    
    def do_words_rhyme(self, word1: str, word2: str) -> bool:
        """Check if two words rhyme."""
        word1_clean = word1.lower().strip('.,!?;:"\'-')
        word2_clean = word2.lower().strip('.,!?;:"\'-')
        
        if not word1_clean or not word2_clean or word1_clean == word2_clean:
            return False
        
        rhymes = self.get_rhymes(word1_clean)
        return word2_clean in rhymes


class StanzaScorer:
    """Scores stanzas based on various heuristics."""
    
    def __init__(self, rhyme_detector):
        self.rhyme_detector = rhyme_detector
    
    def score_stanza(self, stanza: str):
        """Score a stanza based on multiple heuristics."""
        lines = [line.strip() for line in stanza.split('\n') if line.strip()]
        
        if not lines:
            return {'total': 0, 'rhyme_score': 0, 'density_score': 0, 'line_count': 0}
        
        rhyme_score = self._calculate_rhyme_score(lines)
        density_score = self._calculate_density_score(lines)
        line_count = len(lines)
        
        total = (rhyme_score * 0.6 + density_score * 0.3 + min(line_count / 4, 1.0) * 0.1) * 100
        
        return {
            'total': round(total, 1),
            'rhyme_score': round(rhyme_score * 100, 1),
            'density_score': round(density_score * 100, 1),
            'line_count': line_count
        }
    
    def _calculate_rhyme_score(self, lines):
        """Calculate rhyme score based on end-word rhymes."""
        if len(lines) < 2:
            return 0.0
        
        end_words = []
        for line in lines:
            words = re.findall(r'\b\w+\b', line)
            if words:
                end_words.append(words[-1])
        
        if len(end_words) < 2:
            return 0.0
        
        rhyme_pairs = 0
        total_pairs = 0
        
        for i in range(len(end_words)):
            for j in range(i + 1, len(end_words)):
                total_pairs += 1
                if self.rhyme_detector.do_words_rhyme(end_words[i], end_words[j]):
                    rhyme_pairs += 1
        
        return rhyme_pairs / total_pairs if total_pairs > 0 else 0.0
    
    def _calculate_density_score(self, lines):
        """Calculate score based on word density."""
        word_counts = []
        for line in lines:
            words = re.findall(r'\b\w+\b', line)
            word_counts.append(len(words))
        
        if not word_counts:
            return 0.0
        
        avg_words = sum(word_counts) / len(word_counts)
        if 5 <= avg_words <= 10:
            return 1.0
        elif avg_words < 5:
            return avg_words / 5.0
        else:
            return max(0.0, 1.0 - (avg_words - 10) / 10)


def test_rhyme_detection():
    """Test rhyme detection."""
    print("Testing rhyme detection...")
    detector = RhymeDetector()
    
    # Test basic rhymes
    assert detector.do_words_rhyme("cat", "hat"), "cat and hat should rhyme"
    assert detector.do_words_rhyme("day", "say"), "day and say should rhyme"
    assert not detector.do_words_rhyme("cat", "dog"), "cat and dog should not rhyme"
    assert not detector.do_words_rhyme("cat", "cat"), "same word should not rhyme with itself"
    
    print("✓ Rhyme detection tests passed")


def test_stanza_parsing():
    """Test stanza parsing."""
    print("Testing stanza parsing...")
    
    text = """Roses are red
Violets are blue

Sugar is sweet
And so are you"""
    
    stanzas = re.split(r'\n\s*\n', text)
    stanzas = [s.strip() for s in stanzas if s.strip()]
    
    assert len(stanzas) == 2, f"Expected 2 stanzas, got {len(stanzas)}"
    assert "Roses are red" in stanzas[0], "First stanza should contain 'Roses are red'"
    assert "Sugar is sweet" in stanzas[1], "Second stanza should contain 'Sugar is sweet'"
    
    print("✓ Stanza parsing tests passed")


def test_stanza_scoring():
    """Test stanza scoring."""
    print("Testing stanza scoring...")
    
    detector = RhymeDetector()
    scorer = StanzaScorer(detector)
    
    # Test with a rhyming stanza
    stanza1 = """Roses are red
Violets are blue
Sugar is sweet
And so are you"""
    
    scores = scorer.score_stanza(stanza1)
    assert scores['line_count'] == 4, f"Expected 4 lines, got {scores['line_count']}"
    assert scores['total'] > 0, "Total score should be greater than 0"
    
    print(f"  Stanza 1 scores: {scores}")
    
    # Test with empty stanza
    scores_empty = scorer.score_stanza("")
    assert scores_empty['total'] == 0, "Empty stanza should have 0 score"
    
    print("✓ Stanza scoring tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Lyrical Refiner Core Tests")
    print("=" * 50)
    
    try:
        test_rhyme_detection()
        test_stanza_parsing()
        test_stanza_scoring()
        
        print("=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
