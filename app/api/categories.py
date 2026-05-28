from flask import jsonify, request
from app import db
from app.models import Category
from app.api import api
from app.api.errors import bad_request

# 1. READ ALL (GET)
@api.route('/categories/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({
        'categories': [category.to_json() for category in categories]
    }), 200

# 2. READ ONE (GET)
@api.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_json()), 200

# 3. CREATE (POST)
@api.route('/categories/', methods=['POST'])
def new_category():
    json_data = request.get_json() or {}
    if 'name' not in json_data:
        return bad_request('Category name is missing.')
    
    if Category.query.filter_by(name=json_data['name']).first():
        return bad_request('Category name already exists.')
        
    category = Category.from_json(json_data)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_json()), 201

# 4. UPDATE (PUT)
@api.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    json_data = request.get_json() or {}
    
    if 'name' not in json_data:
        return bad_request('Category name is missing.')
        
    existing = Category.query.filter_by(name=json_data['name']).first()
    if existing and existing.id != id:
        return bad_request('Category name already exists.')
        
    category.name = json_data['name']
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_json()), 200

# 5. DELETE (DELETE)
@api.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted successfully.'}), 200