from configparser import ConfigParser
import psycopg2 as pg
import os


def get_db_settings():
    """
    Получение настроек подключения к БД.
    """
    cparser = ConfigParser()
    cparser.read(os.path.join(os.getcwd(), 'scripts', 'processing', 'settings', 'settings.ini'))
    db_section = cparser['DB']
    
    return {
        'user': db_section['user'],
        'password': db_section['password'],
        'host': db_section['host'],
        'port': db_section['port'],
        'database': db_section['database']
    }


# Настройки для подключения к БД.
DB_SETTINGS = get_db_settings()
USER = DB_SETTINGS['user']
PASSWORD = DB_SETTINGS['password']
HOST = DB_SETTINGS['host']
PORT = DB_SETTINGS['port']
DATABASE = DB_SETTINGS['database']


def get_info(sql: str):
    """
    Получение информации из БД.

    sql - текст скрипта.
    """
    with pg.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE
    ) as conn:
        cursor = conn.cursor()
        headers = None
        results = None
        try:
            cursor.execute(sql)
            headers = [i[0] for i in cursor.description]
            results = cursor.fetchall()
        except Exception as err:
            print(err)
            return None, None, str(err)

        return headers, results, None
