import io
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Create database connection
def get_db_connection():
    try:
        conn = sqlite3.connect('data.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics', methods=['POST'])
def topics():
    year = request.form.get('year')
    department = request.form.get('department')
    
    conn = get_db_connection()
    if not conn:
        flash('Failed to connect to the database.')
        return redirect(url_for('index'))

    if year == 'IV year':
        # Fetch forenoon topics
        forenoon_topics = conn.execute('''
            SELECT * FROM topics
            WHERE year = ? AND session = "forenoon" AND selected = 0 AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?))
        ''', (year, department)).fetchall()
        
        # Fetch afternoon topics with special condition for MECH department
        if department == 'MECH':
            afternoon_topics = conn.execute('''
                SELECT * FROM topics
                WHERE year = ? AND session = "afternoon" AND selected = 0 AND (department_id IS NULL OR department_id = 2)
            ''', (year,)).fetchall()
        else:
            afternoon_topics = conn.execute('''
                SELECT * FROM topics
                WHERE year = ? AND session = "afternoon" AND selected = 0 AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?))
            ''', (year, department)).fetchall()

        conn.close()
        return render_template('iv_year_topics.html', year=year, forenoon_topics=forenoon_topics, afternoon_topics=afternoon_topics)

    elif year == 'III year':
        if department in ['CSE', 'AI&DS', 'IT', 'ECE', 'EEE']:
            # Show all topics for III year and exclude department_id = 2
            topics = conn.execute('''
                SELECT * FROM topics
                WHERE year = ? AND (department_id IS NULL OR department_id != 2) AND selected = 0
            ''', (year,)).fetchall()
        
        elif department in ['CIVIL', 'MECH']:
            # Show all topics for III year and exclude department_id = 1
            topics = conn.execute('''
                SELECT * FROM topics
                WHERE year = ? AND (department_id IS NULL OR department_id != 1) AND selected = 0
            ''', (year,)).fetchall()
        
        else:
            # Handle unexpected department cases or default logic for III year
            topics = conn.execute('''
                SELECT * FROM topics
                WHERE year = ? AND selected = 0
            ''', (year,)).fetchall()
    
    else:
        # For other years, show topics based on the year
        topics = conn.execute('''
            SELECT * FROM topics
            WHERE year = ? AND selected = 0
        ''', (year,)).fetchall()

    conn.close()
    return render_template('topics.html', year=year, topics=topics)


@app.route('/form/<int:topic_id>', methods=['GET', 'POST'])
def form(topic_id):
    conn = get_db_connection()
    if conn is None:
        flash('Failed to connect to the database.')
        return redirect(url_for('index'))

    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    if topic is None:
        conn.close()
        return "Topic not found", 404
    
    if topic['selected']:
        conn.close()
        return redirect(url_for('success_page'))

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        qualification = request.form['qualification']
        experience_nscet = request.form['experience_nscet']
        total_experience = request.form['total_experience']
        
        # Check if the email already exists for the same year
        existing_entry = conn.execute('SELECT * FROM faculty_details WHERE email = ? AND year = ?', (email, topic['year'])).fetchone()
        if existing_entry:
            flash('You have already applied for a topic in this year with this email address.')
            conn.close()
            return redirect(url_for('form', topic_id=topic_id))
        
        # Mark the topic as selected
        conn.execute('UPDATE topics SET selected = 1 WHERE id = ?', (topic_id,))
        conn.commit()
        
        # Save the data to the database
        conn.execute('INSERT INTO faculty_details (email, name, designation, qualification, experience_nscet, total_experience, year, department, topic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (email, name, designation, qualification, experience_nscet, total_experience, topic['year'], topic['department_id'], topic['topic']))
        conn.commit()
        conn.close()
        
        return redirect(url_for('success_page'))

    conn.close()
    return render_template('form.html', topic=topic)

@app.route('/iv_year_form', methods=['GET', 'POST'])
def iv_year_form():
    if request.method == 'POST':
        forenoon_topic = request.form['forenoon_topic']
        afternoon_topic = request.form['afternoon_topic']
        email = request.form['email']
        name = request.form['name']
        designation = request.form['designation']
        qualification = request.form['qualification']
        experience_nscet = request.form['experience_nscet']
        total_experience = request.form['total_experience']

        # Debugging: Print out the form data
        print(f"Form data: {forenoon_topic}, {afternoon_topic}, {email}, {name}, {designation}, {qualification}, {experience_nscet}, {total_experience}")

        conn = get_db_connection()
        if conn is None:
            print("Database connection failed")
            flash('Failed to connect to the database.')
            return redirect(url_for('iv_year_form'))
        
        try:
            conn.execute('INSERT INTO iv_year_data (forenoon_topic, afternoon_topic, email, name, designation, qualification, experience_nscet, total_experience) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                         (forenoon_topic, afternoon_topic, email, name, designation, qualification, experience_nscet, total_experience))
            conn.commit()
            flash('IV Year data saved successfully!')
        except Exception as e:
            print(f"Error: {e}")
            flash('Failed to save data to the database.')
        finally:
            conn.close()

        return redirect(url_for('success_page'))
    
    return render_template('iv_year_form.html')

@app.route('/success')
def success_page():
    return render_template('success.html')

def export_to_excel(year):
    conn = get_db_connection()
    if conn is None:
        flash('Failed to connect to the database.')
        return None
    
    if year == 'IV year':
        df = pd.read_sql_query('SELECT * FROM iv_year_data', conn)
    else:
        df = pd.read_sql_query('SELECT * FROM faculty_details WHERE year = ?', conn, params=(year,))
    
    conn.close()
    
    # Create an in-memory output file for the new workbook
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    
    # Set the file pointer to the beginning of the stream
    output.seek(0)
    
    return output

@app.route('/download/<year>', methods=['GET'])
def download(year):
    output = export_to_excel(year)
    if output:
        return send_file(output, attachment_filename=f'{year}.xlsx', as_attachment=True)
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    conn = get_db_connection()
    if conn is None:
        flash('Failed to connect to the database.')
        return redirect(url_for('index'))
    
    conn.execute('UPDATE topics SET selected = 0')
    conn.commit()
    conn.close()
    flash('Data has been reset.')
    return redirect(url_for('index'))

@app.route('/reset_excel', methods=['POST'])
def reset_excel():
    conn = get_db_connection()
    if conn is None:
        flash('Failed to connect to the database.')
        return redirect(url_for('index'))
    
    conn.execute('DELETE FROM faculty_details')
    conn.commit()
    conn.close()
    flash('Excel data has been reset.')
    return redirect(url_for('index'))

@app.route('/excel', methods=['GET'])
def excel():
    return render_template('excel.html')

if __name__ == '__main__':
    app.run(debug=True)
