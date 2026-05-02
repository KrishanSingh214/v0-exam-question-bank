#!/usr/bin/env python3
"""
Seed demo data for quick testing
Run: python scripts/seed_demo_data.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
from models import Base, Exam, Subject, Topic, Question, User
from routes.auth import hash_password

def seed_data():
    """Seed the database with demo data"""
    print("[v0] Seeding demo data...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Exam).first():
            print("[v0] Database already has data. Skipping seed.")
            return
        
        # Create demo user
        demo_user = User(
            username="demo",
            email="demo@example.com",
            password_hash=hash_password("demo123"),
            full_name="Demo User",
            exam_interest="JEE Main",
            subjects_of_interest="Physics, Chemistry, Mathematics"
        )
        db.add(demo_user)
        db.commit()
        print("[v0] ✓ Created demo user (username: demo, password: demo123)")
        
        # Create Exams
        jee = Exam(name="JEE Main", description="Joint Entrance Examination Main")
        neet = Exam(name="NEET", description="National Eligibility cum Entrance Test")
        db.add_all([jee, neet])
        db.commit()
        print("[v0] ✓ Created exams: JEE Main, NEET")
        
        # Create Subjects for JEE
        physics = Subject(exam_id=jee.id, name="Physics", description="Physics concepts and problems")
        chemistry = Subject(exam_id=jee.id, name="Chemistry", description="Chemistry concepts and problems")
        maths = Subject(exam_id=jee.id, name="Mathematics", description="Mathematics concepts and problems")
        db.add_all([physics, chemistry, maths])
        db.commit()
        print("[v0] ✓ Created subjects: Physics, Chemistry, Mathematics")
        
        # Create Topics for Physics
        mechanics = Topic(subject_id=physics.id, name="Mechanics", description="Motion, Forces, Energy")
        optics = Topic(subject_id=physics.id, name="Optics", description="Light, Reflection, Refraction")
        waves = Topic(subject_id=physics.id, name="Waves", description="Sound, Light Waves")
        db.add_all([mechanics, optics, waves])
        db.commit()
        print("[v0] ✓ Created topics: Mechanics, Optics, Waves")
        
        # Create sample questions
        questions_data = [
            # Mechanics
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": mechanics.id,
                "question_text": "A car accelerates from rest at 2 m/s². What is its velocity after 5 seconds?",
                "option_a": "5 m/s",
                "option_b": "10 m/s",
                "option_c": "25 m/s",
                "option_d": "50 m/s",
                "correct_answer": "B",
                "difficulty_level": "easy",
                "explanation": "Using v = u + at, where u=0, a=2, t=5: v = 0 + 2×5 = 10 m/s"
            },
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": mechanics.id,
                "question_text": "What is the SI unit of force?",
                "option_a": "Dyne",
                "option_b": "Newton",
                "option_c": "Erg",
                "option_d": "Joule",
                "correct_answer": "B",
                "difficulty_level": "easy",
                "explanation": "Newton (N) is the SI unit of force. 1 N = 1 kg⋅m/s²"
            },
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": mechanics.id,
                "question_text": "A projectile is launched at 45° with initial velocity 20 m/s. Find max height (g=10 m/s²)",
                "option_a": "5 m",
                "option_b": "10 m",
                "option_c": "20 m",
                "option_d": "25 m",
                "correct_answer": "B",
                "difficulty_level": "medium",
                "explanation": "At 45°, h_max = (v₀²sin²θ)/(2g) = (400 × 0.5)/(20) = 10 m"
            },
            
            # Optics
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": optics.id,
                "question_text": "What is the speed of light in vacuum?",
                "option_a": "2 × 10⁸ m/s",
                "option_b": "3 × 10⁸ m/s",
                "option_c": "4 × 10⁸ m/s",
                "option_d": "5 × 10⁸ m/s",
                "correct_answer": "B",
                "difficulty_level": "easy",
                "explanation": "The speed of light in vacuum is approximately 3 × 10⁸ m/s or 3 × 10⁵ km/s"
            },
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": optics.id,
                "question_text": "What is the refractive index of water?",
                "option_a": "1.0",
                "option_b": "1.33",
                "option_c": "1.5",
                "option_d": "2.0",
                "correct_answer": "B",
                "difficulty_level": "easy",
                "explanation": "The refractive index of water is approximately 1.33 at room temperature"
            },
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": optics.id,
                "question_text": "A light ray enters glass (n=1.5) from air at 30°. Find refraction angle.",
                "option_a": "15°",
                "option_b": "19.5°",
                "option_c": "25°",
                "option_d": "30°",
                "correct_answer": "B",
                "difficulty_level": "medium",
                "explanation": "Using Snell's law: sin(30°) = 1.5 × sin(θ), θ ≈ 19.5°"
            },
            
            # Waves
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": waves.id,
                "question_text": "What is the frequency of a wave with wavelength 2m and speed 40 m/s?",
                "option_a": "10 Hz",
                "option_b": "20 Hz",
                "option_c": "40 Hz",
                "option_d": "80 Hz",
                "correct_answer": "B",
                "difficulty_level": "easy",
                "explanation": "f = v/λ = 40/2 = 20 Hz"
            },
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": waves.id,
                "question_text": "The period of a wave is 0.5s. What is its frequency?",
                "option_a": "0.5 Hz",
                "option_b": "1 Hz",
                "option_c": "2 Hz",
                "option_d": "0.25 Hz",
                "correct_answer": "C",
                "difficulty_level": "easy",
                "explanation": "f = 1/T = 1/0.5 = 2 Hz"
            },
            {
                "exam_id": jee.id,
                "subject_id": physics.id,
                "topic_id": waves.id,
                "question_text": "Two sound waves have frequencies 256 Hz and 260 Hz. Beat frequency is?",
                "option_a": "4 Hz",
                "option_b": "8 Hz",
                "option_c": "16 Hz",
                "option_d": "516 Hz",
                "correct_answer": "A",
                "difficulty_level": "medium",
                "explanation": "Beat frequency = |f₁ - f₂| = |256 - 260| = 4 Hz"
            },
        ]
        
        for q_data in questions_data:
            q = Question(**q_data)
            db.add(q)
        
        db.commit()
        print(f"[v0] ✓ Created {len(questions_data)} sample questions")
        
        print("[v0] ✅ Demo data seeding completed successfully!")
        print("[v0] You can now login with:")
        print("[v0]   Username: demo")
        print("[v0]   Password: demo123")
        
    except Exception as e:
        print(f"[v0] ❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
