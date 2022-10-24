import sqlite3


class WeightDb(object):
    def __init__(self):
        self.weight_db, self.db_cursor = self.connect_db()

    def connect_db(self):
        try:
            with sqlite3.connect("database.db") as weight_db:
                db_cursor = weight_db.cursor()
            db_cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='weight' ''')
            if not db_cursor.fetchone()[0] == 1:
                raise ValueError('Table weight does not exists.')
        except ValueError:
            weight_db = sqlite3.connect('database.db')
            weight_db.execute('CREATE TABLE weight (Weight TEXT, Date TEXT)')
            db_cursor = weight_db.cursor()

        return weight_db, db_cursor

    def insert_info(self, weight, date):
        self.db_cursor.execute("INSERT INTO weight (Weight, Date) "
                               "VALUES(?, ?)", (weight, date))
        self.weight_db.commit()

    def delete_last_record(self, date):
        self.db_cursor.execute("DELETE FROM weight WHERE Date=?", (date,))
        self.weight_db.commit()

    def get_coord_data(self):
        date_coord = []
        weight_coord = []
        self.db_cursor.execute("SELECT * FROM weight")
        records = self.db_cursor.fetchall()
        if not records == []:
            for row in records:
                readable_row = str(row).replace(')', '').replace('(', '').replace('u\'', '').replace("'", "")
                split_info = readable_row.split(',')
                weight_coord.append(int(split_info[0]))
                date_coord.append(split_info[1])
            return date_coord, weight_coord
        else:
            return False, False

    def show_db(self):
        self.weight_db.row_factory = sqlite3.Row
        self.db_cursor.execute("select * from weight")
        rows = self.db_cursor.fetchall()
        for row in rows:
            print(row)
