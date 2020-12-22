import os
import sqlite3


class SQLiteDB:
    _default = "None"
    current_id_category = 1

    def __init__(self, path="server/data"):
        self._setup_path(path)
        self.sqlite_connection = sqlite3.connect(self.path, check_same_thread=False)
        self.sqlite_connection.row_factory = sqlite3.Row
        self.cursor = self.sqlite_connection.cursor()
        self.create_tables()

    def _setup_path(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                files = []
                for file in os.listdir(path):
                    if file.endswith(".db"):
                        files.append(file)
                if len(files) != 0:
                    self.path = os.path.join(path, files[0])
                else:
                    self.__create_file_db(os.path.join(path, "task.db"))
            if os.path.isfile(path):
                self.path = path
        else:
            if os.path.isdir(path):
                self.__create_file_db(os.path.join(path, "task.db"))
            if os.path.isfile(path) and os.path.splitext(path)[1] == ".db":
                self.__create_file_db(path)
            if os.path.isfile(path) and os.path.splitext(path)[1] != ".db":
                self.__create_file_db(os.path.splitext(path)[0] + ".db")

    def __create_file_db(self, path):
        self.path = path
        with open(path, "w") as f:
            pass

    def create_tables(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS categories (id_category INTEGER, name_category varchar(20) UNIQUE, PRIMARY KEY(id_category));")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id_task INTEGER, title VARCHAR(20), status INTEGER , id_category INTEGER, PRIMARY KEY(id_task), FOREIGN KEY(id_category) REFERENCES categories(id_category));")
        self.cursor.execute("SELECT COUNT(id_category) FROM categories")
        categories_count = self.cursor.fetchone()[0]
        if categories_count == 0:
            self.insert_category(self._default)

    def get_all_tasks(self):
        self.cursor.execute("SELECT * FROM tasks ORDER BY id_task DESC;")
        return self.cursor.fetchall()

    def get_filtered_tasks(self, id_category):
        self.cursor.execute("SELECT * FROM tasks WHERE id_category=? ORDER BY id_task DESC;", (id_category,))
        return self.cursor.fetchall()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories;")
        return self.cursor.fetchall()

    def insert_task(self, title_task: str):
        self.cursor.execute("INSERT INTO tasks (title, status, id_category) VALUES (?, FALSE, ?)", (title_task, self.current_id_category,))
        self.sqlite_connection.commit()

    def insert_category(self, category: str):
        self.cursor.execute("INSERT INTO categories(name_category) VALUES (?);", (category,))
        self.sqlite_connection.commit()

    def update_task_status(self, id_task: int, new_status: int):
        self.cursor.execute("UPDATE tasks SET status=? WHERE id_task=?;", (new_status, id_task,))
        self.sqlite_connection.commit()

    def update_task_category(self, id_task: int, id_category: int):
        self.cursor.execute("UPDATE tasks SET id_category=? WHERE id_task=?;", (id_category, id_task,))
        self.sqlite_connection.commit()

    def update_category_name(self, id_destination: int, source: str):
        self.cursor.execute("UPDATE categories SET name_category=? WHERE id_category=?;", (source, id_destination,))
        self.sqlite_connection.commit()

    def delete_task(self, task_id: int):
        self.cursor.execute("DELETE FROM tasks WHERE id_task=?;", (task_id,))

    def delete_category(self, category_id: int):
        self.cursor.execute("DELETE FROM categories WHERE id_category=?;", (category_id,))

    def __del__(self):
        self.sqlite_connection.close()