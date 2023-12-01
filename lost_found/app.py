import json

from db import db
from flask import Flask, request
from db import Item
from db import Location
import locations

# define db filename
db_filename = "lost.db"
app = Flask(__name__)

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# -- TASK ROUTES ------------------------------------------------------


@app.route("/")
@app.route("/items/")
def get_items():
    """
    Endpoint for getting all items
    """
#    tasks = []
#    for task in Task.query.all():
#        tasks.append(task.serialize())
#    return success_response({"tasks":tasks})

    items = [item.serialize() for item in Item.query.all()]
    return success_response({"items":items})

@app.route("/items/<int:loc_id>", methods=["POST"])
def create_items(loc_id):
    """
    Endpoint for creating a new task
    """
    body = json.loads(request.data)
    new_item = Item(desc = body.get("desc"), loc_desc=body.get("loc_desc"), time=body.get("time"), status = body.get("status"), contact = body.get("contact"), loc_id=loc_id)
    db.session.add(new_item)
    db.session.commit()
    return success_response(new_item.serialize(), 201)



@app.route("/items/<int:item_id>/")
def get_item(item_id):
    """
    Endpoint for getting a item by id
    """
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response("Item not found!")
    return success_response(item.serialize())



@app.route("/items/<int:item_id>/", methods=["DELETE"])
def delete_item(item_id):
    """
    Endpoint for deleting a item by id
    """
    item = Item.query.filter_by(id=item_id).first()
    if item is None:
        return failure_response("Item not found!")
    db.session.delete(item)
    db.session.commit
    return success_response(item.serialize())

@app.route("/items/<int:loc_id>/")
def get_items_by_loc_id(loc_id):
    location = Location.query.filter_by(id=loc_id).first()
    if location is None:
        return failure_response("Location not found!")
    return success_response(location.serialize()["items"])


@app.route("/items/<int:loc_code>/")
def get_items_by_loc_code(loc_code):
    location = Location.query.filter_by(building_code=loc_code).first()
    if location is None:
        return failure_response("Location not found!")
    return success_response(location.serialize()["items"])


# -- SUBTASK ROUTES ---------------------------------------------------


@app.route("/locations/")
def get_all_locations():
    """
    Gets all locations
    """
    locations = [loc.serialize() for loc in Location.query.all()]
    return success_response({"locations":locations})

@app.route("/locations/<int:building_code>/")
def get_location_id_by_code(building_code):
    """
    Get id of location by code.
    """

    location = Location.query.filter_by(building_code=building_code).first()
    if location is None:
        return failure_response("Location not found!")
    return location.serialize()["id"]



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
