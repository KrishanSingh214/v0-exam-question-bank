"""
Script to parse question PDFs and import them into the database.
Supports parsing from text files with structured format.
"""

import os
import sys
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base, Exam, Subject, Topic, Question
from database import SessionLocal

load_dotenv()

# Database session
db = SessionLocal()

# Sample data structure
EXAMS = [
    {"name": "JEE Mains", "description": "Joint Entrance Examination (Mains)"},
    {"name": "JEE Advanced", "description": "Joint Entrance Examination (Advanced)"},
    {"name": "NEET", "description": "National Eligibility cum Entrance Test"},
    {"name": "UPSC", "description": "Union Public Service Commission"},
]

SUBJECTS = {
    "JEE Mains": [
        {"name": "Mathematics", "description": "Math for JEE"},
        {"name": "Physics", "description": "Physics for JEE"},
        {"name": "Chemistry", "description": "Chemistry for JEE"},
    ],
    "JEE Advanced": [
        {"name": "Mathematics", "description": "Advanced Math"},
        {"name": "Physics", "description": "Advanced Physics"},
        {"name": "Chemistry", "description": "Advanced Chemistry"},
    ],
    "NEET": [
        {"name": "Biology", "description": "Biology for NEET"},
        {"name": "Chemistry", "description": "Chemistry for NEET"},
        {"name": "Physics", "description": "Physics for NEET"},
    ],
}

TOPICS = {
    ("JEE Mains", "Mathematics"): [
        "Quadratic Equations", "Sequences and Series", "Calculus", "Trigonometry",
        "Complex Numbers", "Permutations and Combinations", "Probability"
    ],
    ("JEE Mains", "Physics"): [
        "Mechanics", "Optics", "Electricity", "Magnetism", "Modern Physics",
        "Thermodynamics", "Waves and Sound"
    ],
    ("JEE Mains", "Chemistry"): [
        "Atomic Structure", "Chemical Bonding", "Organic Chemistry", "Inorganic Chemistry",
        "Thermodynamics", "Electrochemistry", "Chemical Equilibrium"
    ],
    ("NEET", "Biology"): [
        "Cell Structure", "Photosynthesis", "Respiration", "Reproduction", 
        "Genetics", "Evolution", "Ecology"
    ],
    ("NEET", "Physics"): [
        "Mechanics", "Thermodynamics", "Waves", "Optics", "Electricity and Magnetism"
    ],
    ("NEET", "Chemistry"): [
        "Atomic Structure", "Bonding", "Organic Reactions", "Periodic Table",
        "Solutions", "Redox Reactions", "Kinetics"
    ],
}

# Sample questions for demonstration
SAMPLE_QUESTIONS = [
    {
        "exam": "JEE Mains",
        "subject": "Mathematics",
        "topic": "Quadratic Equations",
        "question": "If α and β are roots of x² - 5x + 6 = 0, find α + β",
        "options": {
            "A": "5",
            "B": "6",
            "C": "-5",
            "D": "-6"
        },
        "correct": "A",
        "explanation": "By Vieta's formula, sum of roots = -b/a = 5",
        "difficulty": "easy"
    },
    {
        "exam": "JEE Mains",
        "subject": "Physics",
        "topic": "Mechanics",
        "question": "A body is projected vertically upward with velocity 20 m/s. How long does it take to return?",
        "options": {
            "A": "2 seconds",
            "B": "4 seconds",
            "C": "5 seconds",
            "D": "10 seconds"
        },
        "correct": "B",
        "explanation": "Time of flight = 2u/g = 2×20/10 = 4 seconds",
        "difficulty": "easy"
    },
    {
        "exam": "NEET",
        "subject": "Biology",
        "topic": "Cell Structure",
        "question": "Which organelle is responsible for ATP synthesis?",
        "options": {
            "A": "Lysosome",
            "B": "Mitochondria",
            "C": "Golgi apparatus",
            "D": "Endoplasmic reticulum"
        },
        "correct": "B",
        "explanation": "Mitochondria is the powerhouse of the cell, responsible for ATP production",
        "difficulty": "easy"
    },
]

def create_base_structure():
    """Create exams, subjects, and topics"""
    print("Creating base structure (Exams, Subjects, Topics)...")
    
    for exam_data in EXAMS:
        # Check if exam exists
        exam = db.query(Exam).filter(Exam.name == exam_data["name"]).first()
        if not exam:
            exam = Exam(**exam_data)
            db.add(exam)
            db.commit()
            print(f"✓ Created exam: {exam_data['name']}")
        
        # Add subjects
        if exam_data["name"] in SUBJECTS:
            for subject_data in SUBJECTS[exam_data["name"]]:
                subject = db.query(Subject).filter(
                    Subject.name == subject_data["name"],
                    Subject.exam_id == exam.id
                ).first()
                
                if not subject:
                    subject = Subject(exam_id=exam.id, **subject_data)
                    db.add(subject)
                    db.commit()
                    print(f"  ✓ Created subject: {subject_data['name']}")
                
                # Add topics
                key = (exam_data["name"], subject_data["name"])
                if key in TOPICS:
                    for topic_name in TOPICS[key]:
                        topic = db.query(Topic).filter(
                            Topic.name == topic_name,
                            Topic.subject_id == subject.id
                        ).first()
                        
                        if not topic:
                            topic = Topic(
                                subject_id=subject.id,
                                name=topic_name,
                                description=f"{topic_name} for {subject_data['name']}"
                            )
                            db.add(topic)
                            db.commit()
                            print(f"    ✓ Created topic: {topic_name}")

