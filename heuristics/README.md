# Poetic Evaluation Heuristics

This directory contains standalone heuristics for evaluating various poetic attributes of text. Each heuristic can be run independently via CLI, imported as a Python module, or used through the main evaluation tool.

## Available Heuristics

### 1. End Rhyme (`end_rhyme.py`)
Evaluates how well line endings follow common rhyme schemes (ABAB, AABB, etc.).

**Score Range:** 0-100 (percentage match to rhyme scheme)

**Usage:**
```bash
# Run standalone
python3 -m heuristics.end_rhyme < input.txt

# Use in Python
from heuristics import score_end_rhyme
score = score_end_rhyme("The cat sat on the mat\nThe rat wore a hat")
```

**What it measures:**
- Detects rhyme schemes automatically
- Scores adherence to expected rhyme patterns
- Uses phonetic matching from the CMU Pronouncing Dictionary

### 2. Internal Rhyme (`internal_rhyme.py`)
Evaluates rhyming words within lines (not just at the ends).

**Score Range:** Higher is better (no fixed upper bound)

**Usage:**
```bash
# Run standalone
python3 -m heuristics.internal_rhyme < input.txt

# Use in Python
from heuristics import score_internal_rhyme
score = score_internal_rhyme("I'm drastically plastic and enthusiastic")
```

**What it measures:**
- Finds words that rhyme within the same line
- Detects repeated phoneme clusters
- Awards more points for multiple rhyming instances

### 3. Mosaic Rhyme (`mosaic_rhyme.py`)
Evaluates multi-word rhymes where a sequence of words rhymes with a single word.

**Score Range:** Higher is better (no fixed upper bound)

**Usage:**
```bash
# Run standalone
python3 -m heuristics.mosaic_rhyme < input.txt

# Use in Python
from heuristics import score_mosaic_rhyme
score = score_mosaic_rhyme("oh there goes gravity\noh he's so mad but he")
```

**What it measures:**
- Finds sequences of 2-3 words that rhyme with single words
- Example: "gravity" rhyming with "mad but he"
- Awards points based on sequence length

### 4. Syllable Meter (`syllable_meter.py`)
Evaluates metrical consistency based on syllable counts and stress patterns.

**Score Range:** 0-100 (consistency measure)

**Usage:**
```bash
# Run standalone
python3 -m heuristics.syllable_meter < input.txt

# Use in Python
from heuristics import score_syllable_meter
score = score_syllable_meter("Shall I compare thee to a summer's day")
```

**What it measures:**
- Consistency of syllable counts across lines
- Detection of common metrical feet (iambic, trochaic, etc.)
- Stress pattern analysis

### 5. Alliteration (`alliteration.py`)
Evaluates the presence of repeated initial consonant sounds.

**Score Range:** Higher is better (no fixed upper bound)

**Usage:**
```bash
# Run standalone
python3 -m heuristics.alliteration < input.txt

# Use in Python
from heuristics import score_alliteration
score = score_alliteration("Peter Piper picked a peck of pickled peppers")
```

**What it measures:**
- Consecutive words starting with the same sound
- Non-consecutive alliteration within a gap
- Awards more points for longer alliterative sequences

## Using the Main Evaluation Tool

Run all heuristics at once:

```bash
# Evaluate all heuristics
python3 evaluate_poetry.py input.txt

# Or from stdin
echo "Your poem here" | python3 evaluate_poetry.py

# Run specific heuristic only
python3 evaluate_poetry.py --heuristic end_rhyme input.txt
```

## Dependencies

The heuristics use the `pronouncing` Python library, which provides:
- CMU Pronouncing Dictionary for phonetic lookup
- Syllable counting
- Stress pattern analysis
- Rhyme detection

Install dependencies:
```bash
pip install -r requirements.txt
```

## How Scores Work

- **End Rhyme** and **Syllable Meter**: 0-100 scale (percentage-based)
- **Internal Rhyme**, **Mosaic Rhyme**, and **Alliteration**: Open-ended scales where higher is better
  - Scores are roughly proportional to the amount of the poetic device present
  - Normalized by text length to allow comparison across different stanza sizes

## Design Philosophy

Each heuristic is:
- **Standalone**: Can be run independently without dependencies on other heuristics
- **Simple**: Straightforward algorithms, no over-engineering
- **Phonetic-based**: Uses actual pronunciation data, not just spelling
- **Quantitative**: Returns numeric scores for objective comparison

## Examples

### Perfect AABB Rhyme Scheme
```
The cat sat on the mat
The rat wore a fancy hat
The dog ran through the fog
The hog jumped like a frog
```
- End Rhyme: 100/100
- Syllable Meter: ~79/100

### Strong Alliteration
```
Peter Piper picked a peck of pickled peppers
```
- Alliteration: ~88/100
- Internal Rhyme: ~31/100

### Internal Rhyme Example
```
I'm drastically plastic and enthusiastic
```
- Internal Rhyme: High score due to "-astic" repetition
