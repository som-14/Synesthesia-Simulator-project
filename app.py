"""
app.py - Synesthesia Experience Simulator
Person 4: Flask, Web Interface, Routing
Main application that connects all modules.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import os
import json
import uuid
from datetime import datetime

# Import from other team members
from engine import SynestheticMapping, AudioColorMapper, SpatialMapper, ConsistencyTester
from visualizer import SynestheticVisualizer
from data_manager import SessionManager, ConsistencyTracker

app = Flask(__name__)
app.secret_key = 'synesthesia-simulator-secret-key-2026'

# Initialize components (OOP instantiation)
visualizer = SynestheticVisualizer(output_dir='static/generated')
session_manager = SessionManager(base_dir='user_data')
consistency_tracker = ConsistencyTracker(session_manager)

# Store active user profiles in memory
user_profiles = {}


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - introduces the project."""
    stats = session_manager.get_usage_statistics()
    return render_template('index.html', stats=stats)


@app.route('/text', methods=['GET', 'POST'])
def text_visualizer():
    """
    Text visualization route.
    GET: Show form
    POST: Process text and show visualization
    """
    if request.method == 'POST':
        text = request.form.get('text', '')
        profile = request.form.get('profile', 'standard')
        user_id = request.form.get('user_id', 'anonymous')

        if not text.strip():
            flash('Please enter some text!', 'error')
            return redirect(url_for('text_visualizer'))

        # Use engine.py (Person 1)
        mapping = SynestheticMapping(profile=profile)
        analysis = mapping.analyze_text(text)

        # Use visualizer.py (Person 2)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'text_{user_id}_{timestamp}.png'
        result = visualizer.create_text_visualization(analysis, text, filename)

        # Use data_manager.py (Person 3)
        session_manager.save_session(user_id, 'text_analysis', {
            'text': text,
            'profile': profile,
            'analysis': analysis,
            'image': result['filename']
        })

        return render_template('results.html',
                             result_type='text',
                             text=text,
                             image_path=result['base64'],
                             filename=result['filename'],
                             analysis=analysis,
                             profile=profile)

    # GET request - show form
    profiles = ['standard', 'nabokov', 'messiaen', 'warm', 'cool']
    return render_template('text.html', profiles=profiles)


@app.route('/audio', methods=['GET', 'POST'])
def audio_visualizer():
    """
    Audio visualization route.
    Uses generated sample audio (no file upload needed for demo).
    """
    if request.method == 'POST':
        user_id = request.form.get('user_id', 'anonymous')

        # Use engine.py (Person 1) - generate sample audio
        audio_mapper = AudioColorMapper()
        freqs, amps = audio_mapper.generate_sample_audio(duration=2.0)

        # Analyze with engine
        analysis = audio_mapper.analyze_frequencies(freqs, amps)

        # Use visualizer.py (Person 2) - try new method first, fallback to simple
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'audio_{user_id}_{timestamp}.png'

        try:
            result = visualizer.create_audio_visualization(analysis, filename)
        except Exception as e:
            # Fallback to simple bar chart if fill_between fails
            result = visualizer.create_simple_audio_chart(analysis, filename)

        # Use data_manager.py (Person 3)
        session_manager.save_session(user_id, 'audio_analysis', {
            'peak_frequency': analysis['peak_frequency'],
            'total_energy': analysis['total_energy'],
            'image': result['filename']
        })

        return render_template('results.html',
                             result_type='audio',
                             image_path=result['base64'],
                             filename=result['filename'],
                             analysis=analysis)

    return render_template('audio.html')


