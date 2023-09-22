"""
добавляем в текущие таблицы значения
"""
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from configBD import Supplier
#
# # Создаем соединение с базой данных
# engine = create_engine('postgresql://postgres:ghbdtnsql@localhost:5432/ygolek')
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # Создаем новых поставщиков
# suppliers = [
#     Supplier(name='СУЭК-Черногорск'),
#     Supplier(name='Аршановский'),
#     Supplier(name='ИЗЫХСКИЙ')
# ]
#
# # Добавляем поставщиков в сессию и сохраняем изменения в базе данных
# session.add_all(suppliers)
# session.commit()
#
# # Закрываем сессию
# session.close()
# _________________________________________________________________________________________________________


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configBD import Supplier, CoalBrand

# Создаем соединение с базой данных
engine = create_engine('postgresql://postgres:ghbdtnsql@localhost:5432/ygolek')
Session = sessionmaker(bind=engine)
session = Session()

# Создаем новых поставщиков
suppliers = [
    Supplier(name='СУЭК-Черногорск'),
    Supplier(name='Аршановский'),
    Supplier(name='ИЗЫХСКИЙ')
]

# Создаем новые марки угля
coal_brands = [
    CoalBrand(name='ДМСШ 0-25', supplier=suppliers[0], price_per_ton=100.0),
    CoalBrand(name='ДО 25-50', supplier=suppliers[0], price_per_ton=150.0),
    CoalBrand(name='ДПК 50-200', supplier=suppliers[0], price_per_ton=200.0),
    CoalBrand(name='ДР 0-300', supplier=suppliers[0], price_per_ton=250.0),
    CoalBrand(name='Рядовка', supplier=suppliers[0], price_per_ton=300.0),
    CoalBrand(name='Обогащенный', supplier=suppliers[1], price_per_ton=200.0),
    CoalBrand(name='Порода', supplier=suppliers[2], price_per_ton=250.0)
]

# Добавляем поставщиков и марки угля в сессию и сохраняем изменения в базе данных
session.add_all(suppliers)
session.add_all(coal_brands)
session.commit()

# Закрываем сессию
session.close()
