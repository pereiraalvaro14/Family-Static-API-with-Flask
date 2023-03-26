"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import json
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def saveFavorite():

    data = request.json
    print(data)

    first_name=data['first_name']
    age=int(data['age'])
    lucky_numbers=data['lucky_numbers']

    try:
        id = data['id']
    except:
        print("sdfsdfsdfsdfs")
        id = ''
    
    jackson_family.add_member({
        "first_name": first_name,
        "age": age,
        "lucky_numbers": lucky_numbers,
        "id": id
    })

    response_body = {
        "data": "saved"
    }

    return jsonify(response_body), 200

@app.route('/member/<id>', methods=['GET'])
def get_member(id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(int(id))
    
    return jsonify(member), 200

@app.route('/member/<id>', methods=['DELETE'])
def delete_member(id):

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.delete_member(int(id))
    
    return {"done": True}, 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)