@app.route('/spatial', methods=['GET', 'POST'])
def spatial_visualizer():
    """
    Spatial sequence visualization.
    Maps numbers or months to 3D positions.
    """
    if request.method == 'POST':
        sequence_type = request.form.get('sequence_type', 'numbers')
        sequence_input = request.form.get('sequence', '')
        user_id = request.form.get('user_id', 'anonymous')

        if not sequence_input.strip():
            flash('Please enter a sequence!', 'error')
            return redirect(url_for('spatial_visualizer'))

        # Parse sequence
        if sequence_type == 'numbers':
            sequence = [c for c in sequence_input if c.isdigit()]
        else:
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                     'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            sequence = [m.capitalize() for m in sequence_input.lower().split() 
                       if m in months]

        if not sequence:
            flash('No valid items found in sequence!', 'error')
            return redirect(url_for('spatial_visualizer'))

        # Use engine.py (Person 1)
        mapper = SpatialMapper()
        analysis = mapper.analyze_sequence(sequence)

        # Use visualizer.py (Person 2)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'spatial_{user_id}_{timestamp}.png'
        result = visualizer.create_spatial_visualization(analysis, filename)

        # Use data_manager.py (Person 3)
        session_manager.save_session(user_id, 'spatial_analysis', {
            'sequence': sequence,
            'sequence_type': sequence_type,
            'positions': analysis['positions'],
            'image': result['filename']
        })

        return render_template('results.html',
                             result_type='spatial',
                             image_path=result['base64'],
                             filename=result['filename'],
                             analysis=analysis,
                             sequence=sequence)

    return render_template('spatial.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile_builder():
    """
    Profile builder - users create custom color mappings.
    Also used for consistency testing.
    """
    if request.method == 'POST':
        user_id = request.form.get('user_id', 'anonymous')
        action = request.form.get('action', 'save')

        # Extract color mappings from form
        mappings = {}
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
            color = request.form.get(f'color_{char}', '')
            if color:
                mappings[char] = color

        if action == 'save':
            # Save profile
            session_manager.save_user_profile(user_id, {
                'mappings': mappings,
                'created': datetime.now().isoformat()
            })

            # Also record for consistency testing
            consistency_tracker.record_test(user_id, mappings)

            flash('Profile saved successfully!', 'success')
            return redirect(url_for('profile_builder', user_id=user_id))

        elif action == 'test':
            # Run consistency test
            consistency_tracker.record_test(user_id, mappings)
            result = consistency_tracker.analyze_consistency(user_id)

            # Generate consistency chart
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'consistency_{user_id}_{timestamp}.png'
            chart = visualizer.create_consistency_chart(result, filename)

            return render_template('results.html',
                                 result_type='consistency',
                                 image_path=chart['base64'],
                                 filename=chart['filename'],
                                 analysis=result)

    # GET request
    user_id = request.args.get('user_id', 'anonymous')
    profile = session_manager.load_user_profile(user_id)

    # Default colors
    default_mapping = SynestheticMapping('standard').mappings
    current_mapping = profile.get('mappings', default_mapping) if profile else default_mapping

    return render_template('profile.html',
                         user_id=user_id,
                         mappings=current_mapping,
                         characters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


@app.route('/export/<export_type>/<filename>')
def export_file(export_type, filename):
    """
    Export route - download CSV or TXT files.
    Demonstrates File Handling with downloads.
    """
    if export_type == 'csv':
        filepath = os.path.join('user_data/exports', filename)
    elif export_type == 'txt':
        filepath = os.path.join('user_data/exports', filename)
    else:
        flash('Invalid export type!', 'error')
        return redirect(url_for('index'))

    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('File not found!', 'error')
        return redirect(url_for('index'))


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """
    API endpoint for AJAX requests.
    Returns JSON with analysis results.
    """
    data = request.get_json()
    text = data.get('text', '')
    profile = data.get('profile', 'standard')

    mapping = SynestheticMapping(profile=profile)
    analysis = mapping.analyze_text(text)

    return jsonify({
        'success': True,
        'total_chars': analysis['total_chars'],
        'unique_colors': analysis['unique_colors'],
        'dominant_colors': analysis['dominant_colors'],
        'profile': analysis['profile']
    })


@app.route('/sessions/<user_id>')
def user_sessions(user_id):
    """View all sessions for a user."""
    sessions = session_manager.get_user_sessions(user_id)
    return render_template('results.html',
                         result_type='sessions',
                         sessions=sessions,
                         user_id=user_id)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error='Something went wrong'), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('static/generated', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)

    print("=" * 50)
    print("SYNESTHESIA EXPERIENCE SIMULATOR")
    print("=" * 50)
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5000)
