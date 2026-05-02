#!/usr/bin/env python
"""
PDF Parser for extracting questions from the provided PDF files.
This script converts PDF questions into CSV format for bulk import.

Supported PDF formats:
- 500-English-Questions-1.pdf & 2.pdf
- 500-Maths-Questions-1.pdf & 2.pdf

Usage:
    python pdf_parser.py <pdf_file_path> <output_csv_path>
    python pdf_parser.py ../data/500-English-Questions-1.pdf ../data/english_questions.csv
"""

import re
import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class QuestionParser:
    """Parser for extracting questions from PDFs in various formats."""
    
    def __init__(self, subject: str = "English"):
        self.subject = subject
        self.questions = []
        
    def parse_english_format(self, text: str) -> List[Dict]:
        """
        Parse English questions in common PDF format.
        Expected format:
        1. Question text here?
        (a) Option A
        (b) Option B
        (c) Option C
        (d) Option D
        Answer: a
        """
        questions = []
        
        # Split by numbered questions
        pattern = r'^(\d+)\.\s+(.+?)(?=\n\(a\))|(?=\n\d+\.)|$'
        matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            question_num = match.group(1)
            question_text = match.group(2).strip()
            
            if not question_text:
                continue
            
            # Extract options
            options_pattern = r'\(([a-d])\)\s+(.+?)(?=\(|^|$)'
            option_matches = re.finditer(options_pattern, question_text, re.MULTILINE)
            
            options = {}
            for opt_match in option_matches:
                letter = opt_match.group(1)
                text = opt_match.group(2).strip()
                options[letter] = text
            
            # Extract answer if present
            answer_match = re.search(r'Answer:\s*([a-d])', text, re.IGNORECASE)
            correct_answer = answer_match.group(1).lower() if answer_match else None
            
            if len(options) >= 2:  # At least 2 options
                questions.append({
                    'number': question_num,
                    'text': question_text.split('(a)')[0].strip(),
                    'options': options,
                    'correct_answer': correct_answer,
                    'difficulty': 'Medium',  # Default, can be adjusted
                    'type': 'Multiple Choice'
                })
        
        return questions
    
    def parse_math_format(self, text: str) -> List[Dict]:
        """Parse Math questions from PDF."""
        questions = []
        
        # Similar pattern for math questions
        pattern = r'^(\d+)\.\s+(.+?)(?=\n\(|(?=\n\d+\.)|$)'
        matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            question_num = match.group(1)
            question_text = match.group(2).strip()
            
            if not question_text:
                continue
            
            # Extract options
            options_pattern = r'\(([A-D]|[a-d])\)\s+(.+?)(?=\(|$)'
            option_matches = re.finditer(options_pattern, question_text)
            
            options = {}
            for opt_match in option_matches:
                letter = opt_match.group(1).lower()
                opt_text = opt_match.group(2).strip()
                options[letter] = opt_text
            
            # Determine difficulty
            if any(keyword in question_text.lower() for keyword in ['complex', 'difficult', 'advanced']):
                difficulty = 'Hard'
            elif any(keyword in question_text.lower() for keyword in ['simple', 'basic', 'easy']):
                difficulty = 'Easy'
            else:
                difficulty = 'Medium'
            
            if len(options) >= 2:
                questions.append({
                    'number': question_num,
                    'text': question_text.split('(')[0].strip() if '(' in question_text else question_text,
                    'options': options,
                    'correct_answer': None,  # Usually not in PDF
                    'difficulty': difficulty,
                    'type': 'Multiple Choice'
                })
        
        return questions
    
    def extract_from_text_file(self, filepath: str) -> List[Dict]:
        """Extract questions from text file (converted from PDF)."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if 'english' in filepath.lower() or self.subject.lower() == 'english':
                return self.parse_english_format(text)
            elif 'math' in filepath.lower() or self.subject.lower() == 'math':
                return self.parse_math_format(text)
            else:
                return self.parse_english_format(text)
        
        except Exception as e:
            print(f"Error parsing file: {e}")
            return []
    
    def to_csv(self, output_path: str, questions: List[Dict]):
        """Convert parsed questions to CSV format."""
        fieldnames = [
            'question_number',
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer',
            'difficulty_level',
            'subject',
            'topic',
            'type'
        ]
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for q in questions:
                    row = {
                        'question_number': q.get('number', ''),
                        'question_text': q.get('text', ''),
                        'option_a': q['options'].get('a', ''),
                        'option_b': q['options'].get('b', ''),
                        'option_c': q['options'].get('c', ''),
                        'option_d': q['options'].get('d', ''),
                        'correct_answer': q.get('correct_answer', ''),
                        'difficulty_level': q.get('difficulty', 'Medium'),
                        'subject': self.subject,
                        'topic': q.get('topic', 'General'),
                        'type': q.get('type', 'Multiple Choice')
                    }
                    writer.writerow(row)
            
            print(f"✓ Exported {len(questions)} questions to {output_path}")
            return True
        
        except Exception as e:
            print(f"✗ Error writing CSV: {e}")
            return False


class PDFToCSVConverter:
    """Convert PDF question files to CSV format for bulk import."""
    
    def __init__(self):
        self.parsers = {
            'english': QuestionParser('English'),
            'math': QuestionParser('Math'),
        }
    
    def convert_english_pdfs(self, pdf_paths: List[str], output_path: str = '../data/english_questions.csv'):
        """Convert English PDF questions to CSV."""
        print(f"\nProcessing English PDFs...")
        all_questions = []
        
        for pdf_path in pdf_paths:
            print(f"  Parsing {Path(pdf_path).name}...")
            parser = self.parsers['english']
            
            # Note: PyPDF2 or pdfplumber would be needed for actual PDF parsing
            # For now, assuming text extraction is done
            questions = parser.extract_from_text_file(pdf_path)
            all_questions.extend(questions)
            print(f"    Found {len(questions)} questions")
        
        parser = self.parsers['english']
        parser.to_csv(output_path, all_questions)
        return all_questions
    
    def convert_math_pdfs(self, pdf_paths: List[str], output_path: str = '../data/math_questions.csv'):
        """Convert Math PDF questions to CSV."""
        print(f"\nProcessing Math PDFs...")
        all_questions = []
        
        for pdf_path in pdf_paths:
            print(f"  Parsing {Path(pdf_path).name}...")
            parser = self.parsers['math']
            questions = parser.extract_from_text_file(pdf_path)
            all_questions.extend(questions)
            print(f"    Found {len(questions)} questions")
        
        parser = self.parsers['math']
        parser.to_csv(output_path, all_questions)
        return all_questions


def manual_import_sample_questions():
    """
    Manually add sample questions to the database.
    This is a fallback for when PDF parsing is not available.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app import Base, QuestionDB, OptionDB, TopicDB
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/question_bank"
    )
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    sample_questions = [
        # English Grammar
        {
            "topic": 1,
            "text": "Which of the following is grammatically correct?",
            "options": [
                ("The team are winning.", False),
                ("The team is winning.", True),
                ("The team have won.", False),
                ("The teams is winning.", False),
            ],
            "difficulty": "Easy"
        },
        # Math Algebra
        {
            "topic": 4,
            "text": "Solve for x: 2x + 3 = 11",
            "options": [
                ("x = 3", False),
                ("x = 4", True),
                ("x = 5", False),
                ("x = 6", False),
            ],
            "difficulty": "Easy"
        },
    ]
    
    for q_data in sample_questions:
        question = QuestionDB(
            topic_id=q_data['topic'],
            question_text=q_data['text'],
            difficulty_level=q_data['difficulty'],
            question_type='Multiple Choice'
        )
        db.add(question)
        db.flush()
        
        for i, (opt_text, is_correct) in enumerate(q_data['options']):
            option = OptionDB(
                question_id=question.id,
                option_text=opt_text,
                option_label=chr(65 + i),
                is_correct=is_correct
            )
            db.add(option)
    
    db.commit()
    print(f"✓ Imported {len(sample_questions)} questions to database")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("PDF to CSV Question Converter")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "questions.csv"
        
        parser = QuestionParser("English" if "english" in pdf_file.lower() else "Math")
        questions = parser.extract_from_text_file(pdf_file)
        parser.to_csv(output_file, questions)
    else:
        print("""
Usage:
    python pdf_parser.py <pdf_file> <output_csv>

Example:
    python pdf_parser.py ../data/500-English-Questions-1.pdf ../data/english_q1.csv
    python pdf_parser.py ../data/500-Maths-Questions-1.pdf ../data/math_q1.csv

Note: This script requires the PDF to be converted to text first.
Convert PDF to text using: pdftotext input.pdf output.txt

Or use PyPDF2:
    pip install PyPDF2
    python -c "import PyPDF2; ..."
        """)
        print("\n✓ Parser is ready for use. Import into your Python code:")
        print("  from pdf_parser import QuestionParser")
        print("  parser = QuestionParser('English')")
        print("  questions = parser.extract_from_text_file('questions.txt')")
        print("  parser.to_csv('output.csv', questions)")
