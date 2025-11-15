"""
Mosaic Rhyme Heuristic

Evaluates the presence of mosaic rhymes (multi-word rhymes).
A mosaic rhyme is when multiple words together rhyme with a single word or phrase.
Example: "gravity" rhymes with "mad but he"
"""

import pronouncing
import re


def get_words(text):
    """Extract words from text, preserving order."""
    return re.findall(r'\b\w+\b', text.lower())


def get_phones_sequence(words):
    """
    Get the phoneme sequence for a list of words.
    Returns the combined phoneme string, or None if any word is not found.
    """
    phone_parts = []
    for word in words:
        phones = pronouncing.phones_for_word(word)
        if not phones:
            return None
        phone_parts.append(phones[0])
    
    return ' '.join(phone_parts)


def phones_rhyme(phones1, phones2):
    """
    Check if two phoneme sequences rhyme.
    They rhyme if they share the same ending from the last stressed vowel.
    """
    if not phones1 or not phones2:
        return False
    
    # Find the rhyming parts (from last stressed vowel onwards)
    def get_rhyme_part(phones):
        phone_list = phones.split()
        # Find the last stressed vowel (ends with 1 or 2)
        for i in range(len(phone_list) - 1, -1, -1):
            if phone_list[i][-1] in '12':
                return ' '.join(phone_list[i:])
        return phones  # If no stress found, use whole thing
    
    rhyme1 = get_rhyme_part(phones1)
    rhyme2 = get_rhyme_part(phones2)
    
    return rhyme1 == rhyme2


def find_mosaic_rhymes(lines):
    """
    Find mosaic rhymes across lines.
    Returns a list of mosaic rhyme matches with their scores.
    """
    mosaic_rhymes = []
    
    for i, line1 in enumerate(lines):
        words1 = get_words(line1)
        
        for j, line2 in enumerate(lines):
            if i == j:
                continue
            
            words2 = get_words(line2)
            
            # Try single words from line1 against multi-word sequences from line2
            for w1_idx, word1 in enumerate(words1):
                phones1 = pronouncing.phones_for_word(word1)
                if not phones1:
                    continue
                phones1 = phones1[0]
                
                # Try different length sequences from line2
                for start in range(len(words2)):
                    for length in range(2, min(4, len(words2) - start + 1)):  # 2-3 word sequences
                        word_seq = words2[start:start + length]
                        phones2 = get_phones_sequence(word_seq)
                        
                        if phones2 and phones_rhyme(phones1, phones2):
                            mosaic_rhymes.append({
                                'word': word1,
                                'sequence': ' '.join(word_seq),
                                'line1': i,
                                'line2': j,
                                'length': length
                            })
            
            # Try multi-word sequences from line1 against single words from line2
            for w2_idx, word2 in enumerate(words2):
                phones2 = pronouncing.phones_for_word(word2)
                if not phones2:
                    continue
                phones2 = phones2[0]
                
                # Try different length sequences from line1
                for start in range(len(words1)):
                    for length in range(2, min(4, len(words1) - start + 1)):
                        word_seq = words1[start:start + length]
                        phones1 = get_phones_sequence(word_seq)
                        
                        if phones1 and phones_rhyme(phones1, phones2):
                            mosaic_rhymes.append({
                                'sequence': ' '.join(word_seq),
                                'word': word2,
                                'line1': i,
                                'line2': j,
                                'length': length
                            })
    
    return mosaic_rhymes


def score_mosaic_rhyme(stanza):
    """
    Score the mosaic rhyme quality of a stanza.
    
    Mosaic rhymes are multi-word rhymes where a sequence of words rhymes
    with a single word or another sequence.
    
    Args:
        stanza (str): The text to evaluate (multi-line string)
    
    Returns:
        float: Score representing mosaic rhyme richness (higher is better)
              Each mosaic rhyme found adds to the score, with longer
              sequences weighted more heavily.
    
    Examples:
        >>> stanza = "oh there goes gravity\\noh he's so mad but he"
        >>> score_mosaic_rhyme(stanza)  # Should detect gravity/mad but he
        
        >>> stanza = "I need to speak clearly\\nI see really"
        >>> score_mosaic_rhyme(stanza)  # Should detect clearly/see really
    """
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    
    if len(lines) < 2:
        return 0.0
    
    mosaic_rhymes = find_mosaic_rhymes(lines)
    
    # Calculate score based on number and quality of mosaic rhymes
    total_score = 0
    seen = set()  # Avoid counting the same rhyme multiple times
    
    for rhyme in mosaic_rhymes:
        # Create a unique key for this rhyme
        word = rhyme.get('word', '')
        sequence = rhyme.get('sequence', '')
        
        # Filter out trivial cases where single syllable words all rhyme
        # Only count if the sequence has 2+ syllables total
        word_phones = pronouncing.phones_for_word(word)
        if word_phones and pronouncing.syllable_count(word_phones[0]) <= 1:
            # Single syllable word - only count if sequence is interesting
            seq_words = sequence.split()
            if len(seq_words) < 2:
                continue  # Skip trivial single-syllable matches
        
        key = (word, sequence, rhyme['line1'], rhyme['line2'])
        
        if key not in seen:
            seen.add(key)
            # Award points for longer sequences only (2+ word sequences are interesting)
            # Scale: 2 words = 10 points, 3 words = 15 points
            total_score += (rhyme['length']) * 5
    
    # Normalize by number of lines to avoid inflated scores
    if len(lines) > 0:
        total_score = total_score / len(lines)
    
    return total_score


def main():
    """CLI interface for mosaic rhyme scoring."""
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
    mosaic_rhymes = find_mosaic_rhymes(lines)
    score = score_mosaic_rhyme(stanza)
    
    print(f"\nMosaic rhyme score: {score:.2f}")
    print(f"Found {len(mosaic_rhymes)} potential mosaic rhyme(s):")
    
    seen = set()
    for rhyme in mosaic_rhymes:
        word = rhyme.get('word', '')
        sequence = rhyme.get('sequence', '')
        key = (word, sequence, rhyme['line1'], rhyme['line2'])
        
        if key not in seen:
            seen.add(key)
            print(f"  '{word}' ~ '{sequence}' (lines {rhyme['line1']+1} and {rhyme['line2']+1})")


if __name__ == '__main__':
    main()
