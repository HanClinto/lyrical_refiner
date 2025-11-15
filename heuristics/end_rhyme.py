"""
End Rhyme Heuristic

Evaluates how well the ends of lines follow common rhyme schemes.
Supports patterns like ABAB, AABB, ABCB, etc.
"""

import pronouncing
import re


def get_last_word(line):
    """Extract the last meaningful word from a line."""
    # Remove punctuation and get last word
    words = re.findall(r'\b\w+\b', line.lower())
    return words[-1] if words else ""


def get_rhyming_part(word):
    """Get the rhyming part (phonemes) of a word."""
    phones = pronouncing.phones_for_word(word)
    if phones:
        return pronouncing.rhyming_part(phones[0])
    return None


def detect_rhyme_scheme(lines):
    """
    Detect the rhyme scheme of given lines.
    Returns a list of labels (e.g., ['A', 'B', 'A', 'B']).
    """
    if not lines:
        return []
    
    last_words = [get_last_word(line) for line in lines]
    rhyme_parts = [get_rhyming_part(word) for word in last_words]
    
    scheme = []
    label_map = {}
    current_label = ord('A')
    
    for i, rhyme_part in enumerate(rhyme_parts):
        if rhyme_part is None:
            scheme.append('?')  # Unknown
            continue
            
        # Check if this rhyme part matches any previous one
        found = False
        for prev_idx, prev_part in enumerate(rhyme_parts[:i]):
            if prev_part and rhyme_part == prev_part:
                scheme.append(scheme[prev_idx])
                found = True
                break
        
        if not found:
            # Assign a new label
            label = chr(current_label)
            scheme.append(label)
            current_label += 1
    
    return scheme


def score_end_rhyme(stanza, expected_scheme=None):
    """
    Score the end rhyme quality of a stanza.
    
    Args:
        stanza (str): The text to evaluate (multi-line string)
        expected_scheme (list, optional): Expected rhyme scheme like ['A', 'B', 'A', 'B']
                                          If None, scores based on any rhyme presence
    
    Returns:
        float: Score from 0-100, where 100 is perfect adherence to the rhyme scheme
    
    Examples:
        >>> stanza = "The cat sat on the mat\\nThe dog ran in the fog\\n"
        >>> score_end_rhyme(stanza)  # Detects AABB
        100.0
        
        >>> score_end_rhyme(stanza, expected_scheme=['A', 'B', 'A', 'B'])
        0.0  # Doesn't match ABAB
    """
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    
    if len(lines) < 2:
        return 0.0
    
    detected_scheme = detect_rhyme_scheme(lines)
    
    # If no expected scheme, score based on rhyme presence
    if expected_scheme is None:
        # Count how many lines rhyme with at least one other line
        rhyme_counts = {}
        for label in detected_scheme:
            if label != '?':
                rhyme_counts[label] = rhyme_counts.get(label, 0) + 1
        
        # Lines that rhyme with at least one other line
        rhyming_lines = sum(1 for label in detected_scheme 
                           if label != '?' and rhyme_counts.get(label, 0) > 1)
        
        return (rhyming_lines / len(lines)) * 100.0
    
    # If expected scheme is provided, check for exact match
    if len(expected_scheme) != len(detected_scheme):
        return 0.0
    
    matches = sum(1 for d, e in zip(detected_scheme, expected_scheme) 
                  if d != '?' and d == e or (d == '?' and e == '?'))
    
    return (matches / len(expected_scheme)) * 100.0


def main():
    """CLI interface for end rhyme scoring."""
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
    scheme = detect_rhyme_scheme(lines)
    score = score_end_rhyme(stanza)
    
    print(f"\nDetected rhyme scheme: {' '.join(scheme)}")
    print(f"End rhyme score: {score:.2f}/100")
    
    # Test against common schemes
    print("\nScores for common rhyme schemes:")
    for scheme_name, scheme_pattern in [
        ('AABB', ['A', 'A', 'B', 'B']),
        ('ABAB', ['A', 'B', 'A', 'B']),
        ('ABCB', ['A', 'B', 'C', 'B']),
    ]:
        if len(lines) == len(scheme_pattern):
            scheme_score = score_end_rhyme(stanza, expected_scheme=scheme_pattern)
            print(f"  {scheme_name}: {scheme_score:.2f}/100")


if __name__ == '__main__':
    main()
