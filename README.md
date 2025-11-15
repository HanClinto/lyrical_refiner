# lyrical_refiner
A suite of tools and helpers for song lyric creation using a combination of agents, genetic algorithms, discrete heuristics, and colorful visualizations to experiment with ai-assisted lyric creation.

## Poetic Evaluation Heuristics

This project includes a comprehensive set of heuristics for evaluating poetic quality:

- **End Rhyme**: Detects and scores rhyme schemes (ABAB, AABB, etc.)
- **Internal Rhyme**: Finds rhyming words within lines
- **Mosaic Rhyme**: Detects multi-word rhymes (e.g., "gravity" ~ "mad but he")
- **Syllable Meter**: Evaluates metrical consistency and stress patterns
- **Alliteration**: Scores repeated initial consonant sounds

### Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Evaluate a poem:
```bash
python3 evaluate_poetry.py input.txt
```

3. Or use individual heuristics:
```bash
python3 -m heuristics.end_rhyme < input.txt
python3 -m heuristics.alliteration < input.txt
```

### Example

```bash
$ echo "Peter Piper picked a peck of pickled peppers" | python3 evaluate_poetry.py

============================================================
POETIC EVALUATION RESULTS
============================================================
End Rhyme...............................     0.00
Internal Rhyme..........................    31.25
Mosaic Rhyme............................   175.00
Syllable Meter..........................    70.00
Alliteration............................    87.50
------------------------------------------------------------
Overall Average.........................    72.75
============================================================
```

See [heuristics/README.md](heuristics/README.md) for detailed documentation.
