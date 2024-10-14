from flask import Blueprint, request, jsonify
from models import Project, db

project_bp = Blueprint('project', __name__)

@project_bp.route('', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects])

@project_bp.route('', methods=['POST'])
def create_projects():
    data = request.get_json()
    new_project = Project(name=data['name'], description=data['description'])
    
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify(new_project.to_dict()), 201