def import_sample_questions():
    """Import sample questions"""
    print("\nImporting sample questions...")
    
    for q_data in SAMPLE_QUESTIONS:
        exam = db.query(Exam).filter(Exam.name == q_data["exam"]).first()
        if not exam:
            print(f"✗ Exam not found: {q_data['exam']}")
            continue
        
        subject = db.query(Subject).filter(
            Subject.name == q_data["subject"],
            Subject.exam_id == exam.id
        ).first()
        if not subject:
            print(f"✗ Subject not found: {q_data['subject']}")
            continue
        
        topic = db.query(Topic).filter(
            Topic.name == q_data["topic"],
            Topic.subject_id == subject.id
        ).first()
        if not topic:
            print(f"✗ Topic not found: {q_data['topic']}")
            continue
        
        # Check if question already exists
        existing = db.query(Question).filter(
            Question.question_text == q_data["question"]
        ).first()
        if existing:
            print(f"~ Skipped duplicate question: {q_data['question'][:50]}...")
            continue
        
        question = Question(
            exam_id=exam.id,
            subject_id=subject.id,
            topic_id=topic.id,
            question_text=q_data["question"],
            option_a=q_data["options"]["A"],
            option_b=q_data["options"]["B"],
            option_c=q_data["options"]["C"],
            option_d=q_data["options"]["D"],
            correct_answer=q_data["correct"],
            explanation=q_data["explanation"],
            difficulty_level=q_data["difficulty"]
        )
        db.add(question)
        db.commit()
        print(f"✓ Added question: {q_data['question'][:50]}...")

def parse_text_file(filepath):
    """Parse questions from a text file"""
    print(f"\nParsing questions from {filepath}...")
    
    questions = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parsing - looks for pattern like:
        # Q. Question text
        # A) Option A
        # B) Option B
        # etc.
        
        # This is a placeholder - actual PDF parsing requires PyPDF2 or similar
        print("  [Note: Manual parsing needed for actual PDF files]")
        print("  Use PyPDF2 or pdfplumber for production PDF parsing")
        
    except Exception as e:
        print(f"  Error reading file: {e}")
    
    return questions

def import_from_csv(filepath):
    """Import questions from CSV file"""
    print(f"\nImporting from CSV: {filepath}...")
    
    try:
        import csv
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            
            for row in reader:
                # Expected columns: exam_id, subject_id, topic_id, question_text, 
                # option_a, option_b, option_c, option_d, correct_answer, 
                # explanation, difficulty_level
                
                try:
                    question = Question(
                        exam_id=int(row['exam_id']),
                        subject_id=int(row['subject_id']),
                        topic_id=int(row['topic_id']),
                        question_text=row['question_text'],
                        option_a=row['option_a'],
                        option_b=row['option_b'],
                        option_c=row['option_c'],
                        option_d=row['option_d'],
                        correct_answer=row['correct_answer'],
                        explanation=row.get('explanation', ''),
                        difficulty_level=row.get('difficulty_level', 'medium')
                    )
                    db.add(question)
                    count += 1
                    
                    if count % 100 == 0:
                        db.commit()
                        print(f"  Imported {count} questions...")
                
                except Exception as e:
                    print(f"  Error importing row: {e}")
                    continue
            
            db.commit()
            print(f"✓ Successfully imported {count} questions from CSV")
    
    except ImportError:
        print("  CSV module not available")
    except Exception as e:
        print(f"  Error: {e}")

def main():
    """Main import function"""
    print("=" * 60)
    print("Question Bank - Data Import Script")
    print("=" * 60)
    
    try:
        # Create base structure
        create_base_structure()
        
        # Import sample questions
        import_sample_questions()
        
        # Check for external files
        csv_file = "questions.csv"
        if os.path.exists(csv_file):
            import_from_csv(csv_file)
        
        # Print summary
        exam_count = db.query(Exam).count()
        subject_count = db.query(Subject).count()
        topic_count = db.query(Topic).count()
        question_count = db.query(Question).count()
        
        print("\n" + "=" * 60)
        print("Import Summary:")
        print(f"  Exams: {exam_count}")
        print(f"  Subjects: {subject_count}")
        print(f"  Topics: {topic_count}")
        print(f"  Questions: {question_count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during import: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
