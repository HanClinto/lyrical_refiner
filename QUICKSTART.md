# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### Evaluate All Heuristics

```bash
python3 evaluate_poetry.py input.txt
```

Or from stdin:
```bash
echo "Your poem here" | python3 evaluate_poetry.py
```

### Run Individual Heuristics

Each heuristic can be run independently:

```bash
# End rhyme detection
python3 -m heuristics.end_rhyme < poem.txt

# Internal rhyme detection
python3 -m heuristics.internal_rhyme < poem.txt

# Mosaic rhyme detection
python3 -m heuristics.mosaic_rhyme < poem.txt

# Syllable meter analysis
python3 -m heuristics.syllable_meter < poem.txt

# Alliteration detection
python3 -m heuristics.alliteration < poem.txt
```

### Run Specific Heuristic Only

```bash
python3 evaluate_poetry.py --heuristic end_rhyme input.txt
```

## Examples

### Example 1: Perfect AABB Rhyme

```bash
cat << EOF | python3 evaluate_poetry.py
The cat sat on the mat
The rat wore a fancy hat
The dog ran through the fog
The hog jumped like a frog
EOF
```

Expected output:
- End Rhyme: 100/100
- High Syllable Meter score

### Example 2: Alliteration

```bash
echo "Peter Piper picked a peck of pickled peppers" | python3 evaluate_poetry.py
```

Expected output:
- High Alliteration score (75+)

### Example 3: Internal Rhyme

```bash
echo "I'm drastically plastic and enthusiastic" | python3 evaluate_poetry.py
```

Expected output:
- High Internal Rhyme score (150+)

## Using in Python Code

```python
from heuristics import (
    score_end_rhyme,
    score_internal_rhyme,
    score_mosaic_rhyme,
    score_syllable_meter,
    score_alliteration,
)

stanza = """The cat sat on the mat
The rat wore a fancy hat"""

# Score individual heuristics
end_rhyme_score = score_end_rhyme(stanza)
alliteration_score = score_alliteration(stanza)

print(f"End Rhyme: {end_rhyme_score:.2f}")
print(f"Alliteration: {alliteration_score:.2f}")
```

## Running Tests

```bash
# Run all tests
python3 tests/test_end_rhyme.py
python3 tests/test_internal_rhyme.py
python3 tests/test_alliteration.py
python3 tests/test_integration.py
```

## Understanding Scores

### Fixed Range (0-100)
- **End Rhyme**: Percentage match to rhyme scheme
- **Syllable Meter**: Consistency of syllable counts and meter

### Open-Ended (Higher is Better)
- **Internal Rhyme**: Proportional to rhyming words found
- **Mosaic Rhyme**: Proportional to multi-word rhymes found
- **Alliteration**: Proportional to alliterative sequences found

## Sample Files

See `examples/sample_poems.txt` for example poems demonstrating each heuristic.
