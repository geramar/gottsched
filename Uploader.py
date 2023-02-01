from mysql.connector import connect, MySQLConnection
from typing import NoReturn
from Letter import Letter
from greeting_analysis.Schema import Schema


class Uploader:
    def __init__(self, host: str, user: str, password: str, database: str) -> NoReturn:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.__make_connection()

    def __make_connection(self) -> MySQLConnection:
        connection = connect(host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database)
        return connection

    def __commit_query(self, query: str) -> NoReturn:
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def select(self, query: str):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def create_table(self, table_name: str) -> NoReturn:
        create_query = f"CREATE TABLE if not exists {table_name} (id INT PRIMARY KEY AUTO_INCREMENT, band INT," \
                       "page INT, sender VARCHAR(128), receiver VARCHAR(128), date DATE, greeting VARCHAR(256));"
        self.__commit_query(create_query)

    def insert_letter(self, letter: Letter, table_name : str) -> NoReturn:
        formatted_date = self.__format_date(letter.get_date())
        insert_query = f"INSERT {table_name} (band, page, sender, receiver, date, greeting) " \
                       f"VALUES ({letter.get_band()}, {letter.get_page()}, '{letter.get_sender()}',"  \
                       f"'{letter.get_receiver()}', '{formatted_date}', '{letter.get_greeting()}');"
        if not self.__check_letter_existence(table_name, letter.get_band(), letter.get_page()):
            self.__commit_query(insert_query)

    def insert_band(self, list_of_letters: list[Letter], table_name: str) -> NoReturn:
        i = 0
        for letter in list_of_letters:
            self.insert_letter(letter, table_name)
            if not self.__check_letter_existence(table_name, letter.get_band(), letter.get_page()):
                i += 1
        print(f"Band {list_of_letters[0].band}, {len(list_of_letters)} letters. Uploaded: {i}")

    def insert_schema(self, id: int, schema: Schema, table_name: str):
        if not self.__check_schema_existence(table_name, id):
            insert_query = f"INSERT {table_name} (id, short_schema, long_schema) VALUES ({id}, '{schema.short}', '{schema.long}');"
            self.__commit_query(insert_query)
            print (f"Inserted, id: {id}")

    @staticmethod
    def __format_date(date: str) -> str:
        split = date.split(".")
        if len(split) == 3:
            day, month, year = split
        else:
            day, month, year = 0, 0, split[0]
        if month == '02' and day == '29':
            day = '28'
        formatted_date = f"{year}-{month}-{day}"
        return formatted_date

    def __check_letter_existence(self, table_name: str, band: int, page: int) -> bool:
        select_query = f"SELECT COUNT(*) FROM {table_name} WHERE band={band} and page={page};"
        with self.connection.cursor() as cursor:
            cursor.execute(select_query)
            result = int(cursor.fetchone()[0])
            return True if result else False

    def __check_schema_existence(self, table_name: str, id: int):
        select_query = f"SELECT COUNT(*) FROM {table_name} WHERE id={id};"
        with self.connection.cursor() as cursor:
            cursor.execute(select_query)
            result = int(cursor.fetchone()[0])
            return True if result else False





