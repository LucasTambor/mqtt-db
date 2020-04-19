#!/usr/bin/python3
import sqlite3

class SqliteDB(object):
    DB_NAME = ""
    TABLE_NAME = ""

    def __init__(self, db_file):
        self.DB_NAME = db_file
        print("Initializing DB at {}".format(self.DB_NAME))

    def CreateTable(self, name):
        self.TABLE_NAME = name
        self.db = sqlite3.connect(self.DB_NAME)
        self.cur = self.db.cursor()

        print("Creating Table {}".format(self.TABLE_NAME))
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS {}
                (id INTEGER PRIMARY KEY AUTOINCREMENT, deviceID TEXT, messageID INTEGER,
                temperature REAL, humidity REAL, command INTEGER, sample INTEGER, date DATE, time TIME);'''.format(name))
        except Exception as e:
            print("Faile to create table {}:".format(name))
            print(e)
            raise(e)
        finally:
            self.db.close()

    def saveJson(self, json):
        self.db = sqlite3.connect(self.DB_NAME)
        self.cur = self.db.cursor()
        print("Saving Json to {}".format(self.TABLE_NAME))
        try:
            self.cur.execute('''INSERT INTO {}
                                ('deviceID', 'messageID', 'temperature', 'humidity', 'command', 'sample',
                                 'date', 'time')
                                VALUES(?, ?, ?, ?, ?, ?, date('now', 'localtime'), time('now', 'localtime'));'''.format(self.TABLE_NAME),
                                (json["ID"], 1, json["TEMP"], json["HUMID"], json["SAMPLE"], json["CMD"]))
        except Exception as err:
            print("Failed execution in SQL: ")
            print(err)
            self.db.rollback() #clean last operation, after last commit, to DB last stable state
        else:
            self.db.commit()
        finally:
            self.db.close()

    def commit(self):
        self.db.commit()

    def PrintTable(self):
        self.cur.execute("SELECT * FROM {}".format(self.TABLE_NAME))
        for row in self.cur:
            print(row)

if __name__ == '__main__':
    print("#########################################")
    print("Persister Test")
    print("#########################################")

    db = SqliteDB("test.db")

    db.CreateTable("test_table")

    db.PrintTable()