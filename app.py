from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
        forenoon_topics = conn.execute('SELECT * FROM topics WHERE year = ? AND session = "forenoon" AND selected = 0 AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?))', (year, department)).fetchall()
        afternoon_topics = conn.execute('SELECT * FROM topics WHERE year = ? AND session = "afternoon" AND selected = 0 AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?))', (year, department)).fetchall()
        conn.close()
        return render_template('iv_year.html', year=year, forenoon_topics=forenoon_topics, afternoon_topics=afternoon_topics)
    else:
        topics = conn.execute('SELECT * FROM topics WHERE year = ? AND (department_id IS NULL OR department_id = (SELECT id FROM departments WHERE name = ?)) AND selected = 0', (year, department)).fetchall()
        conn.close()
        return render_template('topics.html', year=year, topics=topics)

@app.route('/form/<int:topic_id>', methods=['GET', 'POST'])
def form(topic_id):
    if request.method == 'POST':
        # Handle form submission (You can add form fields and processing here)
        conn = get_db_connection()
        conn.execute('UPDATE topics SET selected = 1 WHERE id = ?', (topic_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    topic = conn.execute('SELECT * FROM topics WHERE id = ?', (topic_id,)).fetchone()
    conn.close()
    return render_template('form.html', topic=topic)

@app.route('/reset', methods=['POST'])
def reset():
    conn = get_db_connection()
    conn.execute('UPDATE topics SET selected = 0')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
