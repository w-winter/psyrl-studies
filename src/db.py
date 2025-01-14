import sqlite3
from typing import Dict, List, Optional

class Database:
    def __init__(self, db_path: str = "studies.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS studies (
                    id INTEGER PRIMARY KEY,
                    post_title TEXT,
                    project_name TEXT,
                    research_theme TEXT,
                    location_map TEXT,
                    location_text TEXT,
                    research_type TEXT,
                    phd_project TEXT,
                    recruiting BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def get_existing_ids(self) -> List[int]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT id FROM studies")
            return [row[0] for row in cursor.fetchall()]

    def insert_study(self, study: Dict) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO studies (
                    id, post_title, project_name, research_theme,
                    location_map, location_text, research_type,
                    phd_project, recruiting
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                int(study['ID']),
                study['post_title'],
                study.get('atlas-research_project_name'),
                study.get('atlas-summary_research_theme'),
                study.get('atlas-location_map'),
                study.get('atlas-location_text'),
                study.get('atlas-type_of_research'),
                study.get('atlas-name_of_phd_project'),
                study.get('recruiting', False)
            ))
            conn.commit()

    def get_study(self, study_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM studies WHERE id = ?",
                (study_id,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
