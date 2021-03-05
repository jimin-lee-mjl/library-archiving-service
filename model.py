from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False, unique=True)
    rentals = db.relationship('Rental', backref='user')
    comment = db.relationship('Comment', backref='user')
    marks = db.relationship('Mark', backref='user')

    def rental_book(self, book_id):
        new_rental = Rental(
            book_id=book_id,
            user_id_history=self.id
        )
        self.rentals.append(new_rental)

    def return_book(self, book):
        self.rentals.remove(book)

    def create_comment(self, content, rating, book_id):
        new_comment = Comment(
            content=content,
            rating=rating,
            book_id=book_id
        )
        self.comment.append(new_comment)

    def create_mark(self, book_id):
        marked_book = Mark(
            book_id=book_id
        )
        self.marks.append(marked_book)

    def check_mark(self, book_id):
        try:
            marked_book = [book for book in self.marks if book.book_id == book_id][0]
            return True
        except:
            return False

    def check_rental(self, book_id):
        try:
            rent_book = [book for book in self.rentals if book.book_id == book_id][0]
            return True
        except:
            return False


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(30))
    publisher = db.Column(db.String(30))
    publication_date = db.Column(db.Date)
    pages = db.Column(db.Integer)
    isbn = db.Column(db.String(50))
    description = db.Column(db.Text)
    link = db.Column(db.Text)
    image = db.Column(db.String(50))
    rating = db.Column(db.Integer, default=0)
    available = db.Column(db.Integer, default=5)
    comment = db.relationship('Comment', backref='book')

    def is_available(self):
        return self.available > 0

    def rental_book(self):
        self.available -= 1

    def return_book(self):
        self.available += 1

    def calculate_rating(self):
        total = 0
        if self.comment:
            for comment in self.comment:
                rating = int(comment.rating)
                total += rating
            total = round(total/len(self.comment))
        return total


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    rental_date = db.Column(db.Date, default=datetime.now().date())
    return_date = db.Column(db.Date)
    user_id_history = db.Column(db.Integer)
    book_detail = db.relationship('Book', backref='rental')

    def return_book(self):
        self.return_date = datetime.now().date()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.Date, default=datetime.now().date())
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def update(self, content, rating, update_date):
        self.content = content
        self.rating = rating
        self.created_at = update_date


class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    book_detail = db.relationship('Book', backref='mark')
