import os
import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import create_tables
from models import Publisher, Shop, Book, Stock, Sale
from datetime import datetime

if __name__ == '__main__':

    load_dotenv()
    
    login = os.getenv('login')
    password = os.getenv('password')    
    database_name = os.getenv('database_name') 
    # postgresql
    DSN = f'postgresql://{login}:{password}@localhost:5432/{database_name}' 
    engine = sq.create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), 
                          **record.get('fields')))        
        session.commit()
        
    publisher = input('enter the publisher\'s name or ID: ')

    try: 
        id = int(publisher)
        query = (session.query(Publisher).
                 join(Book).
                 join(Stock).
                 join(Shop).
                 join(Sale).
                 filter(Publisher.id == id))
        results = query.all()  
    except ValueError:
        query = (session.query(Publisher).
                 join(Book).
                 join(Stock).
                 join(Shop).
                 join(Sale).
                 filter(Publisher.name.like(f'%{publisher}%')))
        results = query.all()       

    if results:
        for result in results:                          
            for book in result.books:   
                for stock in book.stocks:   
                    for sale in stock.sales:    
                        date_sale = (
                        datetime.fromisoformat(str(sale.date_sale)).date()
                        )                         
                        sum = str(sale.count*sale.price)
                        print(f'{book.title} | '  
                              f'{stock.shop.name} | {sum} | {date_sale}')
    else:
        print("No publishers found matching the criteria.") 

    session.close()




