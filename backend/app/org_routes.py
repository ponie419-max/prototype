import sqlite3
from flask import request, jsonify, session

def init_org_routes(app):

    @app.route('/api/organizations', methods=['POST'])
    def create_organization():
        # In a real-world scenario, you'd want to protect this route,
        # possibly making it accessible only to a Super Admin.
        data = request.get_json()
        name = data.get('name')

        if not name:
            return jsonify({'message': 'Organization name is required'}), 400

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO organizations (name) VALUES (?)', (name,))
            org_id = c.lastrowid
            conn.commit()
            conn.close()
            return jsonify({'message': 'Organization created successfully!', 'organization_id': org_id}), 201
        except sqlite3.IntegrityError:
            return jsonify({'message': 'Organization name already exists'}), 400

    @app.route('/api/teams', methods=['POST'])
    def create_team():
        if not session.get('is_admin'): # For now, we'll assume Org Admins are the ones creating teams
            return jsonify({'message': 'Unauthorized: Admins only'}), 403

        data = request.get_json()
        name = data.get('name')
        organization_id = data.get('organization_id')

        if not name or not organization_id:
            return jsonify({'message': 'Team name and organization ID are required'}), 400

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO teams (name, organization_id) VALUES (?, ?)', (name, organization_id))
        team_id = c.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Team created successfully!', 'team_id': team_id}), 201

    @app.route('/api/teams/<int:team_id>/members', methods=['POST'])
    def add_team_member(team_id):
        if not session.get('is_admin'):
            return jsonify({'message': 'Unauthorized: Admins only'}), 403

        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({'message': 'User ID is required'}), 400

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO team_members (user_id, team_id) VALUES (?, ?)', (user_id, team_id))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'message': 'User is already in this team'}), 400
        finally:
            conn.close()

        return jsonify({'message': 'User added to team successfully!'}), 201
