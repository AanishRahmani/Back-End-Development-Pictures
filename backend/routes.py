from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    data = [
        {"id": 1, "url": "https://example.com/pic1", "event_country": "United States", "event_state": "California", "event_city": "Los Angeles", "event_date": "2025-01-01"},
        {"id": 2, "url": "https://example.com/pic2", "event_country": "United States", "event_state": "New York", "event_city": "New York City", "event_date": "2025-01-02"},
        {"id": 3, "url": "https://example.com/pic3", "event_country": "Canada", "event_state": "Ontario", "event_city": "Toronto", "event_date": "2025-01-03"},
        {"id": 4, "url": "https://example.com/pic4", "event_country": "United Kingdom", "event_state": "England", "event_city": "London", "event_date": "2025-01-04"},
        {"id": 5, "url": "https://example.com/pic5", "event_country": "Australia", "event_state": "Victoria", "event_city": "Melbourne", "event_date": "2025-01-05"},
        {"id": 6, "url": "https://example.com/pic6", "event_country": "Germany", "event_state": "Bavaria", "event_city": "Munich", "event_date": "2025-01-06"},
        {"id": 7, "url": "https://example.com/pic7", "event_country": "India", "event_state": "Maharashtra", "event_city": "Mumbai", "event_date": "2025-01-07"},
        {"id": 8, "url": "https://example.com/pic8", "event_country": "Japan", "event_state": "Tokyo", "event_city": "Tokyo", "event_date": "2025-01-08"},
        {"id": 9, "url": "https://example.com/pic9", "event_country": "France", "event_state": "Île-de-France", "event_city": "Paris", "event_date": "2025-01-09"},
        {"id": 10, "url": "https://example.com/pic10", "event_country": "Italy", "event_state": "Lazio", "event_city": "Rome", "event_date": "2025-01-10"}
]

    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])

def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == int(id):
            return jsonify(picture)
    return jsonify({"message": "Picture not found"}), 404



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    request_data = request.get_json()

    if not request_data:
        return jsonify({"message": "No data provided in the request body"}), 400

    id = request_data.get("id")
    if not id:
        return jsonify({"message": "'id' is required in the request body"}), 400

    # Check if the picture with the same id already exists
    for picture in data:
        if picture['id'] == id:
            return jsonify({"Message": f"picture with id {id} already present"}), 302

    required_fields = ['pic_url', 'event_country', 'event_state', 'event_city', 'event_date']
    for field in required_fields:
        if field not in request_data:
            return jsonify({"message": f"'{field}' is required in the request body"}), 400

    new_pic = {
        "id": id,
        "pic_url": request_data['pic_url'],
        "event_country": request_data['event_country'],
        "event_state": request_data['event_state'],
        "event_city": request_data['event_city'],
        "event_date": request_data['event_date']
    }

    data.append(new_pic)
    return jsonify({"Message": f"Picture with id {id} added successfully.", "Picture": new_pic, "id": id}), 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    request_data = request.get_json()

    # Find the picture in the data list
    for picture in data:
        if picture['id'] == id:
            # Explicitly update each field
            picture['pic_url'] = request_data.get('pic_url', picture['pic_url'])
            picture['event_country'] = request_data.get('event_country', picture['event_country'])
            picture['event_state'] = request_data.get('event_state', picture['event_state'])
            picture['event_city'] = request_data.get('event_city', picture['event_city'])
            picture['event_date'] = request_data.get('event_date', picture['event_date'])
            
            return jsonify(picture), 200

    # If picture not found, return 404
    return jsonify({"message": "picture not found"}), 404
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i ,picture in enumerate(data):
        if picture['id']==id:
            del data[i]
            return '',204
    return jsonify({"message": "picture not found"}),404