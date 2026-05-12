"""
engine.py - Synesthesia Engine
Person 1: Core Logic, OOP, NumPy, Pandas
Converts text/audio/numbers into color data and statistical analysis.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import json


class SynestheticMapping:
    """
    OOP Class: Maps characters to colors based on synesthetic rules.
    Supports multiple famous synesthete profiles.
    """

    def __init__(self, profile: str = "standard"):
        self.profile = profile
        self.mappings = self._load_profile()
        self.history = []  # Track usage for Pandas analysis

    def _load_profile(self) -> Dict[str, str]:
        """Load color mappings based on selected profile."""
        profiles = {
            "standard": self._generate_standard(),
            "nabokov": self._load_nabokov(),
            "messiaen": self._load_messiaen(),
            "warm": self._generate_warm(),
            "cool": self._generate_cool()
        }
        return profiles.get(self.profile, self._generate_standard())

    def _generate_standard(self) -> Dict[str, str]:
        """Generate mathematically consistent color mappings using NumPy."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        np.random.seed(42)  # Reproducible

        # Use NumPy to generate evenly distributed HSV colors
        n = len(chars)
        hues = np.linspace(0, 360, n, endpoint=False)

        colors = {}
        for i, char in enumerate(chars):
            h = hues[i]
            s = 0.8
            v = 0.9
            colors[char] = self._hsv_to_hex(h, s, v)

        return colors

    def _load_nabokov(self) -> Dict[str, str]:
        """Famous author Vladimir Nabokov's actual letter colors."""
        return {
            'A': '#E74C3C', 'B': '#3498DB', 'C': '#F1C40F', 'D': '#E67E22',
            'E': '#9B59B6', 'F': '#1ABC9C', 'G': '#E74C3C', 'H': '#95A5A6',
            'I': '#ECF0F1', 'J': '#F39C12', 'K': '#C0392B', 'L': '#F1C40F',
            'M': '#3498DB', 'N': '#9B59B6', 'O': '#E67E22', 'P': '#2ECC71',
            'Q': '#34495E', 'R': '#E74C3C', 'S': '#F1C40F', 'T': '#3498DB',
            'U': '#9B59B6', 'V': '#E67E22', 'W': '#2C3E50', 'X': '#7F8C8D',
            'Y': '#F1C40F', 'Z': '#2ECC71', '0': '#000000', '1': '#FFFFFF',
            '2': '#E74C3C', '3': '#3498DB', '4': '#F1C40F', '5': '#2ECC71',
            '6': '#9B59B6', '7': '#E67E22', '8': '#1ABC9C', '9': '#E91E63'
        }

    def _load_messiaen(self) -> Dict[str, str]:
        """Composer Olivier Messiaen's musical note colors."""
        return {
            'C': '#E74C3C', 'C#': '#8E44AD', 'D': '#F39C12', 'D#': '#2C3E50',
            'E': '#F1C40F', 'F': '#FFFFFF', 'F#': '#3498DB', 'G': '#E67E22',
            'G#': '#2ECC71', 'A': '#9B59B6', 'A#': '#C0392B', 'B': '#1ABC9C'
        }

    def _generate_warm(self) -> Dict[str, str]:
        """Warm color palette using NumPy."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        np.random.seed(100)
        colors = {}
        for char in chars:
            r = np.random.uniform(0.7, 1.0)
            g = np.random.uniform(0.3, 0.7)
            b = np.random.uniform(0.0, 0.3)
            colors[char] = self._rgb_to_hex(r, g, b)
        return colors

    def _generate_cool(self) -> Dict[str, str]:
        """Cool color palette using NumPy."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        np.random.seed(200)
        colors = {}
        for char in chars:
            r = np.random.uniform(0.0, 0.3)
            g = np.random.uniform(0.3, 0.7)
            b = np.random.uniform(0.7, 1.0)
            colors[char] = self._rgb_to_hex(r, g, b)
        return colors

    def _hsv_to_hex(self, h: float, s: float, v: float) -> str:
        """Convert HSV to hex color using NumPy."""
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _rgb_to_hex(self, r: float, g: float, b: float) -> str:
        """Convert RGB floats to hex."""
        return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

    def get_color(self, char: str) -> str:
        """Get color for a single character."""
        upper = char.upper()
        return self.mappings.get(upper, '#CCCCCC')

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text and return comprehensive data.
        Uses Pandas for statistical analysis.
        """
        results = []
        frequencies = {}

        for char in text:
            if char.isalnum():
                color = self.get_color(char)
                results.append({
                    'character': char,
                    'color': color,
                    'is_space': False
                })
                frequencies[char.upper()] = frequencies.get(char.upper(), 0) + 1
            elif char.isspace():
                results.append({
                    'character': ' ',
                    'color': '#FFFFFF',
                    'is_space': True
                })

        # Create Pandas DataFrame for analysis
        df = pd.DataFrame(results)

        # Statistical analysis with NumPy
        color_counts = df[df['is_space'] == False]['color'].value_counts()
        total_chars = len(df[df['is_space'] == False])

        # NumPy calculations
        percentages = np.array(color_counts.values) / total_chars * 100

        # Dominant colors
        dominant = [
            {'color': color, 'percentage': float(pct), 'count': int(count)}
            for color, count, pct in zip(
                color_counts.index, 
                color_counts.values, 
                percentages
            )
        ]

        # Store in history
        self.history.append({
            'text': text,
            'timestamp': pd.Timestamp.now().isoformat(),
            'total_chars': total_chars,
            'unique_colors': len(color_counts)
        })

        return {
            'characters': results,
            'frequencies': frequencies,
            'dominant_colors': dominant,
            'total_chars': total_chars,
            'unique_colors': len(color_counts),
            'profile': self.profile
        }

    def get_history_df(self) -> pd.DataFrame:
        """Return usage history as Pandas DataFrame."""
        return pd.DataFrame(self.history)


class AudioColorMapper:
    """
    OOP Class: Maps audio frequencies to colors.
    Uses NumPy for signal processing calculations.
    """

    def __init__(self):
        # Frequency ranges (Hz) with corresponding colors
        self.freq_ranges = [
            (20, 60, '#2C3E50', 'Sub-bass'),
            (60, 250, '#8E44AD', 'Bass'),
            (250, 500, '#3498DB', 'Low Mids'),
            (500, 2000, '#2ECC71', 'Mids'),
            (2000, 4000, '#F1C40F', 'High Mids'),
            (4000, 6000, '#E67E22', 'Presence'),
            (6000, 20000, '#E74C3C', 'Brilliance')
        ]

    def frequency_to_color(self, freq: float) -> Tuple[str, str]:
        """Convert frequency to color and label."""
        for low, high, color, label in self.freq_ranges:
            if low <= freq < high:
                return color, label
        return '#95A5A6', 'Unknown'

    def analyze_frequencies(self, frequencies: np.ndarray, 
                           amplitudes: np.ndarray) -> Dict:
        """
        Analyze frequency spectrum using NumPy.
        Returns color-mapped spectrum data.
        """
        # NumPy operations
        total_energy = np.sum(amplitudes)
        max_amp = np.max(amplitudes) if len(amplitudes) > 0 else 1

        spectrum = []
        range_energy = {color: 0.0 for _, _, color, _ in self.freq_ranges}

        for freq, amp in zip(frequencies, amplitudes):
            color, label = self.frequency_to_color(freq)
            intensity = amp / max_amp

            spectrum.append({
                'frequency': float(freq),
                'amplitude': float(amp),
                'color': color,
                'label': label,
                'intensity': float(intensity)
            })

            if color in range_energy:
                range_energy[color] += float(intensity)

        # Sort by energy using NumPy
        colors = list(range_energy.keys())
        energies = np.array(list(range_energy.values()))
        sorted_indices = np.argsort(energies)[::-1]

        dominant = [
            {'color': colors[i], 'energy': float(energies[i])}
            for i in sorted_indices[:3] if float(energies[i]) > 0.001
        ]

        return {
            'spectrum': spectrum,
            'dominant_colors': dominant,
            'total_energy': float(total_energy),
            'peak_frequency': float(frequencies[np.argmax(amplitudes)]) if len(amplitudes) > 0 else 0
        }

    def generate_sample_audio(self, duration: float = 2.0, 
                             sample_rate: int = 44100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate sample audio data using NumPy for demo purposes.
        Creates a chord with multiple frequencies.
        """
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

        # Generate a C-major chord: C4, E4, G4
        freqs = [261.63, 329.63, 392.00]  # Hz

        signal = np.zeros_like(t)
        for freq in freqs:
            signal += 0.3 * np.sin(2 * np.pi * freq * t)

        # Add some harmonics using NumPy
        for freq in freqs:
            signal += 0.1 * np.sin(2 * np.pi * freq * 2 * t)  # 2nd harmonic
            signal += 0.05 * np.sin(2 * np.pi * freq * 3 * t)  # 3rd harmonic

        # Add noise
        signal += 0.02 * np.random.randn(len(t))

        # FFT using NumPy
        fft = np.fft.fft(signal)
        freqs_fft = np.fft.fftfreq(len(signal), 1/sample_rate)

        # Only positive frequencies
        positive_mask = freqs_fft > 0
        freqs_fft = freqs_fft[positive_mask]
        amplitudes = np.abs(fft)[positive_mask]

        # Downsample for visualization
        step = max(1, len(freqs_fft) // 500)
        return freqs_fft[::step], amplitudes[::step]


class SpatialMapper:
    """
    OOP Class: Maps numbers and sequences to 3D spatial positions.
    Uses NumPy for coordinate calculations.
    """

    def __init__(self):
        self.number_positions = self._generate_number_space()
        self.month_positions = self._generate_month_space()

    def _generate_number_space(self) -> Dict[str, Tuple[float, float, float]]:
        """Generate spiral 3D coordinates for numbers 0-9 using NumPy."""
        positions = {}
        angles = np.linspace(0, 4 * np.pi, 10)
        radii = np.linspace(1, 5, 10)
        heights = np.linspace(0, 4, 10)

        for i in range(10):
            x = float(radii[i] * np.cos(angles[i]))
            y = float(radii[i] * np.sin(angles[i]))
            z = float(heights[i])
            positions[str(i)] = (x, y, z)

        return positions

    def _generate_month_space(self) -> Dict[str, Tuple[float, float, float]]:
        """Generate circular layout for months using NumPy."""
        positions = {}
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for i, month in enumerate(months):
            angle = (i / 12) * 2 * np.pi
            x = float(5 * np.cos(angle))
            y = float(5 * np.sin(angle))
            z = float(i * 0.3)
            positions[month] = (x, y, z)

        return positions

    def get_position(self, item: str) -> Tuple[float, float, float]:
        """Get 3D coordinates for a number or month."""
        if item in self.number_positions:
            return self.number_positions[item]
        elif item in self.month_positions:
            return self.month_positions[item]
        return (0.0, 0.0, 0.0)

    def analyze_sequence(self, sequence: List[str]) -> Dict:
        """
        Analyze a sequence and return spatial data.
        Uses NumPy for distance calculations.
        """
        positions = []

        for item in sequence:
            pos = self.get_position(item)
            positions.append({
                'item': item,
                'x': pos[0],
                'y': pos[1],
                'z': pos[2]
            })

        # NumPy distance calculations
        if len(positions) > 1:
            coords = np.array([[p['x'], p['y'], p['z']] for p in positions])
            distances = []

            for i in range(len(coords) - 1):
                dist = float(np.linalg.norm(coords[i+1] - coords[i]))
                distances.append({
                    'from': sequence[i],
                    'to': sequence[i+1],
                    'distance': dist
                })
        else:
            distances = []

        return {
            'positions': positions,
            'distances': distances,
            'sequence': sequence
        }


class ConsistencyTester:
    """
    OOP Class: Tests if someone's color associations are consistent.
    Real synesthetes have 90%+ consistency over time.
    """

    def __init__(self):
        self.tests = []

    def record_test(self, user_id: str, mappings: Dict[str, str]):
        """Record a user's color mappings."""
        import datetime
        self.tests.append({
            'user_id': user_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'mappings': mappings
        })

    def calculate_consistency(self, user_id: str) -> Dict:
        """
        Calculate consistency score using NumPy and Pandas.
        """
        user_tests = [t for t in self.tests if t['user_id'] == user_id]

        if len(user_tests) < 2:
            return {
                'consistency_score': 0.0,
                'tests_count': len(user_tests),
                'is_synesthete': False,
                'message': 'Need at least 2 tests'
            }

        # Extract all characters tested
        all_chars = set()
        for test in user_tests:
            all_chars.update(test['mappings'].keys())

        # Calculate consistency per character
        char_scores = {}

        for char in all_chars:
            colors = []
            for test in user_tests:
                if char in test['mappings']:
                    colors.append(test['mappings'][char])

            if len(colors) > 1:
                # NumPy: percentage of same color across tests
                colors_array = np.array(colors)
                first_color = colors_array[0]
                matches = np.sum(colors_array == first_color)
                char_scores[char] = float(matches / len(colors)) * 100

        # Overall score
        if char_scores:
            scores_array = np.array(list(char_scores.values()))
            overall = float(np.mean(scores_array))
        else:
            overall = 0.0

        # Create Pandas DataFrame for detailed report
        df = pd.DataFrame([
            {'character': k, 'consistency': v}
            for k, v in char_scores.items()
        ])

        return {
            'consistency_score': overall,
            'character_scores': char_scores,
            'tests_count': len(user_tests),
            'is_synesthete': overall > 80,
            'details_df': df.to_dict('records'),
            'message': 'Likely synesthete' if overall > 80 else 'Not consistent enough'
        }
