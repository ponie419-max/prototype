import sqlite3
import bcrypt
from flask import request, jsonify, session

def init_routes(app):
    @app.route('/api/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        organization_id = data.get('organization_id') # Users must join an organization

        if not all([email, password, organization_id]):
            return jsonify({'message': 'Email, password, and organization ID are required'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            # By default, new users are 'employees'. Admins can change this later.
            c.execute('INSERT INTO users (email, password, organization_id, role) VALUES (?, ?, ?, ?)',
                      (email, hashed_password, organization_id, 'employee'))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Signup successful!'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Email already exists'}), 400

    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT id, password, role, organization_id FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
            session['user_id'] = user[0]
            session['email'] = email
            session['role'] = user[2]
            session['organization_id'] = user[3]
            # The 'is_admin' flag is now legacy, but we can set it for compatibility
            # with older parts of the code until they are refactored.
            session['is_admin'] = (user[2] == 'org_admin' or user[2] == 'super_admin')
            
            return jsonify({
                'message': 'Login successful!',
                'role': user[2],
                'organization_id': user[3]
            }), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401

    @app.route('/api/user', methods=['GET'])
    def get_current_user():
        if 'email' in session:
            return jsonify({
                'email': session['email'],
                'is_admin': session.get('is_admin', False)
            })
        else:
            return jsonify({'email': None, 'is_admin': False})

    @app.route('/api/employees', methods=['GET'])
    def get_employees():
        # Optional: you can restrict this route as needed
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM employees")
        employees = c.fetchall()
        conn.close()
        return jsonify(employees), 200

    @app.route('/api/employees', methods=['POST'])
    def add_employee():
        if not session.get('is_admin'):
            return jsonify({'message': 'Unauthorized: Admins only'}), 403

        data = request.get_json()
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        position = data.get('position')
        department = data.get('department')
        phone = data.get('phone')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO employees (first_name, last_name, email, position, department, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, position, department, phone))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Employee added successfully!'}), 201
