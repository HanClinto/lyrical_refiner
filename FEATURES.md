# Lyrical Refiner - Feature Overview

## Visual Features

### 1. Rich-Text Color Highlighting

Words that rhyme are automatically highlighted with matching colors:

```
Example Display:
┌─────────────────────────────────────┐
│  Roses are red                      │  ← "red" not highlighted (no rhyme found)
│  Violets are [blue]                 │  ← "blue" highlighted in color A
│  Sugar is sweet                     │  ← "sweet" not highlighted
│  And so are [you]                   │  ← "you" highlighted in color A (rhymes with "blue")
│                                     │
│  The stars at [night]               │  ← "night" highlighted in color B
│  Shine oh so [bright]               │  ← "bright" highlighted in color B (rhymes with "night")
│  Making dreams come [true]          │  ← "true" highlighted in color C
│  Under skies of [blue]              │  ← "blue" highlighted in color C (rhymes with "true")
└─────────────────────────────────────┘

[bracketed words] = color-highlighted text
```

### 2. Sidebar Scoring

Real-time quality metrics for each stanza:

```
┌────────────────────┐
│  Stanza Scores     │
├────────────────────┤
│                    │
│ ═══ Stanza 1 ═══   │
│ Total Score: 39.5  │  ← Overall quality
│   Rhyme: 16.7      │  ← Rhyme density
│   Density: 65.0    │  ← Word count optimization
│   Lines: 4         │  ← Number of lines
│                    │
│ ═══ Stanza 2 ═══   │
│ Total Score: 54.0  │
│   Rhyme: 33.3      │  ← Better rhyme score!
│   Density: 80.0    │
│   Lines: 4         │
│                    │
└────────────────────┘
```

### 3. Color Scheme

10 distinct colors for different rhyme groups:

