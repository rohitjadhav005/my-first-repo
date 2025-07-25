from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, status FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    status = request.form['status']
    if title and status:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, status) VALUES (?, ?)', (title, status))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_task(id):
    title = request.form['title']
    status = request.form['status']
    if title and status:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET title = ?, status = ? WHERE id = ?', (title, status, id))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)