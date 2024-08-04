import sqlite3

def insert_topics():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    topics = [
        # II Year
        ('II year', None, 'Numbers and Percentage', None, 0),
        ('II year', None, 'Calendar & Blood Relation', None, 0),
        ('II year', None, 'Personality Development, Self Awareness & Physical Wellbeing', None, 0),
        ('II year', None, 'Spelling, Spotting Grammatical Error & Preposition', None, 0),
        ('II year', None, 'Clocks and Ages', None, 0),
        ('II year', None, 'C & C++ Basics', None, 0),
        ('II year', None, 'Evaluation and Supervising (At the end of Odd Semester)', None, 0),
        
        # III Year
        ('III year', None, 'Trigonometry, Algebra & Partnership', None, 0),
        ('III year', None, 'Leadership Skills, Team Work, Adaptability & Problem Solving Skills', None, 0),
        ('III year', None, 'Arranging Jumbled Sentence, Direct and Indirect Speech, Cloze Passage, Connectors & Verbal Analog', None, 0),
        ('III year', None, 'Divisibility Rules and Crypt Arithmetic', None, 0),
        ('III year', None, 'Analogy, Alpha Numeric Series, Mixtures and Allegations', None, 0),
        ('III year', 1, 'CSE/ AI&DS/ IT/ ECE/EEE (Array, String, Functions Looping)', None, 0),
        ('III year', 2, 'CIVIL/ MECH (Basics of Auto CAD)', None, 0),
        ('III year', None, 'Evaluation and Supervising (At the end of Odd Semester)', None, 0),
        
        # IV Year Forenoon
        ('IV year', None, 'Profit & Loss, Probability', 'forenoon', 0),
        ('IV year', None, 'Spotting Errors, Synonyms and Antonyms', 'forenoon', 0),
        ('IV year', None, 'Time, Speed, Distance & Work', 'forenoon', 0),
        ('IV year', None, 'Blood Relation', 'forenoon', 0),
        ('IV year', None, 'Average and Permutation', 'forenoon', 0),
        ('IV year', None, 'Sentence Correction, Active & Passive Voice', 'forenoon', 0),
        ('IV year', None, 'Coding and Decoding, Data Interpretation', 'forenoon', 0),
        ('IV year', None, 'Tenses', 'forenoon', 0),
        ('IV year', None, 'Ratio and Proportion, Geometry', 'forenoon', 0),
        ('IV year', None, 'Critical Thinking & Sentence Completion', 'forenoon', 0),
        ('IV year', None, 'Mensuration & Logarithms', 'forenoon', 0),
        ('IV year', None, 'Seating Arrangements, Critical Reasoning', 'forenoon', 0),
        ('IV year', None, 'Series', 'forenoon', 0),
        ('IV year', None, 'Selecting Words, Sentence Pattern & Ordering of Words', 'forenoon', 0),
        ('IV year', None, 'Syllogism, Calendar & Clock', 'forenoon', 0),
        ('IV year', None, 'Cubes and Dices', 'forenoon', 0),
        ('IV year', None, 'Direction, Distance & Puzzle', 'forenoon', 0),
        ('IV year', None, 'Venn Diagram, Data Sufficiency', 'forenoon', 0),
        ('IV year', None, 'Verbal Reasoning, Cause & Effect', 'forenoon', 0),
        ('IV year', None, 'Modifiers', 'forenoon', 0),
        ('IV year', None, 'Evaluation and Supervising (At the end of Odd Semester)', 'forenoon', 0),
        
        # IV Year Afternoon
        ('IV year', 1, 'Basic Programming Skills (6 Hrs)', 'afternoon', 0),
        ('IV year', 1, 'Data Structures (3 Hrs)', 'afternoon', 0),
        ('IV year', 1, 'OOPS Concept (Inheritance, Class, Polymorphism, Constructor, Destructor, Friend Function) (6 hrs)', 'afternoon', 0),
        ('IV year', 1, 'Algorithms (Sorting/ Searching) (6 hrs)', 'afternoon', 0),
        ('IV year', 2, 'Basic Programming Skills (6 Hrs)', 'afternoon', 0),
        ('IV year', 2, 'Data Structures (3 Hrs)', 'afternoon', 0),
        ('IV year', 2, 'OOPS Concept (Inheritance, Class, Polymorphism, Constructor, Destructor, Friend Function) (6 hrs)', 'afternoon', 0),
        ('IV year', 2, 'Algorithms (Sorting/ Searching) (6 hrs)', 'afternoon', 0),
        ('IV year', 3, 'Structural Architecture & STAAD Pro (6 Hrs)', 'afternoon', 0),
        ('IV year', 3, 'Revit Architecture (6 hrs)', 'afternoon', 0),
        ('IV year', 3, 'Advanced Auto CAD (6 hrs)', 'afternoon', 0),
        ('IV year', 3, 'Fundamental on REBAR Analysis (3 Hrs)', 'afternoon', 0),
        ('IV year', 4, 'CIM (6 Hrs)', 'afternoon', 0),
        ('IV year', 4, 'Metrology & Inspection (3 hrs)', 'afternoon', 0),
        ('IV year', 4, 'Fundamentals of Auto CAD (Engineering Drawing) (6 hrs)', 'afternoon', 0),
        ('IV year', 4, 'Robotics and Automation (3 hrs)', 'afternoon', 0),
        ('IV year', 4, 'Machine Design (3 Hrs)', 'afternoon', 0),
    ]
    
    # Insert topics into the database
