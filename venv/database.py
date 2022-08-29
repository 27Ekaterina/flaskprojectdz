from sqlite3 import connect

# Создание баз данных в файле. Если таблицы уже созданы, то его исполнять не нужно

cur = connect('hhsqlite.sqlite').cursor()

cur.executescript('''
    create table area (
    id integer primary key,
    regioncode varchar(50) unique
    );
''')

cur.executescript('''
    create table where_search (
    id integer primary key,
    name varchar(50) unique
    );
''')

cur.executescript('''
    create table skills (
    id integer primary key,
    name varchar (64) unique
    );
''')

cur.executescript('''
    create table words (
    id integer primary key,
    word varchar (64) unique
    );
''')

cur.executescript('''
    CREATE TABLE wordskills (
    id_word INTEGER REFERENCES words (id),
    id_skill INTEGER REFERENCES skills (id),
    id_area INTEGER REFERENCES area (id),
    id_where_search INTEGER REFERENCES where_search (id),
    count integer,
    sellary integer,
    percent integer
    );
''')


cur.close()
