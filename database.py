#Стандартная настройка дляя работы с SQLite

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Путь к файлу
SQLALCHEMY_DATABASE_URL ="sqlite:///./inventory.db"


#Создание движка
engine=create_engine(SQLALCHEMY_DATABASE_URL, connrct_args={"check_same_thread":False})

#Фабрика сессий
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

#Базовый класс для модулей
Base=declarative_base()