1. 🟥 Light Red (#FFB3BA)
2. 🟩 Light Green (#BAFFC9)
3. 🟦 Light Blue (#BAE1FF)
4. 🟨 Light Yellow (#FFFFBA)
5. 🟧 Light Orange (#FFDFBA)
6. 🟪 Light Purple (#E0BBE4)
7. 🟫 Light Peach (#FFDFD3)
8. 🟦 Light Lavender (#C7CEEA)
9. 🟦 Light Cyan (#B2F7EF)
10. 🌸 Light Pink (#F4ACB7)

Colors rotate automatically for different rhyme groups.

## Smart Features

### Automatic Stanza Detection

Stanzas are automatically separated when you leave blank lines:

```
Stanza 1
Line 1
Line 2
← blank line here
Stanza 2
Line 1
Line 2
```

### Real-Time Updates

- Changes appear after 500ms of typing inactivity
- Prevents flickering and lag
- Smooth user experience

### End-Word Emphasis

Words at the end of lines are automatically **bolded** to emphasize the rhyme scheme.

## Scoring System Explained

### Total Score (0-100)

Weighted combination of three factors:
- **60%** Rhyme Quality
- **30%** Word Density
- **10%** Line Count

### Rhyme Score (0-100)

Measures how well lines rhyme with each other:
- **100%**: All lines have rhyming partners
- **50%**: Half the line pairs rhyme
- **0%**: No rhymes detected

**Example:**
```
Roses are red     ┐
Violets are blue  ┘ → These 2 lines rhyme
Sugar is sweet    ┐
And so are you    ┘ → These 2 lines rhyme

Score: 16.7% (1 pair out of 6 possible pairs rhyme)
```

### Density Score (0-100)

Evaluates word count per line:
- **100%**: 5-10 words per line (optimal)
- **60%**: 3 words per line (too sparse)
- **50%**: 15 words per line (too dense)

**Why it matters:** 
- Too few words: Choppy, incomplete thoughts
- Too many words: Run-on, hard to follow
- Just right: Natural, flowing lyrics

### Line Count Factor (0-1)

Normalized by target of 4 lines:
- **1.0**: 4+ lines (full stanza)
- **0.5**: 2 lines (half stanza)
- **0.25**: 1 line (fragment)

## Example Scoring Breakdown

### High-Scoring Stanza (Score: 54.0)

```
The stars at night        (5 words)
Shine oh so bright        (4 words)
Making dreams come true   (4 words)
Under skies of blue       (4 words)
```

**Analysis:**
- ✓ 2 rhyme pairs: "night/bright" and "true/blue"
- ✓ Average 4.25 words per line (optimal)
- ✓ 4 lines (complete stanza)
- **Result:** Rhyme 33.3%, Density 80.0%, Total 54.0%

### Low-Scoring Stanza (Score: 39.5)

```
Roses are red        (3 words)
Violets are blue     (3 words)
Sugar is sweet       (3 words)
And so are you       (4 words)
```

**Analysis:**
- ⚠ Only 1 rhyme pair: "blue/you"
- ⚠ Average 3.25 words per line (too sparse)
- ✓ 4 lines (complete stanza)
- **Result:** Rhyme 16.7%, Density 65.0%, Total 39.5%

**To Improve:** Add more words per line and more rhyming line pairs!

## Usage Tips

### Getting Better Scores

1. **More Rhymes:** Try to rhyme multiple line pairs
   ```
   Good: ABAB rhyme scheme
   Better: AABB rhyme scheme
   Best: AAAA rhyme scheme (all lines rhyme!)
   ```

2. **Optimal Length:** Aim for 5-10 words per line
   ```
   Too short: "Roses red"           (2 words)
   Perfect:   "Roses are so red"    (4 words)
   Too long:  "Roses are extremely very super red today"  (7 words)
   ```

3. **Complete Stanzas:** Write at least 4 lines per stanza

### Common Rhyme Schemes

- **AABB:** "roses/poses, blue/true"
- **ABAB:** "roses/blue, poses/true"
- **ABCB:** "roses/blue, poses/true" (last words rhyme)
- **AAAA:** "day/say/way/play" (all rhyme)

## Technical Features

### Phonetic Matching

Uses the CMU Pronouncing Dictionary for accurate rhyme detection:
- Analyzes word sounds, not just spelling
- "blue" rhymes with "true" (both end in /u/)
- "cough" doesn't rhyme with "rough" (different sounds)

### Performance Optimization

- **Caching:** Previously searched words are cached
- **Debouncing:** Updates delayed to reduce lag
- **Efficient Algorithms:** O(n²) complexity for n end-words

### Keyboard Shortcuts

- **Ctrl+Z:** Undo
- **Ctrl+Y:** Redo (platform dependent)
- **Ctrl+C/V/X:** Copy/Paste/Cut

## Limitations

### Current Version Limitations

1. **End-Word Only:** Only detects rhymes at line endings
   - Internal rhymes not detected
   - Mid-line rhymes not highlighted

2. **Dictionary Dependent:** Limited to CMU Dictionary
   - Made-up words not recognized
   - Some slang/modern terms missing

3. **Perfect Rhymes Only:** Only exact phonetic matches
   - Near-rhymes (e.g., "love/move") not detected
   - Assonance/consonance not recognized

4. **English Only:** Currently only supports English lyrics

### Future Enhancements

Planned features for future versions:
- Internal rhyme detection
- Near-rhyme/slant-rhyme support
- Syllable counting and meter analysis
- Alliteration highlighting
- Multi-language support
- Export to PDF/HTML
- AI-powered suggestions
- Cloud sync/save

## Comparison with Traditional Tools

| Feature | Notepad | Word | Lyrical Refiner |
|---------|---------|------|-----------------|
| Basic text editing | ✓ | ✓ | ✓ |
| Spell check | ✗ | ✓ | ✗* |
| Rhyme detection | ✗ | ✗ | ✓ |
| Visual highlighting | ✗ | Manual | Auto |
| Quality scoring | ✗ | ✗ | ✓ |
| Stanza separation | Manual | Manual | Auto |
| Real-time feedback | ✗ | ✗ | ✓ |

*Spell check could be added in future versions

## Target Users

Perfect for:
- 🎤 **Songwriters** - Craft better lyrics with visual feedback
- 📝 **Poets** - See rhyme patterns clearly
- 🎓 **Students** - Learn about poetry and rhyme schemes
- 🎨 **Creative Writers** - Experiment with lyrical writing
- 🎵 **Rappers** - Optimize rhyme density and flow

## Success Stories (Hypothetical)

> "I used to struggle seeing which lines rhymed. Now it's obvious!"
> — Aspiring Songwriter

> "The scoring system helped me understand what makes good lyrics."
> — Poetry Student

> "Visual feedback makes writing so much more engaging!"
> — Creative Writer

---

**Ready to start?** Run `python3 lyrical_refiner.py` and begin writing!
