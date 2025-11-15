#!/usr/bin/env python3
"""
Poetic Evaluation CLI Tool

Run all heuristics on a given text input to evaluate its poetic quality.
"""

import sys
import argparse
from heuristics import (
    score_end_rhyme,
    score_internal_rhyme,
    score_mosaic_rhyme,
    score_syllable_meter,
    score_alliteration,
)


def evaluate_all(stanza):
    """
    Run all heuristics on the given stanza.
    Returns a dictionary of scores.
    """
    return {
        'end_rhyme': score_end_rhyme(stanza),
        'internal_rhyme': score_internal_rhyme(stanza),
        'mosaic_rhyme': score_mosaic_rhyme(stanza),
        'syllable_meter': score_syllable_meter(stanza),
        'alliteration': score_alliteration(stanza),
    }


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate poetic quality using multiple heuristics'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Input file containing the stanza to evaluate (default: stdin)'
    )
    parser.add_argument(
        '--heuristic',
        choices=['end_rhyme', 'internal_rhyme', 'mosaic_rhyme', 'syllable_meter', 'alliteration', 'all'],
        default='all',
        help='Specific heuristic to run (default: all)'
    )
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, 'r') as f:
            stanza = f.read()
    else:
        print("Enter stanza (Ctrl+D or Ctrl+Z when done):", file=sys.stderr)
        stanza = sys.stdin.read()
    
    if not stanza.strip():
        print("Error: No input provided", file=sys.stderr)
        return 1
    
    # Run heuristics
    if args.heuristic == 'all':
        scores = evaluate_all(stanza)
        
        print("\n" + "="*60)
        print("POETIC EVALUATION RESULTS")
        print("="*60)
        
        for name, score in scores.items():
            print(f"{name.replace('_', ' ').title():.<40} {score:>8.2f}")
        
        # Calculate overall score (simple average)
        overall = sum(scores.values()) / len(scores)
        print("-"*60)
        print(f"{'Overall Average':.<40} {overall:>8.2f}")
        print("="*60)
    else:
        # Run specific heuristic
        heuristic_map = {
            'end_rhyme': score_end_rhyme,
            'internal_rhyme': score_internal_rhyme,
            'mosaic_rhyme': score_mosaic_rhyme,
            'syllable_meter': score_syllable_meter,
            'alliteration': score_alliteration,
        }
        
        score_func = heuristic_map[args.heuristic]
        score = score_func(stanza)
        
        print(f"\n{args.heuristic.replace('_', ' ').title()} Score: {score:.2f}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
