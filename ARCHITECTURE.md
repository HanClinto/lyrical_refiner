# Lyrical Refiner - Architecture

## Overview

The Lyrical Refiner is a Python desktop application built with tkinter that provides real-time visual feedback for lyric writing through rhyme detection and quality scoring.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LyricalRefiner (GUI)                     │
│  - Main Tkinter window                                      │
│  - Text editor with rich-text formatting                    │
│  - Sidebar for stanza scores                                │
│  - Event handling and UI updates                            │
└────────────┬──────────────────────────┬─────────────────────┘
             │                          │
             ▼                          ▼
    ┌────────────────┐         ┌───────────────┐
    │ RhymeDetector  │         │StanzaScorer   │
    │ - CMU Dict     │◄────────┤- Rhyme score  │
    │ - Phonetic     │         │- Density score│
    │   matching     │         │- Line count   │
    └────────────────┘         └───────────────┘
             │
             ▼
    ┌────────────────┐
    │  pronouncing   │
    │   library      │
    └────────────────┘
```

## Core Components

### 1. RhymeDetector
**Purpose:** Identifies rhyming words using phonetic analysis

**Key Methods:**
- `get_rhymes(word)` - Returns set of words that rhyme with input
- `do_words_rhyme(word1, word2)` - Boolean check if two words rhyme
- `get_phonemes(word)` - Returns phonetic representation

**Implementation Details:**
- Uses CMU Pronouncing Dictionary via `pronouncing` library
- Caches rhyme lookups for performance
- Strips punctuation for accurate matching

### 2. StanzaScorer
**Purpose:** Evaluates lyric quality using multiple heuristics

**Scoring Algorithm:**
```
Total Score = (Rhyme × 0.6) + (Density × 0.3) + (Lines × 0.1) × 100

Where:
- Rhyme = Proportion of line-ending words that rhyme
- Density = Optimization factor for 5-10 words per line
- Lines = min(line_count / 4, 1.0)
```

**Key Methods:**
- `score_stanza(stanza)` - Returns dict with all scores
- `_calculate_rhyme_score(lines)` - Analyzes end-word rhyming
- `_calculate_density_score(lines)` - Evaluates word density

### 3. LyricalRefiner (Main GUI)
**Purpose:** Provides the user interface and orchestrates all features

**UI Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                  Lyrical Refiner                        │
│                                                         │
│  ┌──────────────────────┐  ┌───────────────────────┐   │
│  │                      │  │   Stanza Scores       │   │
│  │   Text Editor        │  │                       │   │
│  │   (with colored      │  │  ═══ Stanza 1 ═══     │   │
│  │    highlights)       │  │  Total: 39.5/100      │   │
│  │                      │  │  Rhyme: 16.7/100      │   │
│  │  Roses are red       │  │  Density: 65.0/100    │   │
│  │  Violets are blue    │  │  Lines: 4             │   │
│  │                      │  │                       │   │
│  │  Sugar is sweet      │  │  ═══ Stanza 2 ═══     │   │
│  │  And so are you      │  │  Total: 54.0/100      │   │
│  │                      │  │  ...                  │   │
│  └──────────────────────┘  └───────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Key Features:**
- Real-time text editing with undo/redo
- 500ms debounced update system
- 10 distinct color schemes for rhyme groups
- Bold formatting for line-ending words
- Automatic stanza detection via blank line regex

## Data Flow

1. **User Types** → Text widget receives input
2. **Event Triggered** → `schedule_update()` called after 500ms delay
3. **Parse Text** → `parse_stanzas()` splits by blank lines
4. **Find Rhymes** → `highlight_rhymes()` detects and colors matches
5. **Calculate Scores** → `update_scores()` evaluates each stanza
6. **Update Display** → GUI reflects all changes

## Key Algorithms

### Rhyme Detection Algorithm
```python
1. Extract end word from each line
2. For each word pair:
   a. Query CMU dictionary for phonemes
   b. Compare phonetic endings
   c. Mark as rhyme if matching
3. Group rhyming words
4. Assign colors to groups (cycling through 10 colors)
```

### Stanza Parsing Algorithm
```python
1. Split text by regex: r'\n\s*\n' (one or more blank lines)
2. Strip whitespace from each stanza
3. Filter out empty stanzas
4. Return list of stanza strings
```

### Scoring Algorithm Details

**Rhyme Score:**
- Calculates all possible pairs of line-ending words
- Counts how many pairs rhyme
- Returns ratio: rhyme_pairs / total_pairs

**Density Score:**
- Optimal range: 5-10 words per line
- Inside range: score = 1.0
- Below range: score = avg_words / 5.0
- Above range: score = max(0, 1.0 - (avg_words - 10) / 10)

**Line Count Factor:**
- Normalized to 0-1 range
- 4+ lines = 1.0, fewer lines scale proportionally
- Ensures stanzas aren't too short

## Performance Considerations

1. **Caching:** RhymeDetector caches phoneme lookups to avoid repeated API calls
2. **Debouncing:** UI updates delayed 500ms to prevent excessive redraws
3. **Lazy Evaluation:** Only visible stanzas are processed
4. **Efficient Regex:** Stanza splitting uses compiled regex patterns

## Extension Points

Future enhancements could include:

1. **Additional Scoring Metrics:**
   - Syllable counting and meter analysis
   - Alliteration detection
   - Internal rhyme detection (not just end words)

2. **Advanced Features:**
   - Export to various formats (PDF, HTML)
   - Rhyme suggestions for incomplete lines
   - Theme customization
   - Auto-save functionality

3. **AI Integration:**
   - GPT-based line suggestions
   - Style analysis and recommendations
   - Sentiment analysis

## Dependencies

- **Python 3.6+:** Core language
- **tkinter:** GUI framework (usually bundled with Python)
- **pronouncing:** CMU Pronouncing Dictionary wrapper
  - Depends on: cmudict, importlib-metadata, importlib-resources

## File Structure

```
lyrical_refiner/
├── lyrical_refiner.py   # Main application (346 lines)
├── demo.py              # Command-line demo (207 lines)
├── test_core.py         # Unit tests (200 lines)
├── requirements.txt     # Python dependencies
├── README.md            # Project overview
├── USAGE.md             # User guide
├── ARCHITECTURE.md      # This file
└── LICENSE              # License information
```

## Testing Strategy

1. **Unit Tests:** Core logic tested independently of GUI
2. **Integration Tests:** Demo script validates end-to-end functionality
3. **Manual Testing:** GUI requires manual testing for visual elements

## Design Principles

1. **Separation of Concerns:** Logic separated from presentation
2. **Single Responsibility:** Each class has one clear purpose
3. **Modularity:** Components can be tested and used independently
4. **User-Centric:** Focus on immediate visual feedback
5. **Performance:** Optimized for real-time interaction
