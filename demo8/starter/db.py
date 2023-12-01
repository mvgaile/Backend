from flask_sqlalchemy import SQLAlchemy
import base64
import boto3
import datetime
import io
from io import BytesIO
from mimetypes import guess_extension, guess_type
import os
from PIL import Image
import random
import re
import string

db = SQLAlchemy()

EXTENSIONS = ["png", "gif", "jpg", "jpeg"]
BASE_DIR = os.getcwd()
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_BASE_URL = f"https://{S3_BUCKET_NAME}.s3.us-east-1.amazonaws.com"


class Asset(db.Model):
    """
    Asset model
    """
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    base_url = db.Column(db.String, nullable=True)
    salt = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, **kwargs):
        self.create(kwargs.get("image_data"))
        
        
    def serialize(self):
        return {
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "created_at": str(self.created_at)
        }
        
    def create(self,image_data):
        """
        Given image in base-64 form:
        1. Rejects image if is not a supported file type
        2. Generate a random string for filename
        3. Decode the image and attempts to upload to aws
        """
        try:
            ext = guess_extension(guess_type(image_data)[0])[1:]
            
            if ext not in EXTENSIONS:
                raise Exception("Extension {ext} not supported!")
            
            # generate random string
            salt = "".join(
                random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits
                )
                for _ in range(16)
            )
            
            # remove header of base 64
            img_str = re.sub("^data:image/.+;base64,","",image_data)
            img_data = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_data))
            
            self.base_url = S3_BASE_URL
            self.salt = salt
            self.extension = ext
            self.width = img.width
            self.height = img.height
            self.created_at = datetime.datetime.now()
            
            img_filename = f"{self.salt}.{self.extention}"
            self.upload(img, img_filename)
            
        except Exception as e:
            print("error")
    
    def upload(self, img, img_filename):
        try:
            # Save image tempororialy on server
            img_temploc = f"{BASE_DIR}/{img_filename}"
            img.save(img_temploc)
            
            # Uplaod to s3
            s3_client = boto3.client("s3")
            s3_client.upload_file(img_temploc, S3_BUCKET_NAME, img_filename)
            
            # make s3 image public
            s3resource = boto3.resource('s3')
            object_acl = s3resource.ObjectAcl(S3_BUCKET_NAME, img_filename)
            object_acl.put(ACL = "public")
            
            os.remove(img_temploc)
        except Exception as e:
            print('no')