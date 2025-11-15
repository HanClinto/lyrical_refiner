"""
Alliteration Heuristic

Evaluates the presence of alliteration (repeated initial consonant sounds).
Awards points for sequences of words that start with the same sound.
"""

import pronouncing
import re


def get_words(text):
    """Extract words from text, preserving order."""
    return re.findall(r'\b\w+\b', text.lower())


def get_initial_sound(word):
    """
    Get the initial consonant sound(s) of a word.
    Returns the phoneme(s) before the first vowel.
    """
    phones = pronouncing.phones_for_word(word)
    if not phones:
        # Fallback to first letter
        return word[0] if word else None
    
    phone_list = phones[0].split()
    
    # Collect consonants before first vowel
    initial = []
    for phone in phone_list:
        # Vowels have stress markers (0, 1, 2)
        if phone[-1] in '012':
            break
        initial.append(phone)
    
    # If no consonants found, word starts with vowel
    if not initial and phone_list:
        return phone_list[0]
    
    return ' '.join(initial) if initial else None


def find_alliteration_sequences(words, min_length=2):
    """
    Find sequences of consecutive words with the same initial sound.
    Returns a list of (sound, start_index, length) tuples.
    """
    if len(words) < min_length:
        return []
    
    sequences = []
    i = 0
    
    while i < len(words):
        initial = get_initial_sound(words[i])
        if initial is None:
            i += 1
            continue
        
        # Count consecutive words with same initial sound
        length = 1
        j = i + 1
        while j < len(words):
            next_initial = get_initial_sound(words[j])
            if next_initial == initial:
                length += 1
                j += 1
            else:
                break
        
        if length >= min_length:
            sequences.append((initial, i, length))
            i = j
        else:
            i += 1
    
    return sequences


def find_non_consecutive_alliteration(words, max_gap=2):
    """
    Find alliteration that isn't strictly consecutive but close together.
    Returns count of alliterative pairs within max_gap words.
    """
    alliteration_count = 0
    
    for i in range(len(words)):
        initial_i = get_initial_sound(words[i])
        if initial_i is None:
            continue
        
        # Look ahead within the gap
        for j in range(i + 1, min(i + max_gap + 1, len(words))):
            initial_j = get_initial_sound(words[j])
            if initial_j and initial_i == initial_j:
                alliteration_count += 1
    
    return alliteration_count


def score_alliteration(stanza):
    """
    Score the alliteration quality of a stanza.
    
    Awards points for:
    - Consecutive words starting with the same sound
    - Multiple alliterative sequences
    - Longer alliterative sequences (weighted more)
    
    Args:
        stanza (str): The text to evaluate (multi-line string)
    
    Returns:
        float: Score representing alliteration richness (higher is better)
              Score is roughly proportional to the amount of alliteration present.
    
    Examples:
        >>> stanza = "Peter Piper picked a peck of pickled peppers"
        >>> score_alliteration(stanza)  # High score due to 'p' alliteration
        
        >>> stanza = "She sells seashells by the seashore"
        >>> score_alliteration(stanza)  # High score due to 's' alliteration
    """
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    
    total_score = 0
    total_words = 0
    
    for line in lines:
        words = get_words(line)
        if len(words) < 2:
            continue
        
        total_words += len(words)
        
        # Find consecutive alliteration sequences
        sequences = find_alliteration_sequences(words, min_length=2)
        
        for sound, start, length in sequences:
            # Award more points for longer sequences
            # 2 words = 10 points, 3 words = 20, 4 words = 30, etc.
            total_score += (length - 1) * 10
        
        # Find non-consecutive alliteration (bonus points)
        non_consecutive = find_non_consecutive_alliteration(words, max_gap=2)
        total_score += non_consecutive * 5
    
    # Normalize by number of words
    if total_words > 0:
        normalized_score = (total_score / total_words) * 10
    else:
        normalized_score = 0.0
    
    return normalized_score


def main():
    """CLI interface for alliteration scoring."""
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
    score = score_alliteration(stanza)
    
    print(f"\nAlliteration score: {score:.2f}")
    print(f"\nLine-by-line analysis:")
    
    for i, line in enumerate(lines, 1):
        words = get_words(line)
        sequences = find_alliteration_sequences(words, min_length=2)
        
        if sequences:
            print(f"  Line {i}: {len(sequences)} alliterative sequence(s)")
            for sound, start, length in sequences:
                alliterative_words = words[start:start + length]
                print(f"    '{sound}': {' '.join(alliterative_words)}")
        else:
            print(f"  Line {i}: No strong alliteration detected")


if __name__ == '__main__':
    main()
