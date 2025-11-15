# Lyrical Refiner

A rich-text Python application for writing song lyrics with intelligent rhyme detection and visual feedback. This smart notepad helps lyricists see connections between their rhymes through color-coding, highlighting, and stanza scoring.

## Features

✨ **Rich-Text Interface** - Color-coded editor with automatic formatting  
🎨 **Rhyme Detection** - Phonetic analysis highlights rhyming words  
📊 **Stanza Scoring** - Real-time quality metrics for each stanza  
⚡ **Live Updates** - Changes reflect immediately as you type  
📝 **Smart Notepad** - Simple, intuitive text editing experience  

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 lyrical_refiner.py
```

## Usage

1. Type your lyrics in the main editor
2. Separate stanzas with blank lines
3. Watch rhyming words get highlighted with matching colors
4. Check the sidebar for stanza scores and metrics

For detailed instructions, see [USAGE.md](USAGE.md)

## Example

```
Roses are red
Violets are blue

Sugar is sweet
And so are you
```

Words that rhyme (like "blue" and "you") will be highlighted with the same color!

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- pronouncing library

## Architecture

- **RhymeDetector** - Phonetic analysis using CMU Pronouncing Dictionary
- **StanzaScorer** - Multi-heuristic scoring system (rhyme density, word count, line count)
- **LyricalRefiner** - Main GUI application with tkinter

## Contributing

Contributions welcome! This project aims to help lyricists improve their craft through visual feedback and intelligent analysis.

## License

See [LICENSE](LICENSE) file for details.
