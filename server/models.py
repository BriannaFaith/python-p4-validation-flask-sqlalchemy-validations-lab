from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def check_name(self, key, name):
        if self.query.filter(Author.name == name).first():
            raise ValueError("Name must be unique")

        if name == '':
            raise ValueError("Name must not be empty")
        return name

    @validates('phone_number')
    def check_phone_number(self, key, phone_number):
        if not phone_number.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly ten digits")
        return phone_number



    def __repr__(self):
        return f'Author(id={self.id}, name={self.name}, phone_number={self.phone_number})'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    @validates('title')
    def check_title(self, key, title):
        if title  == '':
            raise ValueError("Title must not be empty")

        clickbait_words =  ["Won't Believe", "Secret", "Top", "Guess"]
        if any(word in title for word in clickbait_words):
            return title

        raise ValueError("Title is too clickbait-y")




    @validates('content')
    def check_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content too short. Must be at least 250 characters.")
        return content

    @validates('summary')
    def check_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary too long")
        return summary

    @validates('category')
    def check_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'")
        return category




    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
