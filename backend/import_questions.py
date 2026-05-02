"""
Script to import questions from PDF files into the database.
This script reads sample question data and populates the database with exams, subjects, topics, and questions.
"""

import json
from database import Database
import os

# Sample data structure for questions
SAMPLE_DATA = {
    "exams": [
        {
            "id": 1,
            "name": "JEE",
            "description": "Joint Entrance Examination for Engineering"
        },
        {
            "id": 2,
            "name": "NEET",
            "description": "National Eligibility cum Entrance Test for Medical"
        },
        {
            "id": 3,
            "name": "UPSC",
            "description": "Union Public Service Commission Civil Services"
        }
    ],
    "subjects": {
        1: [  # JEE
            {"id": 1, "name": "Mathematics", "description": "Mathematics for JEE"},
            {"id": 2, "name": "Physics", "description": "Physics for JEE"},
            {"id": 3, "name": "Chemistry", "description": "Chemistry for JEE"}
        ],
        2: [  # NEET
            {"id": 4, "name": "Biology", "description": "Biology for NEET"},
            {"id": 5, "name": "Chemistry", "description": "Chemistry for NEET"},
            {"id": 6, "name": "Physics", "description": "Physics for NEET"}
        ],
        3: [  # UPSC
            {"id": 7, "name": "English", "description": "English for UPSC"},
            {"id": 8, "name": "History", "description": "History for UPSC"},
            {"id": 9, "name": "Geography", "description": "Geography for UPSC"}
        ]
    },
    "topics": {
        1: [  # Mathematics
            {"id": 1, "name": "Algebra"},
            {"id": 2, "name": "Trigonometry"},
            {"id": 3, "name": "Calculus"}
        ],
        4: [  # Biology
            {"id": 4, "name": "Botany"},
            {"id": 5, "name": "Zoology"},
            {"id": 6, "name": "Genetics"}
        ],
        7: [  # English
            {"id": 7, "name": "Grammar"},
            {"id": 8, "name": "Comprehension"},
            {"id": 9, "name": "Vocabulary"}
        ]
    }
}

# Sample questions for demonstration
SAMPLE_QUESTIONS = [
    {
        "topic_id": 1,
        "subject_id": 1,
        "exam_id": 1,
        "question_text": "Solve: 2x + 5 = 13",
        "question_type": "mcq",
        "difficulty_level": "easy",
        "options": [
            {"text": "x = 4", "correct": True},
            {"text": "x = 5", "correct": False},
            {"text": "x = 3", "correct": False},
            {"text": "x = 2", "correct": False}
        ]
    },
    {
        "topic_id": 1,
        "subject_id": 1,
        "exam_id": 1,
        "question_text": "What is the value of sin(90°)?",
        "question_type": "mcq",
        "difficulty_level": "easy",
        "options": [
            {"text": "0", "correct": False},
            {"text": "1", "correct": True},
            {"text": "-1", "correct": False},
            {"text": "undefined", "correct": False}
        ]
    },
    {
        "topic_id": 7,
        "subject_id": 7,
        "exam_id": 3,
        "question_text": "Fill in the blank: She is ____ taller than her brother.",
        "question_type": "mcq",
        "difficulty_level": "medium",
        "options": [
            {"text": "much", "correct": True},
            {"text": "many", "correct": False},
            {"text": "a lot of", "correct": False},
            {"text": "very much", "correct": False}
        ]
    },
    {
        "topic_id": 8,
        "subject_id": 7,
        "exam_id": 3,
        "question_text": "What does 'obsolete' mean?",
        "question_type": "mcq",
        "difficulty_level": "medium",
        "options": [
            {"text": "Old and no longer used", "correct": True},
            {"text": "Very new", "correct": False},
            {"text": "Common", "correct": False},
            {"text": "Valuable", "correct": False}
        ]
    }
]

class QuestionImporter:
    def __init__(self):
        self.db = Database()
    
    def setup_database(self):
        """Initialize database schema"""
        print("Setting up database schema...")
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        self.db.connect()
        self.db.execute_script(schema_path)
        self.db.disconnect()
        print("Database schema initialized successfully!")
    
    def import_exams(self):
        """Import exams into database"""
        print("\nImporting exams...")
        self.db.connect()
        
        for exam in SAMPLE_DATA["exams"]:
            query = "INSERT INTO exams (name, description) VALUES (%s, %s) ON CONFLICT DO NOTHING"
            self.db.execute_insert(query, (exam["name"], exam["description"]))
        
        self.db.disconnect()
        print(f"Imported {len(SAMPLE_DATA['exams'])} exams")
    
    def import_subjects(self):
        """Import subjects into database"""
        print("\nImporting subjects...")
        self.db.connect()
        
        total = 0
        for exam_id, subjects in SAMPLE_DATA["subjects"].items():
            for subject in subjects:
                query = "INSERT INTO subjects (name, exam_id, description) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
                self.db.execute_insert(query, (subject["name"], exam_id, subject["description"]))
                total += 1
        
        self.db.disconnect()
        print(f"Imported {total} subjects")
    
    def import_topics(self):
        """Import topics into database"""
        print("\nImporting topics...")
        self.db.connect()
        
        total = 0
        for subject_id, topics in SAMPLE_DATA["topics"].items():
            for topic in topics:
                query = "INSERT INTO topics (name, subject_id, description) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
                self.db.execute_insert(query, (topic["name"], subject_id, topic["description"]))
                total += 1
        
        self.db.disconnect()
        print(f"Imported {total} topics")
    
    def import_questions(self):
        """Import sample questions into database"""
        print("\nImporting sample questions...")
        self.db.connect()
        
        for q in SAMPLE_QUESTIONS:
            # Insert question
            query = """
            INSERT INTO questions (topic_id, subject_id, exam_id, question_text, question_type, difficulty_level)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """
            params = (q["topic_id"], q["subject_id"], q["exam_id"], q["question_text"], q["question_type"], q["difficulty_level"])
            result = self.db.execute_single(query, params)
            
            if result:
                question_id = result['id']
                
                # Insert options if MCQ
                if q["question_type"] == "mcq" and "options" in q:
                    for option in q["options"]:
                        option_query = "INSERT INTO options (question_id, option_text, is_correct) VALUES (%s, %s, %s)"
                        self.db.execute_insert(option_query, (question_id, option["text"], option["correct"]))
        
        self.db.disconnect()
        print(f"Imported {len(SAMPLE_QUESTIONS)} sample questions")
    
    def run(self):
        """Run the full import process"""
        print("=" * 50)
        print("Question Bank Data Importer")
        print("=" * 50)
        
        try:
            # Step 1: Setup database
            self.setup_database()
            
            # Step 2: Import base data
            self.import_exams()
            self.import_subjects()
            self.import_topics()
            
            # Step 3: Import questions
            self.import_questions()
            
            print("\n" + "=" * 50)
            print("Import completed successfully!")
            print("=" * 50)
            
        except Exception as e:
            print(f"\nError during import: {e}")
            raise

if __name__ == "__main__":
    importer = QuestionImporter()
    importer.run()
