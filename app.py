from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Configuration de la connexion à la base de données via variables d'environnement
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'tododb')
DB_USER = os.getenv('DB_USER', 'todouser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'todopass')

def get_db_connection():
    """Établit une connexion à la base de données PostgreSQL"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def init_db():
    """Initialise la base de données avec la table tasks si elle n'existe pas"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/')
def index():
    """Page d'accueil affichant toutes les tâches"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, title, completed FROM tasks ORDER BY created_at DESC')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        return f"Erreur de connexion à la base de données: {e}", 500

@app.route('/add', methods=['POST'])
def add_task():
    """Ajoute une nouvelle tâche"""
    title = request.form.get('title')
    if title:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO tasks (title) VALUES (%s)', (title,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            return f"Erreur lors de l'ajout: {e}", 500
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    """Bascule le statut completed d'une tâche"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tasks SET completed = NOT completed WHERE id = %s', (task_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Erreur lors de la mise à jour: {e}", 500
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Supprime une tâche"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Erreur lors de la suppression: {e}", 500
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Endpoint de healthcheck pour Nomad"""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}, 200
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
