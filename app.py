import io
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

# Create database connection
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topics', methods=['POST'])
def topics():
    year = request.form.get('year')
    department = request.form.get('department')
    
    conn = get_db_connection()
    
    if year == 'IV year':
        forenoon_topics = conn.execute('''
            SELECT * FROM topics
            WHERE year = ? AND session = "forenoon" AND selected = 0 AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?))
        ''', (year, department)).fetchall()
        afternoon_topics = conn.execute('''
            SELECT * FROM topics
            WHERE year = ? AND session = "afternoon" AND selected = 0 AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?))
        ''', (year, department)).fetchall()
        conn.close()
        return render_template('iv_year.html', year=year, forenoon_topics=forenoon_topics, afternoon_topics=afternoon_topics)
    else:
        topics = conn.execute('''
            SELECT * FROM topics
            WHERE year = ? AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?)) AND selected = 0
        ''', (year, department)).fetchall()
        conn.close()
        return render_template('topics.html', year=year, topics=topics)

@app.route('/form/<int:topic_id>', methods=['GET', 'POST'])
def form(topic_id):
    conn = get_db_connection()
    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()

    if topic is None:
        return "Topic not found", 404
    
    if topic['selected']:
        return redirect(url_for('success_page'))  # Redirect if already processed

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

@app.route('/submit_topic_selection', methods=['POST'])
def submit_topic_selection():
    forenoon_topic_id = request.form.get('forenoon_topic')
    afternoon_topic_id = request.form.get('afternoon_topic')
    
    conn = get_db_connection()
    if forenoon_topic_id:
        conn.execute('UPDATE topics SET selected = 1 WHERE id = ?', (forenoon_topic_id,))
    if afternoon_topic_id:
        conn.execute('UPDATE topics SET selected = 1 WHERE id = ?', (afternoon_topic_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('success_page'))

@app.route('/submit_faculty_details', methods=['POST'])
def submit_faculty_details():
    email = request.form.get('email')
    name = request.form.get('name')
    designation = request.form.get('designation')
    qualification = request.form.get('qualification')
    experience_nscet = request.form.get('experience_nscet')
    total_experience = request.form.get('total_experience')
    year = request.form.get('year')
    department = request.form.get('department')
    topic = request.form.get('forenoon_topic')  # Assuming you're using forenoon_topic

    conn = get_db_connection()
    
    conn.execute('''
    INSERT INTO faculty_details (email, name, designation, qualification, experience_nscet, total_experience, year, department, topic)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (email, name, designation, qualification, experience_nscet, total_experience, year, department, topic))

    conn.commit()
    conn.close()

    return redirect(url_for('success_page'))

@app.route('/success')
def success_page():
    return render_template('success.html')

def export_to_excel(year):
    conn = get_db_connection()
    
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

@app.route('/export_excel')
def export_excel():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Adjust query if necessary
    cursor.execute('SELECT * FROM faculty_details')
    rows = cursor.fetchall()

    conn.close()
    
    # Use pandas to export to Excel
    df = pd.DataFrame(rows, columns=['id', 'email', 'name', 'designation', 'qualification', 'experience_nscet', 'total_experience', 'year', 'department', 'topic'])
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    
    return send_file(output, attachment_filename='faculty_details.xlsx', as_attachment=True)

@app.route('/download/<year>', methods=['GET'])
def download(year):
    output = export_to_excel(year)
    return send_file(output, attachment_filename=f'{year}.xlsx', as_attachment=True)

@app.route('/iv_year', methods=['POST'])
def iv_year():
    year = request.form.get('year')
    department = request.form.get('department')
    
    conn = get_db_connection()

    # Fetch topics excluding IT and AI&DS departments
    forenoon_topics = conn.execute('''
        SELECT * FROM topics
        WHERE year = ?
          AND session = "forenoon"
          AND selected = 0
          AND (department_id IS NULL
               OR department_id = (SELECT id FROM departments WHERE name = ?))
    ''', (year, department)).fetchall()

    afternoon_topics = conn.execute('''
        SELECT * FROM topics
        WHERE year = ?
          AND session = "afternoon"
          AND selected = 0
          AND (department_id IS NULL
               OR department_id = (SELECT id FROM departments WHERE name = ?))
    ''', (year, department)).fetchall()
    
    # Fetch departments excluding IT and AI&DS
    departments = conn.execute('''
        SELECT * FROM departments
        WHERE name != 'IT' AND name != 'AI&DS'
    ''').fetchall()

    conn.close()
    
    return render_template('iv_year.html', year=year, forenoon_topics=forenoon_topics, afternoon_topics=afternoon_topics, departments=departments)

@app.route('/reset', methods=['POST'])
def reset():
    conn = get_db_connection()
    conn.execute('UPDATE topics SET selected = 0')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/reset_excel', methods=['POST'])
def reset_excel():
    conn = get_db_connection()
    conn.execute('DELETE FROM faculty_details')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/excel', methods=['GET'])
def excel():
    return render_template('excel.html')

if __name__ == '__main__':
    app.run(debug=True)
