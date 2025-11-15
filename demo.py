#!/usr/bin/env python3
"""
Demo script to show how the Lyrical Refiner works.
This demonstrates the core features without launching the GUI.
"""

import re
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
            return {'total': 0, 'rhyme_score': 0,
                    'density_score': 0, 'line_count': 0}

        rhyme_score = self._calculate_rhyme_score(lines)
        density_score = self._calculate_density_score(lines)
        line_count = len(lines)

        total = (rhyme_score * 0.6 + density_score * 0.3 +
                 min(line_count / 4, 1.0) * 0.1) * 100

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
                if self.rhyme_detector.do_words_rhyme(
                        end_words[i], end_words[j]):
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


def demo():
    """Run a demonstration of the lyrical refiner features."""
    print("=" * 70)
    print("LYRICAL REFINER - DEMO")
    print("=" * 70)
    print()

    # Example lyrics
    example_lyrics = """Roses are red
Violets are blue
Sugar is sweet
And so are you

The stars at night
Shine oh so bright
Making dreams come true
Under skies of blue"""

    print("Example Lyrics:")
    print("-" * 70)
    print(example_lyrics)
    print("-" * 70)
    print()

    # Initialize detector and scorer
    detector = RhymeDetector()
    scorer = StanzaScorer(detector)

    # Parse stanzas
    stanzas = re.split(r'\n\s*\n', example_lyrics)
    stanzas = [s.strip() for s in stanzas if s.strip()]

    print(f"Found {len(stanzas)} stanza(s)")
    print()

    # Analyze each stanza
    for i, stanza in enumerate(stanzas, 1):
        print(f"{'='*70}")
        print(f"STANZA {i}")
        print(f"{'='*70}")
        print(stanza)
        print()

        # Get end words
        lines = [line.strip() for line in stanza.split('\n') if line.strip()]
        end_words = []
        for line in lines:
            words = re.findall(r'\b\w+\b', line)
            if words:
                end_words.append(words[-1])

        print("End words:", ", ".join(end_words))
        print()

        # Find rhyming pairs
        print("Rhyming pairs detected:")
        rhyme_found = False
        for i in range(len(end_words)):
            for j in range(i + 1, len(end_words)):
                if detector.do_words_rhyme(end_words[i], end_words[j]):
                    print(f"  ✓ '{end_words[i]}' rhymes with '{end_words[j]}'")
                    rhyme_found = True

        if not rhyme_found:
            print("  (No rhyming pairs detected)")
        print()

        # Get scores
        scores = scorer.score_stanza(stanza)
        print("Scores:")
        print(f"  Total Score:    {scores['total']}/100")
        print(f"  Rhyme Score:    {scores['rhyme_score']}/100")
        print(f"  Density Score:  {scores['density_score']}/100")
        print(f"  Line Count:     {scores['line_count']}")
        print()

    print("=" * 70)
    print("FEATURES IN THE GUI APPLICATION:")
    print("=" * 70)
    print("✓ Real-time color highlighting of rhyming words")
    print("✓ 10 different colors for different rhyme groups")
    print("✓ Bold formatting for end-of-line words")
    print("✓ Live scoring updates as you type")
    print("✓ Sidebar showing all stanza scores")
    print("✓ Smart stanza detection via blank lines")
    print()
    print("To run the full GUI application:")
    print("  python3 lyrical_refiner.py")
    print()


if __name__ == '__main__':
    demo()
