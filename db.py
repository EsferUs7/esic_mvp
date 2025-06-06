from os import getenv
from psycopg2 import connect
from datetime import datetime


class DBConnection:
    def __init__(self) -> None:
        self._connection = connect(
            dbname=getenv("DB_NAME"),
            host=getenv("DB_HOST"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
        )
        self._connection.autocommit = True
        self._cursor = self._connection.cursor()

    def get_top(self, group_id: int) -> list[dict[str, object]]:
        self._cursor.execute(f"SELECT * FROM user_info WHERE group_id = {group_id} ORDER BY points DESC")

        result = []

        for row in self._cursor.fetchall():
            user_result = {
                "user_id": row[0],
                "tag_name": row[2],
                "points": row[3],
            }

            result.append(user_result)

        return result
    
    def get_my_rating(self, user_id: int, group_id: int) -> int:
        self._cursor.execute(f"SELECT * FROM user_info WHERE user_id = {user_id} AND group_id = {group_id}")

        return self._cursor.fetchone()[3]
    
    def add_group(self, group_id: int) -> None:
        self._cursor.execute(f"INSERT INTO groups (group_id) VALUES ({group_id})")
    
    def add_user(self, user_id: int, group_id: int, tag_name: str) -> None:
        self._cursor.execute(f"INSERT INTO user_info (user_id, group_id, tag_name) VALUES ({user_id}, {group_id}, '{tag_name}')")

    def add_points(self, user_id: int, group_id: int, points: int) -> None:
        self._cursor.execute(f"UPDATE user_info SET points = points + {points} WHERE user_id = {user_id} AND group_id = {group_id}")
    
    def set_period(self, group_id: int, period: int) -> None:
        self.set_last_message(group_id)

        self._cursor.execute(f"UPDATE groups SET period = {period} WHERE group_id = {group_id}")

    def set_time(self, group_id: int, time: int) -> None:
        if time == 0:
            time = "NULL"

        self.set_last_message(group_id)

        self._cursor.execute(f"UPDATE groups SET send_after = {time} WHERE group_id = {group_id}")

    def set_last_message(self, group_id: int) -> None:
        self._cursor.execute(f"UPDATE groups SET last_message = '{datetime.now()}' WHERE group_id = {group_id}")

    def get_groups_with_ended_period(self) -> list[int]:
        self._cursor.execute("SELECT * FROM groups")

        result = []

        for row in self._cursor.fetchall():
            if (datetime.now() - row[2]).total_seconds() > row[1]:
                result.append(row[0])

        return result
    
    def get_groups_with_ended_time(self) -> list[int]:
        self._cursor.execute("SELECT * FROM groups WHERE send_after IS NOT NULL")

        result = []

        for row in self._cursor.fetchall():
            if (datetime.now() - row[2]).total_seconds() > row[3]:
                result.append(row[0])

        return result

    def add_user_answered_question(self, user_id: int, group_id: int, question_id: int) -> None:
        self._cursor.execute(f"INSERT INTO user_answered_questions (user_id, group_id, question_id) VALUES ({user_id}, {group_id}, {question_id})")

    def has_user_answered_question(self, user_id: int, group_id: int, question_id: int) -> bool:
        self._cursor.execute(f"SELECT * FROM user_answered_questions WHERE user_id = {user_id} AND group_id = {group_id} AND question_id = {question_id}")

        return len(self._cursor.fetchall()) > 0

    def get_question(self) -> dict[str, object]:
        self._cursor.execute("SELECT * FROM questions q JOIN answers a ON a.foreign_question = q.id_question WHERE q.id_question = (SELECT id_question FROM questions ORDER BY RANDOM() LIMIT 1)")

        result = {
            "answers": []
        }

        for row in self._cursor.fetchall():
            result["question_id"] = row[0]
            result["question"] = row[1]
            result["answers"].append(row[4])

            if row[5] is True:
                result["correct_answer"] = row[4]

        return result
  

