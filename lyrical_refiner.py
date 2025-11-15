#!/usr/bin/env python3
"""
Lyrical Refiner - A rich-text lyric editor with rhyme detection and scoring.

This application provides a smart notepad interface for writing song lyrics with:
- Color-coded rhyme detection
- Stanza separation and scoring
- Visual feedback for lyrical patterns
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import re
from typing import List, Dict, Set, Tuple
import pronouncing


class RhymeDetector:
    """Handles rhyme detection using phonetic analysis."""
    
    def __init__(self):
        self.word_cache = {}
    
    def get_rhymes(self, word: str) -> Set[str]:
        """Get all words that rhyme with the given word."""
        word_clean = word.lower().strip('.,!?;:"\'-')
        if not word_clean:
            return set()
            
        if word_clean in self.word_cache:
            return self.word_cache[word_clean]
        
        rhymes = set(pronouncing.rhymes(word_clean))
        self.word_cache[word_clean] = rhymes
        return rhymes
    
    def do_words_rhyme(self, word1: str, word2: str) -> bool:
        """Check if two words rhyme."""
        word1_clean = word1.lower().strip('.,!?;:"\'-')
        word2_clean = word2.lower().strip('.,!?;:"\'-')
        
        if not word1_clean or not word2_clean or word1_clean == word2_clean:
            return False
        
        rhymes = self.get_rhymes(word1_clean)
        return word2_clean in rhymes
    
    def get_phonemes(self, word: str) -> List[str]:
        """Get phoneme representation of a word."""
        word_clean = word.lower().strip('.,!?;:"\'-')
        if not word_clean:
            return []
        phones = pronouncing.phones_for_word(word_clean)
        return phones[0] if phones else []


class StanzaScorer:
    """Scores stanzas based on various heuristics."""
    
    def __init__(self, rhyme_detector: RhymeDetector):
        self.rhyme_detector = rhyme_detector
    
    def score_stanza(self, stanza: str) -> Dict[str, float]:
        """
        Score a stanza based on multiple heuristics.
        Returns a dictionary with individual scores and total.
        """
        lines = [line.strip() for line in stanza.split('\n') if line.strip()]
        
        if not lines:
            return {'total': 0, 'rhyme_score': 0, 'density_score': 0, 'line_count': 0}
        
        # Calculate rhyme score
        rhyme_score = self._calculate_rhyme_score(lines)
        
        # Calculate word density score (words per line)
        density_score = self._calculate_density_score(lines)
        
        # Line count factor
        line_count = len(lines)
        
        # Total score is weighted combination
        total = (rhyme_score * 0.6 + density_score * 0.3 + min(line_count / 4, 1.0) * 0.1) * 100
        
        return {
            'total': round(total, 1),
            'rhyme_score': round(rhyme_score * 100, 1),
            'density_score': round(density_score * 100, 1),
            'line_count': line_count
        }
    
    def _calculate_rhyme_score(self, lines: List[str]) -> float:
        """Calculate rhyme score based on end-word rhymes."""
        if len(lines) < 2:
            return 0.0
        
        end_words = []
        for line in lines:
            words = re.findall(r'\b\w+\b', line)
            if words:
                end_words.append(words[-1])
        
        if len(end_words) < 2:
            return 0.0
        
        # Count rhyming pairs
        rhyme_pairs = 0
        total_pairs = 0
        
        for i in range(len(end_words)):
            for j in range(i + 1, len(end_words)):
                total_pairs += 1
                if self.rhyme_detector.do_words_rhyme(end_words[i], end_words[j]):
                    rhyme_pairs += 1
        
        return rhyme_pairs / total_pairs if total_pairs > 0 else 0.0
    
    def _calculate_density_score(self, lines: List[str]) -> float:
        """Calculate score based on word density (words per line)."""
        word_counts = []
        for line in lines:
            words = re.findall(r'\b\w+\b', line)
            word_counts.append(len(words))
        
        if not word_counts:
            return 0.0
        
        avg_words = sum(word_counts) / len(word_counts)
        # Optimal range is 5-10 words per line
        if 5 <= avg_words <= 10:
            return 1.0
        elif avg_words < 5:
            return avg_words / 5.0
        else:
            return max(0.0, 1.0 - (avg_words - 10) / 10)


class LyricalRefiner(tk.Tk):
    """Main application window for the Lyrical Refiner."""
    
    # Color scheme for rhyme groups
    RHYME_COLORS = [
        '#FFB3BA',  # Light red
        '#BAFFC9',  # Light green
        '#BAE1FF',  # Light blue
        '#FFFFBA',  # Light yellow
        '#FFDFBA',  # Light orange
        '#E0BBE4',  # Light purple
        '#FFDFD3',  # Light peach
        '#C7CEEA',  # Light lavender
        '#B2F7EF',  # Light cyan
        '#F4ACB7',  # Light pink
    ]
    
    def __init__(self):
        super().__init__()
        
        self.title("Lyrical Refiner")
        self.geometry("1000x700")
        
        self.rhyme_detector = RhymeDetector()
        self.stanza_scorer = StanzaScorer(self.rhyme_detector)
        
        self.setup_ui()
        
        # Bind text change event
        self.text_widget.bind('<<Modified>>', self.on_text_modified)
        self.text_widget.bind('<KeyRelease>', self.schedule_update)
        
        self.update_scheduled = False
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create main container
        main_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left side: Text editor
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=3)
        
        # Title label
        title_label = ttk.Label(left_frame, text="Lyrical Refiner", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=5)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(left_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 12),
                                   undo=True, maxundo=-1)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text_widget.yview)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text tags for highlighting
        for i, color in enumerate(self.RHYME_COLORS):
            self.text_widget.tag_config(f'rhyme_{i}', background=color, font=('Arial', 12, 'bold'))
        
        self.text_widget.tag_config('end_word', font=('Arial', 12, 'bold'))
        
        # Right side: Sidebar with scores
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        sidebar_label = ttk.Label(right_frame, text="Stanza Scores", 
                                 font=('Arial', 14, 'bold'))
        sidebar_label.pack(pady=5)
        
        # Scrolled text for scores
        self.score_widget = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, 
                                                      font=('Courier', 10),
                                                      width=30, state=tk.DISABLED)
        self.score_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Instructions
        instructions = ttk.Label(left_frame, 
                                text="Type your lyrics below. Separate stanzas with blank lines.",
                                font=('Arial', 9, 'italic'))
        instructions.pack(pady=2)
    
    def schedule_update(self, event=None):
        """Schedule an update after a short delay to avoid too frequent updates."""
        if not self.update_scheduled:
            self.update_scheduled = True
            self.after(500, self.update_display)
    
    def on_text_modified(self, event=None):
        """Handle text modification event."""
        self.text_widget.edit_modified(False)
    
    def update_display(self):
        """Update the display with rhyme highlighting and scores."""
        self.update_scheduled = False
        
        # Get current text
        text = self.text_widget.get('1.0', 'end-1c')
        
        # Clear all existing tags
        for i in range(len(self.RHYME_COLORS)):
            self.text_widget.tag_remove(f'rhyme_{i}', '1.0', 'end')
        self.text_widget.tag_remove('end_word', '1.0', 'end')
        
        # Parse stanzas
        stanzas = self.parse_stanzas(text)
        
        # Find and highlight rhymes
        self.highlight_rhymes(text, stanzas)
        
        # Update scores
        self.update_scores(stanzas)
    
    def parse_stanzas(self, text: str) -> List[str]:
        """Parse text into stanzas separated by blank lines."""
        # Split by one or more blank lines
        stanzas = re.split(r'\n\s*\n', text)
        return [s.strip() for s in stanzas if s.strip()]
    
    def highlight_rhymes(self, text: str, stanzas: List[str]):
        """Highlight rhyming words across the entire text."""
        # Collect all end words from all lines
        all_end_words = []
        all_lines = text.split('\n')
        
        for line_idx, line in enumerate(all_lines):
            words = re.findall(r'\b\w+\b', line)
            if words:
                end_word = words[-1]
                # Find position in text widget
                word_pattern = r'\b' + re.escape(end_word) + r'\b'
                start_pos = f'{line_idx + 1}.0'
                line_end = f'{line_idx + 1}.end'
                
                # Search for the last occurrence of the word in the line
                pos = self.text_widget.search(word_pattern, start_pos, line_end, 
                                              regexp=True, backwards=True)
                if pos:
                    all_end_words.append((end_word, pos, line_idx))
        
        # Group rhyming words
        rhyme_groups = []
        used_indices = set()
        
        for i, (word1, pos1, line1) in enumerate(all_end_words):
            if i in used_indices:
                continue
            
            group = [(word1, pos1, line1, i)]
            used_indices.add(i)
            
            for j, (word2, pos2, line2) in enumerate(all_end_words):
                if j in used_indices:
                    continue
                if self.rhyme_detector.do_words_rhyme(word1, word2):
                    group.append((word2, pos2, line2, j))
                    used_indices.add(j)
            
            if len(group) > 1:
                rhyme_groups.append(group)
        
        # Apply colors to rhyme groups
        for group_idx, group in enumerate(rhyme_groups):
            color_idx = group_idx % len(self.RHYME_COLORS)
            tag_name = f'rhyme_{color_idx}'
            
            for word, pos, line_idx, _ in group:
                end_pos = f'{pos}+{len(word)}c'
                self.text_widget.tag_add(tag_name, pos, end_pos)
    
    def update_scores(self, stanzas: List[str]):
        """Update the score display in the sidebar."""
        self.score_widget.config(state=tk.NORMAL)
        self.score_widget.delete('1.0', 'end')
        
        if not stanzas:
            self.score_widget.insert('1.0', "No stanzas yet.\n\nStart typing and\nseparate stanzas\nwith blank lines.")
        else:
            for i, stanza in enumerate(stanzas, 1):
                scores = self.stanza_scorer.score_stanza(stanza)
                
                self.score_widget.insert('end', f"═══ Stanza {i} ═══\n")
                self.score_widget.insert('end', f"Total Score: {scores['total']}/100\n")
                self.score_widget.insert('end', f"  Rhyme: {scores['rhyme_score']}/100\n")
                self.score_widget.insert('end', f"  Density: {scores['density_score']}/100\n")
                self.score_widget.insert('end', f"  Lines: {scores['line_count']}\n")
                self.score_widget.insert('end', "\n")
        
        self.score_widget.config(state=tk.DISABLED)


def main():
    """Main entry point for the application."""
    app = LyricalRefiner()
    app.mainloop()


if __name__ == '__main__':
    main()
