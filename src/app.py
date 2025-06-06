"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#get para obtener todos los members almacenados.
@app.route('/members', methods=['GET'])
def handle_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

#2º get para obtener un member segun su ID de forma individual y error en cado de no encontrarlo.
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

#POST para poder añadir nuevos members y error en caso de no encontrarlo.
@app.route('/members', methods=['POST'])
def add_member():
    try:
        member = request.get_json()
        if not member:
            return jsonify({"error": "Invalid JSON"}), 400
        required_fields = ["first_name", "age", "lucky_numbers"]
        if not all(field in member for field in required_fields):
            return jsonify({"error": "Missing fields"}), 400

        new_member = jackson_family.add_member(member)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#DELETE para poder ubicar y borrar un member, encaso de no ubicarlo, error.
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

        

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
