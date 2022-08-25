import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Shop, Sale
import json

if __name__ == "__main__":

    DSN = 'postgresql://postgres:Odnerka1@localhost:5432/db_orm'
    engine = sqlalchemy.create_engine(DSN)

    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('tests_data.json') as file:
         data = json.load(file)

    for element in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[element.get('model')]
        session.add(model(id=element.get('pk'), **element.get('fields')))

    session.commit()

    search = input("Введите название или идентификатор издателя: ")
    for el in (session.query(Publisher, Book, Stock, Shop)
        .filter(Book.id_publisher == Publisher.id)
        .filter(Stock.id_book == Book.id)
        .filter(Shop.id == Stock.id_shop)
        .filter(Publisher.id == int(search) if search.isdigit() else Publisher.name == search).distinct(Shop.name)):
        print(f'Издатель: {el.Publisher.id}, {el.Publisher.name}, Магазин: {el.Shop.name}')


    session.close()
