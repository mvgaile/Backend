from locations import LOCATIONS
from db import db
from db import Location

def create_locations():
    """
    Creates the location table
    """

    for key in LOCATIONS.keys():
        new_location = Location(
            building_name = LOCATIONS[key],
            building_code = key,
        )
        db.session.add(new_location)

    db.session.commit()
