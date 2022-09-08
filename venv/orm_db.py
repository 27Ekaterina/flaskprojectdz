from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///orm.sqlite', echo=True)

Base = declarative_base(bind=engine)
Session = sessionmaker()


class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    regioncode = Column(String(50), unique=True, index=True)

    def __str__(self):
        return f'{self.id}) {self.regioncode}'

    def __repr__(self):
        return f'{self.id} - {self.regioncode}'


class Where_search(Base):
    __tablename__ = 'where_search'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, index=True)


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String(50), unique=True, index=True)


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True)


class WordSkill(Base):
    __tablename__ = 'wordskills'
    id = Column(Integer, primary_key=True)
    id_word = Column(Integer, ForeignKey('words.id'))
    id_skill = Column(Integer, ForeignKey('skills.id'))
    id_area =  Column(Integer, ForeignKey('area.id'))
    id_where_search = Column(Integer, ForeignKey('where_search.id'))
    count = Column(Integer, default=0)
    sellary = Column(Float, default=0)
    percent = Column(Float, default=0)

    def __str__(self):
        return f'{self.id}) {self.id_word} | {self.id_skill} | {self.id_area} | {self.id_where_search} | {self.count} | {self.sellary} | {self.percent} |'


Base.metadata.create_all()