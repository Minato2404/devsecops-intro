import os
import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# KERENTANAN 1: Hardcoded credentials (HIGH)
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

# KERENTANAN 2: SQL Injection (HIGH)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # SQL Injection vulnerability - tidak ada parameterized query
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    return "Login successful" if user else "Login failed"

# KERENTANAN 3: Command Injection (HIGH)
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Command injection - langsung execute user input
    result = os.system(f"ping -c 1 {host}")
    return f"Ping result: {result}"

# KERENTANAN 4: XSS (MEDIUM)
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # XSS vulnerability - tidak ada sanitization
    return render_template_string(f"<h1>Search results for: {query}</h1>")

# KERENTANAN 5: Path Traversal (MEDIUM)
@app.route('/download')
def download():
    filename = request.args.get('file')
    # Path traversal - tidak ada validasi path
    with open(f"/var/www/files/{filename}", 'r') as f:
        return f.read()

# KERENTANAN 6: Weak cryptography (LOW)
import hashlib

def hash_password(password):
    # Menggunakan MD5 yang sudah tidak aman
    return hashlib.md5(password.encode()).hexdigest()

# KERENTANAN 7: Debug mode enabled (MEDIUM)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
Cara Menjalankan Testing
1. Install Security Scanner (Semgrep)
pip install semgrep
2. Scan Aplikasi
# Scan dengan Semgrep
semgrep --config=auto vulnerable_app.py --json > scan_results.json
3. Kirim Hasil ke Workflow
# Kirim hasil scan ke webhook workflow Anda
curl -X POST https://your-n8n-instance.com/webhook/your-webhook-path \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "test-app/vulnerable-python",
    "branch": "main",
    "commit": "abc123",
    "scanner": "semgrep",
    "status": "failed",
    "findings": [
      {
        "severity": "HIGH",
        "title": "Hardcoded credentials detected",
        "description": "API key and database password hardcoded in source code",
        "file": "vulnerable_app.py",
        "line": 9,
        "cwe": "CWE-798"
      },
      {
        "severity": "HIGH",
        "title": "SQL Injection vulnerability",
        "description": "User input directly concatenated into SQL query",
        "file": "vulnerable_app.py",
        "line": 20,
        "cwe": "CWE-89"
      },
      {
        "severity": "HIGH",
        "title": "Command Injection",
        "description": "User input passed to os.system without sanitization",
        "file": "vulnerable_app.py",
        "line": 29,
        "cwe": "CWE-78"
      },
      {
        "severity": "MEDIUM",
        "title": "Cross-Site Scripting (XSS)",
        "description": "User input rendered without escaping",
        "file": "vulnerable_app.py",
        "line": 36,
        "cwe": "CWE-79"
      },
      {
        "severity": "MEDIUM",
        "title": "Path Traversal",
        "description": "File path constructed from user input without validation",
        "file": "vulnerable_app.py",
        "line": 43,
        "cwe": "CWE-22"
      },
      {
        "severity": "LOW",
        "title": "Weak cryptographic hash",
        "description": "MD5 used for password hashing",
        "file": "vulnerable_app.py",
        "line": 51,
        "cwe": "CWE-327"
      }
    ]
  }'
