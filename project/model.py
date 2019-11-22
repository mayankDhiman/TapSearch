from project import db
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import *
from sqlalchemy.orm import *

# Enrollments Database FIXED

# class Enrollments(db.Model):
#     rollno = db.Column(db.Integer, primary_key=True)
#     subject = db.Column(db.String(64), primary_key=True)
#     payment = db.Column(db.String(64))
#     def __init__(self, rollno, subject):
#         self.rollno = rollno
#         self.subject = subject
#         self.payment = 0

#     def __repr__(self):
        # return '<RollNo: {}, Subject: {}>'.format(self.rollno, self.subject)

# class BlobMixin(object):
#     mimetype = db.Column(db.Unicode(length=255), nullable=False)
#     filename = db.Column(db.Unicode(length=255), nullable=False)
#     blob = db.Column(db.LargeBinary(), nullable=False)
#     size = db.Column(db.Integer, nullable=False)

# class Image(db.Model, BlobMixin):
#     __tablename__ = 'images'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Unicode(length=255), nullable=False, unique=True)
#     def __unicode__(self):
#         return u"name : {name}; filename : {filename})".format(name=self.name, filename=self.filename)

class PdfFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(4294000000))
    isPdf = db.Column(db.Boolean)