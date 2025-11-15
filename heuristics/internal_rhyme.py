"""
Internal Rhyme Heuristic

Evaluates the presence of rhyming words within lines (not just at the ends).
Awards points for repeated phoneme clusters within a line or across lines.
"""

import pronouncing
import re


def get_words(text):
    """Extract words from text."""
    return re.findall(r'\b\w+\b', text.lower())


def get_phoneme_clusters(word, min_length=2):
    """
    Extract phoneme clusters from a word.
    Returns a list of phoneme sequences of at least min_length.
    """
    phones = pronouncing.phones_for_word(word)
    if not phones:
        return []
    
    phone_list = phones[0].split()
    clusters = []
    
    # Extract all possible clusters of min_length or more
    for start in range(len(phone_list)):
        for end in range(start + min_length, len(phone_list) + 1):
            cluster = ' '.join(phone_list[start:end])
            clusters.append(cluster)
    
    return clusters


def find_rhyming_pairs(words):
    """
    Find pairs of words that rhyme (share rhyming parts).
    Returns count of rhyming pairs.
    """
    rhyme_parts = []
    for word in words:
        phones = pronouncing.phones_for_word(word)
        if phones:
            rhyme_part = pronouncing.rhyming_part(phones[0])
            if rhyme_part:
                rhyme_parts.append((word, rhyme_part))
    
    # Count unique rhyming pairs
    pairs = 0
    seen = set()
    for i in range(len(rhyme_parts)):
        for j in range(i + 1, len(rhyme_parts)):
            word1, part1 = rhyme_parts[i]
            word2, part2 = rhyme_parts[j]
            if part1 == part2 and word1 != word2:
                pair = tuple(sorted([word1, word2]))
                if pair not in seen:
                    seen.add(pair)
                    pairs += 1
    
    return pairs


def find_phoneme_repetitions(words, min_cluster_size=2):
    """
    Find repeated phoneme clusters within words.
    Returns count of repetitions.
    """
    # Build a map of phoneme clusters to words
    cluster_map = {}
    
    for word in words:
        clusters = get_phoneme_clusters(word, min_cluster_size)
        for cluster in clusters:
            if cluster not in cluster_map:
                cluster_map[cluster] = []
            cluster_map[cluster].append(word)
    
    # Count clusters that appear in multiple words
    repetitions = 0
    for cluster, cluster_words in cluster_map.items():
        # Get unique words (a word might have the same cluster multiple times)
        unique_words = set(cluster_words)
        if len(unique_words) > 1:
            # Award points based on how many words share this cluster
            repetitions += len(unique_words) - 1
    
    return repetitions


def score_internal_rhyme(stanza):
    """
    Score the internal rhyme quality of a stanza.
    
    Awards points for:
    - Words that rhyme within the same line
    - Repeated phoneme clusters across words
    - Multiple rhyming instances
    
    Args:
        stanza (str): The text to evaluate (multi-line string)
    
    Returns:
        float: Score representing internal rhyme richness (higher is better)
              Score is roughly proportional to the number of internal rhymes found.
    
    Examples:
        >>> stanza = "I'm drastically plastic and enthusiastic"
        >>> score_internal_rhyme(stanza)  # High score due to 'astic' repetition
        
        >>> stanza = "The cat sat on the mat"
        >>> score_internal_rhyme(stanza)  # High score due to 'at' sounds
    """
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    
    total_score = 0
    total_words = 0
    
    for line in lines:
        words = get_words(line)
        if len(words) < 2:
            continue
        
        total_words += len(words)
        
        # Score rhyming pairs
        rhyme_pairs = find_rhyming_pairs(words)
        total_score += rhyme_pairs * 10  # 10 points per rhyming pair
        
        # Score phoneme repetitions
        repetitions = find_phoneme_repetitions(words, min_cluster_size=2)
        total_score += repetitions * 5  # 5 points per repetition
    
    # Normalize by number of words to get a per-word score
    if total_words > 0:
        normalized_score = (total_score / total_words) * 10
    else:
        normalized_score = 0.0
    
    return normalized_score


def main():
    """CLI interface for internal rhyme scoring."""
    import sys
    
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            stanza = f.read()
    else:
        # Read from stdin
        print("Enter stanza (Ctrl+D or Ctrl+Z when done):")
        stanza = sys.stdin.read()
    
    score = score_internal_rhyme(stanza)
    
    lines = [line.strip() for line in stanza.strip().split('\n') if line.strip()]
    
    print(f"\nInternal rhyme score: {score:.2f}")
    print(f"Analysis of {len(lines)} line(s):")
    
    # Show detailed analysis per line
    for i, line in enumerate(lines, 1):
        words = get_words(line)
        if len(words) >= 2:
            rhyme_pairs = find_rhyming_pairs(words)
            repetitions = find_phoneme_repetitions(words)
            print(f"  Line {i}: {rhyme_pairs} rhyme pairs, {repetitions} phoneme repetitions")
            
            # Show some example rhyming words
            if rhyme_pairs > 0:
                rhyme_parts = []
                for word in words:
                    phones = pronouncing.phones_for_word(word)
                    if phones:
                        rhyme_part = pronouncing.rhyming_part(phones[0])
                        if rhyme_part:
                            rhyme_parts.append((word, rhyme_part))
                
                # Find and display rhyming words
                rhyming_words = []
                seen = set()
                for i in range(len(rhyme_parts)):
                    for j in range(i + 1, len(rhyme_parts)):
                        word1, part1 = rhyme_parts[i]
                        word2, part2 = rhyme_parts[j]
                        if part1 == part2 and word1 != word2:
                            pair = tuple(sorted([word1, word2]))
                            if pair not in seen:
                                seen.add(pair)
                                rhyming_words.append(f"{word1}/{word2}")
                
                if rhyming_words:
                    print(f"    Rhyming: {', '.join(rhyming_words)}")


if __name__ == '__main__':
    main()
