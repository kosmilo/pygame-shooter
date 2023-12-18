import mysql.connector as connector
from datetime import datetime


class DatabaseLink:
    def __init__(self):
        self.get_top5_scores = "select playername, score from scores order by score desc limit 5;"
        self.conn = self.connect_to_db()

    def connect_to_db(self):
        try:
            conn = connector.connect(host="localhost", user="root", password="", database="pygame_shooter_scores")
        except connector.Error as err:
            print(err)
        else:
            return conn

    def save_score_into_db(self, playername, score):
        cursor = self.conn.cursor()
        date = datetime.now().date()

        add_score = "insert into scores(playername, score, date) values (%s, %s, %s);"
        score_data = (playername, score, str(date))

        cursor.execute(add_score, score_data)

        self.conn.commit()
        cursor.close()

    def get_top5_scores_from_db(self):
        print("trying to get scores from db")
        cursor = self.conn.cursor()
        cursor.execute(self.get_top5_scores)
        result = []
        for (playername, score) in cursor:
            result.append((playername, score))
        cursor.close()
        return result



