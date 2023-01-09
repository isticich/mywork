import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # def add_user(self, user_id,):
    #     with self.connection:
    #         return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `referrer_id`) VALUES (?,?)", (user_id, referrer_id,))
            else:
                return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def count_reeferals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`id`) as count FROM `users` WHERE `referrer_id` = ?", (user_id,)).fetchone()[0]

    def set_active(self, user_id, active):
         with self.connection:
              return self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `active`  FROM `users`").fetchall()

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def user_bonus(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `bonus` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return int(result[0][0])

    def set_bonus(self, user_id, bonus):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `bonus` = ? WHERE `user_id` = ?", (bonus, user_id,))