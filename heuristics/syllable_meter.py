"""
Syllable Meter Heuristic

Evaluates the metrical consistency of a stanza based on syllable counts
and stress patterns. Awards points for consistent meter across lines.
"""

import pronouncing
import re


def get_words(text):
    """Extract words from text."""
    return re.findall(r'\b\w+\b', text.lower())


def count_syllables(line):
    """
    Count the total syllables in a line.
    Returns the syllable count or None if words cannot be analyzed.
    """
    words = get_words(line)
    total = 0
    
    for word in words:
        phones = pronouncing.phones_for_word(word)
        if phones:
            syllables = pronouncing.syllable_count(phones[0])
            total += syllables
        else:
            # Fallback: estimate syllables by counting vowel groups
            total += max(1, len(re.findall(r'[aeiouy]+', word, re.IGNORECASE)))
    
    return total if total > 0 else None


def get_stress_pattern(line):
    """
    Get the stress pattern of a line.
    Returns a string of 0s, 1s, and 2s representing unstressed, primary, and secondary stress.
    """
    words = get_words(line)
    pattern = []
    
    for word in words:
        stresses = pronouncing.stresses_for_word(word)
        if stresses:
            # Use the first pronunciation
            pattern.append(stresses[0])
        else:
            # Unknown stress pattern
            pattern.append('?')
    
    return ''.join(pattern)


def analyze_meter_consistency(syllable_counts):
    """
    Analyze how consistent syllable counts are across lines.
    Returns a score from 0-100.
    """
    if len(syllable_counts) < 2:
        return 100.0 if syllable_counts else 0.0
    
    # Check if all lines have the same syllable count
    unique_counts = set(syllable_counts)
    if len(unique_counts) == 1:
        return 100.0
    
    # Calculate variance
    mean = sum(syllable_counts) / len(syllable_counts)
    variance = sum((x - mean) ** 2 for x in syllable_counts) / len(syllable_counts)
    std_dev = variance ** 0.5
    
    # Score based on standard deviation (lower is better)
    # A std dev of 0 = 100, std dev of 3+ = 0
    score = max(0, 100 - (std_dev * 33.33))
    
    return score


def detect_common_meters(stress_pattern):
    """
    Detect if the stress pattern matches common metrical feet.
    Returns the meter name and a confidence score.
    """
    # Common metrical patterns (simplified)
    meters = {
        'iambic': re.compile(r'(01)+'),  # unstressed-stressed
        'trochaic': re.compile(r'(10)+'),  # stressed-unstressed
        'anapestic': re.compile(r'(001)+'),  # unstressed-unstressed-stressed
        'dactylic': re.compile(r'(100)+'),  # stressed-unstressed-unstressed
    }
    
    # Remove unknown stress markers
    clean_pattern = stress_pattern.replace('?', '')
    
    if not clean_pattern:
        return None, 0.0
    
    best_meter = None
    best_coverage = 0.0
    
    for meter_name, pattern in meters.items():
        matches = pattern.findall(clean_pattern)
        if matches:
            # Calculate how much of the pattern is covered by this meter
            covered = sum(len(m) for m in matches)
            coverage = covered / len(clean_pattern)
            
            if coverage > best_coverage:
                best_coverage = coverage
                best_meter = meter_name
    
    return best_meter, best_coverage * 100


def score_syllable_meter(stanza):
    """
    Score the metrical quality of a stanza based on syllable consistency.
    
    Awards points for:
    - Consistent syllable counts across lines
    - Recognizable metrical patterns (iambic, trochaic, etc.)
    
    Args:
        stanza (str): The text to evaluate (multi-line string)
    
    Returns:
        float: Score from 0-100, where 100 indicates perfect metrical consistency
    
    Examples:
        >>> stanza = "The cat sat on the mat\\nThe dog ran in the fog"
        >>> score_syllable_meter(stanza)  # Should have consistent syllable count
        
        >>> stanza = "Shall I compare thee to a summer's day"
        >>> score_syllable_meter(stanza)  # Iambic pentameter
    """
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    
    if not lines:
        return 0.0
    
    syllable_counts = []
    stress_patterns = []
    
    for line in lines:
        count = count_syllables(line)
        if count is not None:
            syllable_counts.append(count)
        
        pattern = get_stress_pattern(line)
        stress_patterns.append(pattern)
    
    if not syllable_counts:
        return 0.0
    
    # Score based on syllable consistency
    consistency_score = analyze_meter_consistency(syllable_counts)
    
    # Bonus points for recognizable metrical patterns
    meter_bonus = 0
    for pattern in stress_patterns:
        meter, coverage = detect_common_meters(pattern)
        if meter and coverage > 50:
            meter_bonus += coverage / len(stress_patterns)
    
    # Combine scores (consistency is worth 70%, meter recognition is worth 30%)
    total_score = (consistency_score * 0.7) + (meter_bonus * 0.3)
    
    return total_score


def main():
    """CLI interface for syllable meter scoring."""
    import sys
    
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            stanza = f.read()
    else:
        # Read from stdin
        print("Enter stanza (Ctrl+D or Ctrl+Z when done):")
        stanza = sys.stdin.read()
    
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    score = score_syllable_meter(stanza)
    
    print(f"\nSyllable meter score: {score:.2f}/100")
    print(f"\nLine-by-line analysis:")
    
    for i, line in enumerate(lines, 1):
        syllables = count_syllables(line)
        pattern = get_stress_pattern(line)
        meter, coverage = detect_common_meters(pattern)
        
        print(f"  Line {i}: {syllables} syllables")
        print(f"    Stress pattern: {pattern}")
        if meter and coverage > 50:
            print(f"    Detected meter: {meter} ({coverage:.0f}% coverage)")
    
    # Show syllable consistency
    syllable_counts = [count_syllables(line) for line in lines]
    syllable_counts = [c for c in syllable_counts if c is not None]
    
    if syllable_counts:
        consistency = analyze_meter_consistency(syllable_counts)
        print(f"\nSyllable consistency: {consistency:.2f}/100")
        print(f"Syllable counts: {syllable_counts}")


if __name__ == '__main__':
    main()
