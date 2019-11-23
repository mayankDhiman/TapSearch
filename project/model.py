"""
from project import db
from sqlalchemy import *
from sqlalchemy.orm import *

class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(4294000000))
    isPdf = db.Column(db.Boolean)
"""