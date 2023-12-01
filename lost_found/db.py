from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Location(db.Model):
    """
    Location model.
    """

    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    building_name = db.Column(db.String, nullable=False)
    building_code = db.Column(db.String, nullable=False)
    items = db.relationship("Item", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a Location Object.
        """        
        self.building_name = kwargs.get("building_name")
        self.building_code = kwargs.get("building_code")

    def serialize(self):
        """
        Serialize a Location Objectt
        """
        return {
            "id": self.id,
            "building_name" : self.building_name,
            "building_code" : self.building_code,
            "items" : [r.serialize() for r in self.reservations]
        }

class Item(db.Model):
    """
        Item Model
    """
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    desc = db.Column(db.String, nullable = False)
    loc_desc = db.Column(db.String, nullable = False)
    time = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False)
    contact = db.Column(db.String, nullable = True)

    
    loc_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)

    def __init__(self, **kwargs):
            """
            Initialize item object
            """
            self.desc = kwargs.get("desc")
            self.loc_desc = kwargs.get("loc_desc")
            self.time = kwargs.get("time")
            self.status = kwargs.get("status")
            self.contact = kwargs.get("contact")

        
    def serialize(self):
            """
            Serialize a item object
            """
            return {
                "id" : self.id,
                "desc" : self.desc,
                "loc_desc" : self.loc_desc,
                "time" : self.time,
                "status" : self.status,
                "contact" : self.contact            
                }
        