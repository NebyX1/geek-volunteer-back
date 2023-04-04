from utils.db import db


class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(250), nullable=True)

    user_info = db.relationship('UserInfo', backref='developer', lazy=True)
    reviews = db.relationship('Review', backref='developer', lazy=True)
    projects = db.relationship('Project', backref='developer_in_charge', lazy=True)

    def __repr__(self):
        return '<Developer %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "avatar": self.avatar
        }
    
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    org_sector = db.Column(db.String(100), nullable=False)
    org_description = db.Column(db.String(250), nullable=False)
    org_phone = db.Column(db.String(20), nullable=False)
    org_web = db.Column(db.String(250), nullable=True)
    org_vision = db.Column(db.String(250), nullable=True)

    reviews = db.relationship('Review', backref='organization', lazy=True)
    projects = db.relationship('Project', backref='organization', lazy=True)

    def __repr__(self):
        return '<Organization %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "org_sector": self.org_sector,
            "org_description": self.org_description,
            "org_phone": self.org_phone,
            "org_web": self.org_web,
            "org_vision": self.org_vision
        }
    
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    english_level = db.Column(db.String(50), nullable=False)
    github_link = db.Column(db.String(250), nullable=True)
    linkedin = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    programming_languages = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<UserInfo %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "developer_id": self.developer_id,
            "country": self.country,
            "city": self.city,
            "english_level": self.english_level,
            "github_link": self.github_link,
            "linkedin": self.linkedin,
            "description": self.description,
            "programming_languages": self.programming_languages
        }

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.String(250), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    developer_in_charge_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=True)

    reviews = db.relationship('Review', backref='project', lazy=True)

    def __repr__(self):
        return '<Project %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "project_name": self.project_name,
            "project_description": self.project_description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "done": self.done,
            "developer_in_charge_id": self.developer_in_charge_id
        }
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return '<Review %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "organization_id": self.organization_id,
            "developer_id": self.developer_id,
            "project_id": self.project_id,
            "stars": self.stars,
            "comment": self.comment
        }
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }