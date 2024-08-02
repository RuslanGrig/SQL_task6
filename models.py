import sqlalchemy as sq
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)    

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=200), nullable=False)        
    id_publisher = sq.Column(sq.Integer,
                             sq.ForeignKey('publisher.id'), 
                             nullable=False)    
    publisher = relationship(Publisher, backref='books')

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)    
    count = sq.Column(sq.Integer, 
                      sq.CheckConstraint('count >= 0'), 
                      nullable=False)
    id_book = sq.Column(sq.Integer, 
                        sq.ForeignKey('book.id'), 
                        nullable=False)
    id_shop = sq.Column(sq.Integer, 
                        sq.ForeignKey('shop.id'), 
                        nullable=False)
    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')    

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    price = sq.Column(sq.Float, 
                      sq.CheckConstraint('price >= 0'), 
                      nullable=False)
    count = sq.Column(sq.Integer, 
                      sq.CheckConstraint('count >= 0'), 
                      nullable=False) 
    date_sale = sq.Column(sq.TIMESTAMP(timezone=True),
        sq.CheckConstraint('date_sale BETWEEN TIMESTAMPTZ ' \
        '\'1900-01-01T00:00:00.113Z\' AND CURRENT_TIMESTAMP'),
          nullable=False)
    id_stock = sq.Column(sq.Integer, 
                         sq.ForeignKey('stock.id'), 
                         nullable=False)
    stock = relationship(Stock, backref='sales')

def create_tables(engine):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)