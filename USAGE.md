# Lyrical Refiner - Usage Guide

## Overview

Lyrical Refiner is a rich-text Python application for writing song lyrics with intelligent rhyme detection and stanza scoring. It provides a smart notepad interface with visual feedback to help lyricists see connections between their rhymes.

## Features

- **Rich-text interface** - Color-coded text editor built with Python/Tkinter
- **Automatic rhyme detection** - Words that rhyme are highlighted with matching colors
- **Smart stanza separation** - Stanzas are automatically detected when separated by blank lines
- **Scoring system** - Each stanza receives a score based on:
  - Rhyme quality (how many lines rhyme)
  - Word density (optimal words per line)
  - Line count
- **Real-time updates** - Highlights and scores update as you type
- **Sidebar display** - All stanza scores visible at a glance

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python3 lyrical_refiner.py
```

## How to Use

1. **Launch the application** - Run `python3 lyrical_refiner.py`

2. **Start typing** - Enter your lyrics in the main text area

3. **Separate stanzas** - Leave at least one blank line between stanzas

4. **Watch the magic** - As you type:
   - Rhyming words will be highlighted with matching colors
   - The sidebar will show scores for each stanza
   - End-of-line words are bolded to emphasize rhyme patterns

5. **Review scores** - Check the sidebar to see:
   - Total score (0-100)
   - Rhyme score (how well lines rhyme)
   - Density score (word count optimization)
   - Line count for each stanza

## Example

Try typing this example to see the rhyme detection in action:

```
Roses are red
Violets are blue
Sugar is sweet
And so are you

The stars at night
Shine oh so bright
Making dreams come true
Under skies of blue
```

You'll see:
- "red" and "blue" highlighted (if they rhyme)
- "blue" and "you" highlighted with the same color
- "night" and "bright" highlighted together
- "true" and "blue" highlighted together
- Two separate stanza scores in the sidebar

## Tips

- **Use blank lines** - At least one blank line between stanzas for proper separation
- **End words matter** - The last word of each line is analyzed for rhymes
- **Experiment** - Try different rhyme schemes (AABB, ABAB, ABCB, etc.)
- **Check scores** - Higher rhyme scores indicate better rhyme density
- **Optimal length** - Aim for 5-10 words per line for best density scores

## Technical Details

- **Rhyme detection** - Uses the CMU Pronouncing Dictionary for phonetic analysis
- **Color scheme** - 10 different highlight colors cycle through rhyme groups
- **Scoring weights** - Total score = 60% rhyme + 30% density + 10% line count
- **Auto-save** - Changes update automatically after 500ms of inactivity

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- pronouncing library (for rhyme detection)

## Troubleshooting

**No rhymes detected:**
- Make sure words are correctly spelled
- The CMU dictionary might not have all words
- Try common English words for better results

**Colors not showing:**
- Wait 500ms after typing for updates
- Ensure words are at the end of lines
- At least 2 rhyming words needed for highlighting

**Application won't start:**
- Check Python version: `python3 --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Try: `python3 -m tkinter` to test tkinter installation
