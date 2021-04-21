import csv
from datetime import datetime
from app import db
from model import Book


def create_library():
    with open('library.csv', 'r') as books:
        reader = csv.DictReader(books)

        for row in reader:
            date_str = row['publication_date']
            published_at = datetime.strptime(date_str, '%Y-%m-%d').date()
            image = f'./static/book_img/{row["id"]}'
            try:
                open(f'{image}.png')
                image += '.png'
            except:
                image += '.jpg'

            book = Book(
                id=int(row['id']),
                name=row['book_name'],
                author=row['author'],
                publisher=row['publisher'],
                publication_date=published_at,
                pages=int(row['pages']),
                isbn=row['isbn'],
                description=row['description'],
                link=row['link'],
                image=image,
                rating=0,
                available=5
            )
            db.session.add(book)

        db.session.commit()

