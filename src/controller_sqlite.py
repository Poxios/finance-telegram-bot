import sqlite3
import os


def init_sqlite(cur):
    print('[SYSTEM] Initializing DB Start...')

    # [CREATE TABLE] User
    cur.execute("CREATE TABLE User(id INT PRIMARY KEY, name TEXT NOT NULL)")

    # [CREATE TABLE] Favorite Stock
    cur.execute("CREATE TABLE Favorite_Stock( \
                stock_name TEXT UNIQUE NOT NULL, \
                user_id INT, \
                FOREIGN KEY(user_id) REFERENCES User(id))")

    print('[SYSTEM] Initializing DB Complete')


# ! Create sqlite file and initialize if not exist
init_required = False
if not os.path.isfile('sqlite.db'):
    init_required = True

con = sqlite3.connect('./sqlite.db')
cur = con.cursor()

if init_required:
    init_sqlite(cur)

# ! User


def user_add_new_user(user_id: int, name: str):
    try:
        print('Adding new user...')
        cur.execute(
            f'INSERT INTO User VALUES({user_id,name})')
        print('Adding new user complete')
    except:
        print('Adding new user FAILED')


def user_get_list():
    cur.execute('SELECT * FROM User')
    user_list = cur.fetchall
    return user_list


# ! Favorite Stock

def favorite_stock_get_list(user_id: int):
    try:
        print(f'Get favorite stock list: {user_id}...')
        cur.execute(
            f'SELECT stock_name FROM Favorite_Stock WHERE user_id = {user_id}')
        favorite_stock_list = cur.fetchall()
        print(f'Get favorite stock list: {user_id} success')
        return favorite_stock_list
    except:
        print(f'Get favorite stock list: {user_id} failed')


def favorite_stock_add_to_user(user_id: int, stock_ticker: str):
    try:
        print('Adding favorite stock...')
        cur.execute(
            f'INSERT INTO Favorite_Stock VALUES({stock_ticker, user_id})')
        print('Adding favorite stock complete')
    except:
        print('Adding favorite stock FAILED')


def favorite_stock_remove_from_user(user_id: int, stock_ticker: str):
    try:
        print('Remove favorite stock...')
        cur.execute(
            f'DELETE FROM Favorite_Stock WHERE user_id={user_id}, stock_name={stock_ticker}')
        print('Remove favorite stock complete')
    except:
        print('Remove favorite stock FAILED')