"""
data_manager.py - Data Manager
Person 3: File Handling, Pandas, JSON/CSV/TXT operations
Manages user sessions, exports, and consistency tracking.
"""

import json
import os
import pandas as pd
import numpy as np
from datetime import datetime


class SessionManager:
    """Manages user sessions and data persistence."""
    
    def __init__(self, base_dir="user_data"):
        self.base_dir = base_dir
        self.sessions_dir = os.path.join(base_dir, "sessions")
        self.exports_dir = os.path.join(base_dir, "exports")
        self.profiles_dir = os.path.join(base_dir, "profiles")
        
        for dir_path in [self.sessions_dir, self.exports_dir, self.profiles_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def save_session(self, user_id, session_type, data):
        """Save a session to JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{session_type}_{timestamp}.json"
        filepath = os.path.join(self.sessions_dir, filename)
        
        session_record = {
            "user_id": user_id,
            "session_type": session_type,
            "timestamp": timestamp,
            "datetime": datetime.now().isoformat(),
            "data": data
        }
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session_record, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_session(self, filename):
        """Load a session from JSON file."""
        filepath = os.path.join(self.sessions_dir, filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_user_sessions(self, user_id):
        """Get all sessions for a specific user."""
        sessions = []
        if os.path.exists(self.sessions_dir):
            for filename in os.listdir(self.sessions_dir):
                if filename.startswith(user_id) and filename.endswith(".json"):
                    session = self.load_session(filename)
                    if session:
                        sessions.append(session)
        sessions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return sessions
    
    def export_to_csv(self, data, filename=None):
        """Export analysis data to CSV using Pandas."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.csv"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        if "characters" in data:
            df = pd.DataFrame(data["characters"])
        elif "spectrum" in data:
            df = pd.DataFrame(data["spectrum"])
        elif "positions" in data:
            df = pd.DataFrame(data["positions"])
        else:
            df = pd.DataFrame([data])
        
        df.to_csv(filepath, index=False, encoding="utf-8")
        return filepath
    
    def export_to_txt(self, data, user_id="anonymous", filename=None):
        """Generate a formatted text report."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{user_id}_{timestamp}.txt"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        lines = []
        lines.append("=" * 60)
        lines.append("   SYNESTHESIA EXPERIENCE SIMULATOR - ANALYSIS REPORT")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"User ID: {user_id}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        if "profile" in data:
            lines.append(f"Profile Used: {data['profile']}")
            lines.append("")
        
        if "total_chars" in data:
            lines.append(f"Total Characters Analyzed: {data['total_chars']}")
        
        if "unique_colors" in data:
            lines.append(f"Unique Colors Used: {data['unique_colors']}")
            lines.append("")
        
        if "dominant_colors" in data:
            lines.append("-" * 40)
            lines.append("DOMINANT COLORS:")
            lines.append("-" * 40)
            for dc in data["dominant_colors"]:
                lines.append(f"  Color: {dc['color']} - {dc['percentage']:.1f}% ({dc['count']} chars)")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("End of Report")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        return filepath
    
    def save_user_profile(self, user_id, profile_data):
        """Save user's custom color mappings."""
        filepath = os.path.join(self.profiles_dir, f"{user_id}_profile.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2)
        return filepath
    
    def load_user_profile(self, user_id):
        """Load user's custom color mappings."""
        filepath = os.path.join(self.profiles_dir, f"{user_id}_profile.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    
    def get_all_sessions_summary(self):
        """Get summary of all sessions as Pandas DataFrame."""
        records = []
        if os.path.exists(self.sessions_dir):
            for filename in os.listdir(self.sessions_dir):
                if filename.endswith(".json"):
                    session = self.load_session(filename)
                    if session:
                        records.append({
                            "filename": filename,
                            "user_id": session.get("user_id", "unknown"),
                            "session_type": session.get("session_type", "unknown"),
                            "timestamp": session.get("timestamp", ""),
                            "datetime": session.get("datetime", "")
                        })
        return pd.DataFrame(records)
    
    def get_usage_statistics(self):
        """Generate usage statistics using Pandas and NumPy."""
        df = self.get_all_sessions_summary()
        
        if df.empty:
            return {"message": "No sessions found"}
        
        stats = {
            "total_sessions": len(df),
            "unique_users": df["user_id"].nunique(),
            "session_types": df["session_type"].value_counts().to_dict(),
            "most_active_user": df["user_id"].value_counts().index[0] if len(df) > 0 else None
        }
        
        if "datetime" in df.columns and len(df) > 0:
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df["hour"] = df["datetime"].dt.hour
            hourly = df["hour"].value_counts().sort_index()
            stats["peak_hour"] = int(hourly.idxmax()) if not hourly.empty else None
            stats["hourly_distribution"] = hourly.to_dict()
        
        return stats


class ConsistencyTracker:
    """Tracks and analyzes consistency of user mappings."""
    
    def __init__(self, session_manager):
        self.session_manager = session_manager
        self.tests = {}
    
    def record_test(self, user_id, mappings):
        """Record a test session for consistency analysis."""
        if user_id not in self.tests:
            self.tests[user_id] = []
        
        self.tests[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "mappings": mappings
        })
        
        self.session_manager.save_session(user_id, "consistency_test", {
            "mappings": mappings,
            "test_number": len(self.tests[user_id])
        })
    
    def analyze_consistency(self, user_id):
        """Analyze consistency using NumPy and Pandas."""
        if user_id not in self.tests or len(self.tests[user_id]) < 2:
            sessions = self.session_manager.get_user_sessions(user_id)
            consistency_sessions = [s for s in sessions if s.get("session_type") == "consistency_test"]
            
            self.tests[user_id] = [
                {
                    "timestamp": s.get("datetime", ""),
                    "mappings": s.get("data", {}).get("mappings", {})
                }
                for s in consistency_sessions
            ]
        
        tests = self.tests.get(user_id, [])
        
        if len(tests) < 2:
            return {
                "consistency_score": 0.0,
                "tests_count": len(tests),
                "is_synesthete": False,
                "message": "Need at least 2 tests. Take the test again!",
                "character_scores": {}
            }
        
        all_chars = set()
        for test in tests:
            all_chars.update(test["mappings"].keys())
        
        char_scores = {}
        char_data = []
        
        for char in sorted(all_chars):
            colors = []
            for test in tests:
                if char in test["mappings"]:
                    colors.append(test["mappings"][char])
            
            if len(colors) > 1:
                colors_array = np.array(colors)
                first_color = colors_array[0]
                matches = np.sum(colors_array == first_color)
                consistency = float(matches / len(colors)) * 100
                
                char_scores[char] = consistency
                char_data.append({
                    "character": char,
                    "consistency": consistency,
                    "tests": len(colors),
                    "first_color": first_color
                })
        
        if char_scores:
            scores_array = np.array(list(char_scores.values()))
            overall = float(np.mean(scores_array))
            std_dev = float(np.std(scores_array))
        else:
            overall = 0.0
            std_dev = 0.0
        
        df = pd.DataFrame(char_data)
        
        is_synesthete = overall > 80 and std_dev < 20
        
        return {
            "consistency_score": overall,
            "standard_deviation": std_dev,
            "character_scores": char_scores,
            "character_data": char_data,
            "tests_count": len(tests),
            "characters_tested": len(char_scores),
            "is_synesthete": is_synesthete,
            "likelihood": "High" if is_synesthete else "Low",
            "message": "You show strong synesthetic consistency!" if is_synesthete else "Your associations vary. Try testing again in a few days.",
            "details_df": df.to_dict("records") if not df.empty else []
        }
    
    def get_comparison_data(self, user_id):
        """Get all test data for a user as Pandas DataFrame."""
        tests = self.tests.get(user_id, [])
        
        records = []
        for i, test in enumerate(tests):
            for char, color in test["mappings"].items():
                records.append({
                    "test_number": i + 1,
                    "character": char,
                    "color": color,
                    "timestamp": test["timestamp"]
                })
        
        return pd.DataFrame(records)
