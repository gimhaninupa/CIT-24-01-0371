from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time

app = Flask(__name__)

# Retrieve database connection parameters from environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'mindflow')

def get_db_connection():
    # Retry database connection in case the service starts up slowly
    retries = 10
    conn = None
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                dbname=DB_NAME
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database connection failed, retrying in 2 seconds... ({retries} retries left)")
            time.sleep(2)
            retries -= 1
    raise Exception("Could not connect to the database after multiple retries.")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create tasks table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    ''')
    # Create notes table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    # Create moods table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id SERIAL PRIMARY KEY,
            mood TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Initialize Database tables
try:
    init_db()
except Exception as e:
    print("Error initializing database:", e)

@app.route('/')
def index():
    return render_template('index.html')

# --- Tasks API ---
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM tasks ORDER BY id DESC;')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO tasks (title, completed) VALUES (%s, %s) RETURNING *;', (title, False))
    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def toggle_task(task_id):
    data = request.json
    completed = data.get('completed')
    if completed is None:
        return jsonify({'error': 'Completed status is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('UPDATE tasks SET completed = %s WHERE id = %s RETURNING *;', (completed, task_id))
    task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s RETURNING id;', (task_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'success': True})

# --- Notes API ---
@app.route('/api/notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM notes ORDER BY created_at DESC;')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO notes (content) VALUES (%s) RETURNING *;', (content,))
    note = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(note), 201

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = %s RETURNING id;', (note_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({'error': 'Note not found'}), 404
    return jsonify({'success': True})

# --- Mood API ---
@app.route('/api/moods', methods=['GET'])
def get_moods():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM moods ORDER BY created_at DESC LIMIT 10;')
    moods = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(moods)

@app.route('/api/moods', methods=['POST'])
def add_mood():
    data = request.json
    mood = data.get('mood')
    if not mood:
        return jsonify({'error': 'Mood label is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('INSERT INTO moods (mood) VALUES (%s) RETURNING *;', (mood,))
    mood_log = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(mood_log), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)