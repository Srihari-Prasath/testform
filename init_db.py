import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    
    # Drop the existing topics table if it exists to avoid schema conflicts
    conn.execute('DROP TABLE IF EXISTS topics')
    conn.execute('DROP TABLE IF EXISTS departments')

    # Create the departments table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create the topics table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year TEXT NOT NULL,
            department_id INTEGER,
            topic TEXT NOT NULL,
            session TEXT,
            selected BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    ''')

    departments = ["CSE", "IT", "AI&DS", "ECE", "EEE", "MECH", "CIVIL"]
    for dept in departments:
        conn.execute('INSERT INTO departments (name) VALUES (?)', (dept,))

    topics_data = {
        "II year": [
            ("Numbers and Percentage", None),
            ("Calendar & Blood Relation", None),
            ("Personality development, Self Awareness & Physical Wellbeing", None),
            ("Spelling, Spotting Grammatical Error & Preposition", None),
            ("Clocks and Ages", None),
            ("C & C++ Basics", None),
            ("Evaluation and Supervising (At the end of Odd Semester)", None)
        ],
        "III year": [
            ("Trigonometry, Algebra & Partnership", None),
            ("Leadership Skills, Team Work, adaptability & Problem Solving Skills.", None),
            ("Arranging Jumbled Sentence, Direct and Indirect Speech, Cloze Passage, Connectors & Verbal Analog", None),
            ("Divisibility rules and Crypt Arithmetic.", None),
            ("Analogy, Alpha numeric series, Mixtures and Allegations", None),
            ("Evaluation and Supervising (At the end of Odd Semester)", None),
            ("Array, String, Functions Looping", ["CSE", "IT", "AI&DS", "ECE", "EEE"]),
            ("Basics of Auto CAD", ["MECH", "CIVIL"])
        ],
        "IV year": {
            "forenoon": [
                ("Profit & Loss ,Probability", None),
                ("Spotting Errors ,Synonyms and Antonyms", None),
                ("Time, Speed, Distance & Work", None),
                ("Blood Relation", None),
                ("Average and Permutation", None),
                ("Sentence Correction, Active & Passive Voice", None),
                ("Coding and Decoding, Data Interpretation", None),
                ("Tenses", None),
                ("Ratio and Proportion ,Geometry", None),
                ("Critical Thinking & Sentence Completion", None),
                ("Mensuration & Logarithms", None),
                ("Seating Arrangements ,Critical Reasoning", None),
                ("Series", None),
                ("Selecting Words, Sentence Pattern & Ordering of Words", None),
                ("Syllogism ,Calendar & Clock", None),
                ("Cubes and Dices", None),
                ("Direction, Distance & Puzzle", None),
                ("Venn Diagram ,Data Sufficiency", None),
                ("Verbal Reasoning ,Cause & Effect", None),
                ("Modifiers", None),
                ("Evaluation and Supervising (At the end of Odd Semester)", None)
            ],
            "afternoon": {
                "CSE": [
                    ("Basic Programming Skills (6 Hrs)", None),
                    ("Data Structures (3 Hrs)", None),
                    ("OOPS concept (Inheritance, Class, Polymorphism, Constructor, Destructor, Friend Function)- (6hrs)", None),
                    ("Algorithms (Sorting/ Searching) (6hrs)", None)
                ],
                "ECE": [
                    ("Basic Programming Skills (6 Hrs)", None),
                    ("Data Structures (3 Hrs)", None),
                    ("OOPS concept (Inheritance, Class, Polymorphism, Constructor, Destructor, Friend Function)- (6hrs)", None),
                    ("Algorithms (Sorting/ Searching) (6hrs)", None)
                ],
                "EEE": [
                    ("Basic Programming Skills (6 Hrs)", None),
                    ("Data Structures (3 Hrs)", None),
                    ("OOPS concept (Inheritance, Class, Polymorphism, Constructor, Destructor, Friend Function)- (6hrs)", None),
                    ("Algorithms (Sorting/ Searching) (6hrs)", None)
                ],
                "CIVIL": [
                    ("Structural Architecture & STAAD Pro (6 Hrs)", None),
                    ("Revit Architecture (6 hrs)", None),
                    ("Advanced Auto CAD (6hrs)", None),
                    ("Fundamental on REBAR Analysis (3Hrs)", None)
                ],
                "MECH": [
                    ("CIM (6 Hrs)", None),
                    ("Metrology & Inspection (3hrs)", None),
                    ("Fundamentals of Auto CAD (Engineering Drawing) (6hrs)", None),
                    ("Robotics and Automation  (3hrs)", None),
                    ("Machine Design (3 Hrs)", None)
                ]
            }
        }
    }

    for year, topics in topics_data.items():
        if year == "IV year":
            for session, topics_list in topics.items():
                if session == "afternoon":
                    for dept, special_topics in topics_list.items():
                        dept_id = conn.execute('SELECT id FROM departments WHERE name = ?', (dept,)).fetchone()[0]
                        for topic, _ in special_topics:
                            conn.execute('INSERT INTO topics (year, department_id, topic, session, selected) VALUES (?, ?, ?, ?, ?)', (year, dept_id, topic, session, 0))
                else:
                    for topic, _ in topics_list:
                        conn.execute('INSERT INTO topics (year, topic, session, selected) VALUES (?, ?, ?, ?)', (year, topic, session, 0))
        else:
            for topic, dept_list in topics:
                if dept_list is None:
                    conn.execute('INSERT INTO topics (year, topic, selected) VALUES (?, ?, ?)', (year, topic, 0))
                else:
                    for dept in dept_list:
                        dept_id = conn.execute('SELECT id FROM departments WHERE name = ?', (dept,)).fetchone()[0]
                        conn.execute('INSERT INTO topics (year, department_id, topic, selected) VALUES (?, ?, ?, ?)', (year, dept_id, topic, 0))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
