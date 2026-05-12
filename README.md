# 🎨 Synesthesia Experience Simulator

A Flask web application that converts sensory inputs (text, audio, numbers) into visual representations based on documented synesthetic perception patterns.

## 📋 Requirements Met

| Technology | Implementation |
|-----------|----------------|
| **Basic Python** | Core logic, routing, data processing |
| **File Handling** | JSON session storage, CSV/TXT exports, image saving, profile loading |
| **OOP** | 7 classes: SynestheticMapping, AudioColorMapper, SpatialMapper, ConsistencyTester, SynestheticVisualizer, SessionManager, ConsistencyTracker |
| **NumPy** | FFT audio analysis, color calculations, statistical operations, coordinate math |
| **Pandas** | DataFrames for text analysis, session summaries, CSV operations, consistency reports |
| **Matplotlib** | Color-field paintings, 3D spatial maps, audio spectrums, consistency gauge charts |
| **Flask** | Complete web application with routing, templates, form handling |

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt


📁 Project Structure
synesthesia-simulator/
├── app.py                 # Flask routes & web interface
├── engine.py              # Core logic (4 classes)
├── visualizer.py          # Matplotlib charts (1 class)
├── data_manager.py        # File handling & sessions (2 classes)
├── requirements.txt       # Dependencies
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css
│   └── generated/        # Auto-created for images
└── templates/
    ├── base.html
    ├── index.html
    ├── text.html
    ├── audio.html
    ├── spatial.html
    ├── profile.html
    └── results.html

👥 Team Division
| Person       | File                 | Classes                                                                | Technologies                      |
| ------------ | -------------------- | ---------------------------------------------------------------------- | --------------------------------- |
| **Person 1** | `engine.py`          | SynestheticMapping, AudioColorMapper, SpatialMapper, ConsistencyTester | OOP, NumPy, Pandas                |
| **Person 2** | `visualizer.py`      | SynestheticVisualizer                                                  | Matplotlib, NumPy, OOP            |
| **Person 3** | `data_manager.py`    | SessionManager, ConsistencyTracker                                     | File Handling, Pandas, NumPy, OOP |
| **Person 4** | `app.py` + templates | Flask app, 7 HTML templates                                            | Flask, Python, File Handling, OOP |

🎯 Features
1. Text to Color Visualization (/text)
Enter text → see colored blocks for each character
5 profiles: Standard, Nabokov, Messiaen, Warm, Cool
Color distribution statistics
Export as PNG, CSV, TXT
2. Audio to Color Visualization (/audio)
Generate C-major chord with harmonics
FFT frequency analysis using NumPy
Frequency spectrum colored by synesthetic rules
7 frequency ranges mapped to colors
3. Spatial Sequence Mapping (/spatial)
Numbers (0-9) mapped to spiral 3D coordinates
Months (Jan-Dec) mapped to circular 3D layouts
Distance calculations between sequence items
4. Profile Builder & Consistency Test (/profile)
Create custom color-to-letter mappings (A-Z, 0-9)
Save profiles as JSON
Test consistency over multiple sessions
Real synesthetes score 90%+ consistency
Detailed per-character breakdown
🛠️ Technologies Stack
Flask — Web framework
NumPy — Numerical computing, FFT, statistics
Pandas — Data manipulation, CSV exports
Matplotlib — Data visualization, image generation
📝 About Synesthesia
Synesthesia is a neurological condition where senses are "crossed." Approximately 4.4% of the population (1 in 23 people) has some form. Famous synesthetes include Pharrell Williams, Vladimir Nabokov, and Olivier Messiaen.
🤝 Contributing
This is a team project. Each member works on their assigned files.
