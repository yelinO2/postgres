import psycopg2

connection = psycopg2.connect(
             host= "localhost", 
             database="store_db",
             user='ye',
             password='password123')

cursor = connection.cursor()

create_user_table = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL, role INT)"
cursor.execute(create_user_table)

create_genre_table = "CREATE TABLE IF NOT EXISTS genre(id SERIAL PRIMARY KEY, genre text)"
cursor.execute(create_genre_table)

create_author_table = "CREATE TABLE IF NOT EXISTS authors(id SERIAL PRIMARY KEY, author text)"
cursor.execute(create_author_table)

create_book_table = "CREATE TABLE IF NOT EXISTS books(id SERIAL PRIMARY KEY, name text, book_cover text, overview text, publication_date text, language text)"
cursor.execute(create_book_table)

connection.commit()

cursor.close()
connection.close()