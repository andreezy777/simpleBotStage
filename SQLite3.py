import sqlite3


class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM Schedule').fetchall()

    def write_to(self, chat_id, user_id, username, dayofweek, user_with_id):
        sqlite_insert_with_param = """INSERT INTO Schedule
                                 (ChatID, UserID, User, DayOfWeek,UserWithID) 
                                 VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (chat_id, user_id, username, dayofweek, user_with_id)
        self.cursor.execute(sqlite_insert_with_param, data_tuple)
        self.connection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

    def read_my_data(self, username, user_with_id):
        with self.connection:
            return self.cursor.execute('''SELECT s.DayOfWeek FROM Schedule s
                                        WHERE s.User = ? and s.UserWithID = ?''', [username, user_with_id]).fetchall()

    def getID(self, user_id):
        with self.connection:
            return self.cursor.execute('''SELECT  ChatID FROM Schedule WHERE UserID=? LIMIT 1''', [user_id]).fetchall()

    def getChatID(self, username):
        with self.connection:
            return self.cursor.execute('''SELECT  ChatID FROM Schedule WHERE lower(User) = lower(?) LIMIT 1''', [username]).fetchall()

    def getUserID(self, chat_id):
        with self.connection:
            return self.cursor.execute('''SELECT  UserID FROM Schedule WHERE ChatID=? LIMIT 1''', [chat_id]).fetchall()

    def check_row(self, dayofweek, user_id, user_with_id):
        with self.connection:
            return self.cursor.execute('''SELECT * FROM Schedule WHERE DayOfWeek = ? and UserID = ? and UserWithID = ?''',
                     [dayofweek, user_id, user_with_id]).fetchall()

    def delete_row(self, dayofweek, user_id, user_with_id): # check for cursor.rowcount
        with self.connection:
            self.cursor.execute('''DELETE FROM Schedule WHERE DayOfWeek = ? and UserID = ? and UserWithID = ?''',
                                [dayofweek, user_id, user_with_id])
            self.connection.commit()
            print("Python Variables deleted successfully into SqliteDb_developers table")

    def clear(self, user_id):
        with self.connection:
            self.cursor.execute('''DELETE FROM Schedule WHERE UserID = ? and UserWithID = 0 ''', [user_id] )
            self.connection.commit()
            print("Users with UserWithID = 0 - cleared")

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()
