from flask import Flask, render_template, request, redirect, url_for, abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    date = request.form['date']

    if task:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (task, date) VALUES (?, ?)', (task, date))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()

    if task is None:
        conn.close()
        abort(404)

    if request.method == 'POST':
        new_task = request.form['task']
        new_date = request.form['date']
        
        conn.execute('UPDATE tasks SET task = ?, date = ? WHERE id = ?',
                     (new_task, new_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', task=task)

if __name__ == '__main__':
    conn = sqlite3.connect('todo.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT
        )
    ''')
    conn.close()

    app.run(debug=True)
