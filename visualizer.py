"""
visualizer.py - Synesthetic Visualizer
Person 2: Matplotlib, Image Generation
Creates all visual representations of synesthetic data.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
from io import BytesIO
import base64
from typing import Dict


class SynestheticVisualizer:
    """Generates all visualizations for the synesthesia simulator."""

    def __init__(self, output_dir='static/generated'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.generated_files = []

    def _save_and_encode(self, fig, filename):
        """Save figure to file and return base64 for web display."""
        filepath = os.path.join(self.output_dir, filename)
        fig.savefig(filepath, dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')

        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

        plt.close(fig)
        self.generated_files.append(filepath)

        return {
            'filepath': filepath,
            'filename': filename,
            'base64': 'data:image/png;base64,' + image_base64
        }

    def _is_dark(self, hex_color):
        """Check if color is dark for text contrast."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return brightness < 128

    def create_text_visualization(self, analysis_data, text, filename='text_visual.png'):
        """Create a color-field painting from text analysis."""
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.3)

        ax1 = fig.add_subplot(gs[0, :])
        chars_data = analysis_data['characters']
        visible_chars = [c for c in chars_data if not c['is_space']]
        n = len(visible_chars)

        if n == 0:
            ax1.text(0.5, 0.5, 'No valid characters', ha='center', va='center', fontsize=20)
        else:
            cols = int(np.ceil(np.sqrt(n * 1.5)))
            rows = int(np.ceil(n / cols))

            for idx, char_data in enumerate(visible_chars):
                row = idx // cols
                col = idx % cols
                color = char_data['color']
                char = char_data['character']

                rect = FancyBboxPatch(
                    (col, rows - row - 1), 0.95, 0.95,
                    boxstyle="round,pad=0.02",
                    facecolor=color,
                    edgecolor='white',
                    linewidth=2,
                    alpha=0.9
                )
                ax1.add_patch(rect)

                text_color = 'white' if self._is_dark(color) else 'black'
                ax1.text(col + 0.475, rows - row - 0.5, char,
                        ha='center', va='center', fontsize=max(10, 16 - cols//2),
                        fontweight='bold', color=text_color)

            ax1.set_xlim(-0.1, cols)
            ax1.set_ylim(-0.1, rows)
            ax1.set_aspect('equal')

        ax1.axis('off')
        ax1.set_title('Synesthetic Color Field: "' + text[:50] + ('...' if len(text) > 50 else '') + '"',
                     fontsize=16, fontweight='bold', pad=20)

        # Color distribution bar chart
        ax2 = fig.add_subplot(gs[1, :])
        dominant = analysis_data.get('dominant_colors', [])

        if dominant:
            colors = [d['color'] for d in dominant]
            percentages = [d['percentage'] for d in dominant]
            counts = [d['count'] for d in dominant]

            bars = ax2.barh(range(len(colors)), percentages, color=colors,
                           edgecolor='black', linewidth=1, height=0.6)

            ax2.set_yticks(range(len(colors)))
            ax2.set_yticklabels([c + ' (' + str(cnt) + ')' for c, cnt in zip(colors, counts)],
                               fontsize=10)
            ax2.set_xlabel('Percentage of Text (%)', fontsize=12)
            ax2.set_title('Color Distribution', fontsize=14, fontweight='bold')
            ax2.set_xlim(0, max(percentages) * 1.2 if percentages else 10)

            for i, (bar, pct) in enumerate(zip(bars, percentages)):
                ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                        str(round(pct, 1)) + '%', va='center', fontsize=10)
        else:
            ax2.text(0.5, 0.5, 'No color data', ha='center', va='center', fontsize=14)
            ax2.axis('off')

        # Statistics panel
        ax3 = fig.add_subplot(gs[2, :])
        ax3.axis('off')

        profile = analysis_data.get('profile', 'Standard')
        total_chars = analysis_data.get('total_chars', 0)
        unique_colors = analysis_data.get('unique_colors', 0)

        stats_text = 'Profile: ' + profile + '    |    Total Characters: ' + str(total_chars) + '    |    Unique Colors: ' + str(unique_colors)
        if dominant:
            stats_text += '    |    Dominant: ' + dominant[0]['color'] + ' (' + str(round(dominant[0]['percentage'], 1)) + '%)'

        ax3.text(0.5, 0.5, stats_text, ha='center', va='center',
                fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

        return self._save_and_encode(fig, filename)

    def create_spatial_visualization(self, spatial_data, filename='spatial_map.png'):
        """Create 3D spatial visualization of number/month sequences."""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        positions = spatial_data['positions']
        sequence = spatial_data['sequence']

        if not positions:
            ax.text2D(0.5, 0.5, 'No spatial data', ha='center', va='center', fontsize=16)
        else:
            x = np.array([p['x'] for p in positions])
            y = np.array([p['y'] for p in positions])
            z = np.array([p['z'] for p in positions])

            colors = plt.cm.viridis(np.linspace(0, 1, len(positions)))

            for i, (xi, yi, zi, item) in enumerate(zip(x, y, z, sequence)):
                ax.scatter(xi, yi, zi, c=[colors[i]], s=300, alpha=0.8,
                          edgecolors='black', linewidth=2, depthshade=True)
                ax.text(xi, yi, zi, '  ' + item, fontsize=12, fontweight='bold')

            if len(x) > 1:
                ax.plot(x, y, z, 'k--', alpha=0.3, linewidth=2)

            for i in range(len(x) - 1):
                dx = x[i+1] - x[i]
                dy = y[i+1] - y[i]
                dz = z[i+1] - z[i]
                ax.quiver(x[i], y[i], z[i], dx, dy, dz,
                         length=0.8, normalize=True, alpha=0.4, color='gray')

            ax.set_xlabel('X Position', fontsize=11)
            ax.set_ylabel('Y Position', fontsize=11)
            ax.set_zlabel('Z Position', fontsize=11)
            ax.set_title('Spatial Sequence Map: ' + str(sequence), 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)

        return self._save_and_encode(fig, filename)

    def create_simple_audio_chart(self, audio_data, filename='audio_simple.png'):
        """Simple bar chart fallback for audio visualization."""
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))

        spectrum = audio_data['spectrum']

        if not spectrum:
            axes[0].text(0.5, 0.5, 'No audio data', ha='center', va='center', fontsize=16)
            axes[0].axis('off')
            return self._save_and_encode(fig, filename)

        # Simple bar chart of frequencies
        freqs = [s['frequency'] for s in spectrum]
        amps = [s['amplitude'] for s in spectrum]
        colors = [s['color'] for s in spectrum]

        # Downsample for readability
        step = max(1, len(freqs) // 50)
        freqs_sample = freqs[::step]
        amps_sample = amps[::step]
        colors_sample = colors[::step]

        axes[0].bar(range(len(freqs_sample)), amps_sample, color=colors_sample, alpha=0.8)
        axes[0].set_xlabel('Frequency Sample')
        axes[0].set_ylabel('Amplitude')
        axes[0].set_title('Audio Frequency Spectrum (Bar Chart)', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)

        # Dominant colors pie chart
        dominant = audio_data.get('dominant_colors', [])
        if dominant:
            pie_colors = [d['color'] for d in dominant]
            pie_values = [d['energy'] for d in dominant]
            axes[1].pie(pie_values, labels=[f'Range {i+1}' for i in range(len(dominant))], 
                       colors=pie_colors, autopct='%1.1f%%')
            axes[1].set_title('Dominant Color Regions', fontsize=12)
        else:
            axes[1].text(0.5, 0.5, 'No dominant colors', ha='center', va='center')
            axes[1].axis('off')

        plt.tight_layout()
        return self._save_and_encode(fig, filename)

    def create_audio_visualization(self, audio_data, filename='audio_visual.png'):
        """Create audio spectrum visualization with synesthetic colors."""
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.3)

        spectrum = audio_data['spectrum']

        if not spectrum:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No audio data available', ha='center', va='center',
                   fontsize=16)
            ax.axis('off')
            return self._save_and_encode(fig, filename)

        freqs = np.array([s['frequency'] for s in spectrum])
        amps = np.array([s['amplitude'] for s in spectrum])
        colors = [s['color'] for s in spectrum]

        # Main spectrum plot
        ax1 = fig.add_subplot(gs[0, :])

        for i in range(len(freqs) - 1):
            ax1.fill_between([freqs[i], freqs[i+1]],
                           [amps[i], amps[i+1]],
                           color=colors[i], alpha=0.7, edgecolor='none')

        ax1.plot(freqs, amps, 'k-', linewidth=1, alpha=0.5)

        ax1.set_xlabel('Frequency (Hz)', fontsize=12)
        ax1.set_ylabel('Amplitude', fontsize=12)
        ax1.set_title('Audio Frequency Spectrum with Synesthetic Colors',
                     fontsize=14, fontweight='bold')
        ax1.set_xlim(20, 20000)
        ax1.set_xscale('log')
        ax1.grid(True, alpha=0.3)

        range_labels = [
            (40, 'Sub-bass'),
            (150, 'Bass'),
            (375, 'Low Mids'),
            (1250, 'Mids'),
            (3000, 'High Mids'),
            (5000, 'Presence'),
            (10000, 'Brilliance')
        ]

        for freq, label in range_labels:
            ax1.axvline(x=freq, color='gray', linestyle='--', alpha=0.3)
            ax1.text(freq, ax1.get_ylim()[1] * 0.9, label, rotation=90,
                    fontsize=8, ha='right', va='top', alpha=0.7)

        # Dominant colors pie chart
        ax2 = fig.add_subplot(gs[1, 0])
        dominant = audio_data.get('dominant_colors', [])

        if dominant:
            pie_colors = [d['color'] for d in dominant]
            pie_values = [d['energy'] for d in dominant]
            labels = ['Range ' + str(i+1) for i in range(len(dominant))]

            wedges, texts, autotexts = ax2.pie(
                pie_values, labels=labels, colors=pie_colors,
                autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 9}
            )
            ax2.set_title('Dominant Color Regions', fontsize=12, fontweight='bold')
        else:
            ax2.text(0.5, 0.5, 'No dominant colors', ha='center', va='center')
            ax2.axis('off')

        # Frequency statistics
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.axis('off')

        peak_freq = audio_data.get('peak_frequency', 0)
        total_energy = audio_data.get('total_energy', 0)

        stats = 'Peak Frequency: ' + str(round(peak_freq, 1)) + ' Hz\n'
        stats += 'Total Energy: ' + str(round(total_energy, 2)) + '\n'
        stats += 'Data Points: ' + str(len(spectrum)) + '\n'
        stats += 'Frequency Range: ' + str(round(freqs.min(), 1)) + ' - ' + str(round(freqs.max(), 1)) + ' Hz'

        ax3.text(0.5, 0.5, stats, ha='center', va='center', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

        # Color legend by frequency range
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')

        legend_items = [
            ('#2C3E50', 'Sub-bass (20-60 Hz)'),
            ('#8E44AD', 'Bass (60-250 Hz)'),
            ('#3498DB', 'Low Mids (250-500 Hz)'),
            ('#2ECC71', 'Mids (500-2000 Hz)'),
            ('#F1C40F', 'High Mids (2000-4000 Hz)'),
            ('#E67E22', 'Presence (4000-6000 Hz)'),
            ('#E74C3C', 'Brilliance (6000-20000 Hz)')
        ]

        for i, (color, label) in enumerate(legend_items):
            x_pos = (i % 4) * 0.25
            y_pos = 0.7 - (i // 4) * 0.5

            rect = patches.Rectangle((x_pos, y_pos), 0.03, 0.15, 
                           facecolor=color, edgecolor='black')
            ax4.add_patch(rect)
            ax4.text(x_pos + 0.04, y_pos + 0.075, label, fontsize=9, va='center')

        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)

        return self._save_and_encode(fig, filename)

    def create_consistency_chart(self, consistency_data, filename='consistency.png'):
        """Create consistency analysis chart."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        score = consistency_data.get('consistency_score', 0)
        char_scores = consistency_data.get('character_scores', {})

        # Overall score gauge
        ax1 = axes[0]
        theta = np.linspace(0, np.pi, 100)

        ax1.fill_between(np.cos(theta), np.sin(theta), 0, alpha=0.1, color='gray')

        score_theta = theta[:int(score)] if score > 0 else []
        if len(score_theta) > 0:
            color = '#2ECC71' if score > 80 else '#F1C40F' if score > 50 else '#E74C3C'
            ax1.fill_between(np.cos(score_theta), np.sin(score_theta), 0,
                           alpha=0.7, color=color)

        ax1.text(0, 0.3, str(round(score, 1)) + '%', ha='center', va='center',
                fontsize=36, fontweight='bold')
        ax1.text(0, -0.1, 'Consistency Score', ha='center', va='center',
                fontsize=12)

        is_syn = consistency_data.get('is_synesthete', False)
        status_color = '#2ECC71' if is_syn else '#E74C3C'
        status_text = 'LIKELY SYNESTHETE' if is_syn else 'NOT CONSISTENT'
        ax1.text(0, -0.3, status_text, ha='center', va='center',
                fontsize=14, fontweight='bold', color=status_color,
                bbox=dict(boxstyle='round', facecolor='white', edgecolor=status_color))

        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-0.5, 1.2)
        ax1.set_aspect('equal')
        ax1.axis('off')

        # Character breakdown
        ax2 = axes[1]

        if char_scores:
            chars = list(char_scores.keys())[:20]
            scores = [char_scores[c] for c in chars]
            bar_colors = ['#2ECC71' if s > 80 else '#F1C40F' if s > 50 else '#E74C3C' 
                     for s in scores]

            bars = ax2.barh(range(len(chars)), scores, color=bar_colors,
                           edgecolor='black', linewidth=0.5)
            ax2.set_yticks(range(len(chars)))
            ax2.set_yticklabels(chars)
            ax2.set_xlabel('Consistency (%)', fontsize=11)
            ax2.set_title('Per-Character Consistency', fontsize=12, fontweight='bold')
            ax2.set_xlim(0, 105)
            ax2.axvline(x=80, color='green', linestyle='--', alpha=0.5, label='Synesthete threshold')
            ax2.legend(fontsize=9)

            for bar, score_val in zip(bars, scores):
                ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                        str(int(score_val)) + '%', va='center', fontsize=8)
        else:
            ax2.text(0.5, 0.5, 'No character data', ha='center', va='center')
            ax2.axis('off')

        plt.tight_layout()

        return self._save_and_encode(fig, filename)

    def cleanup_old_files(self, max_files=50):
        """Remove oldest generated files to prevent storage bloat."""
        if len(self.generated_files) > max_files:
            old_files = self.generated_files[:-max_files]
            for f in old_files:
                if os.path.exists(f):
                    os.remove(f)
            self.generated_files = self.generated_files[-max_files:]
