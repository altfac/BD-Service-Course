import mysql.connector, json


class Database:
    def __init__(self, connection):
        self.connection = connection

    def get_all_education_materials(self):
        self.connection.reconnect()
        cursor = self.connection.cursor()
        courses, difficulty_levels = {}, {}
        data = {}

        cursor.execute("Select * from difficulty_level")
        ret = cursor.fetchall()
        for i in ret:
            difficulty_levels[i[0]] = i[1]

        cursor.execute("Select * from course")
        ret = cursor.fetchall()
        for i in ret:
            data[i[1]] = {}
            courses[i[0]] = i[1]
            for level in difficulty_levels.keys():
                data[i[1]][difficulty_levels[level]] = []

        cursor.execute("Select * from chapter")
        ret = cursor.fetchall()
        for i in ret:
            course = courses[i[3]]
            level = difficulty_levels[i[4]]
            data[course][level].append([i[0], i[1]])

        return data

    def get_education_material(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"Select * from chapter where Chapter_ID={id}")
            data = list(cursor.fetchone())[:3]
            data[2] = json.loads(data[2])
            for i in range(len(data[2])):
                cursor.execute(f"select * from education_material where Educational_Material={data[2][i]}")
                data[2][i] = list(cursor.fetchone())

            return data
        except Exception:
            return None

    def get_all_practical_tasks(self):
        self.connection.reconnect()
        cursor = self.connection.cursor()
        courses, difficulty_levels = {}, {}
        data = {}

        cursor.execute("Select * from difficulty_level")
        ret = cursor.fetchall()
        for i in ret:
            difficulty_levels[i[0]] = i[1]

        cursor.execute("Select * from course")
        ret = cursor.fetchall()
        for i in ret:
            data[i[1]] = {}
            courses[i[0]] = i[1]
            for level in difficulty_levels.keys():
                data[i[1]][difficulty_levels[level]] = []

        cursor.execute("Select * from task")
        ret = cursor.fetchall()
        for i in ret:
            course = courses[i[7]]
            level = difficulty_levels[i[6]]
            data[course][level].append([i[0], i[1]])

        return data

    def get_practical_task(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM task WHERE (Task_ID)=({id})")
            return cursor.fetchone()
        except Exception:
            return False

    def get_all_attempts_of_task(self, id, student_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM attempt WHERE (TaskTask_ID, StudentStudent_ID)=({id}, {student_id})")
            return cursor.fetchall()
        except Exception:
            return False

    def check_student(self, email, password):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM student WHERE (Email, password)=('{email}', '{password}')")
            res = cursor.fetchall()
            if len(res):
                return res[0]
        except Exception:
            return False

    def get_student(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM student WHERE Student_ID={id}")
            return cursor.fetchone()
        except Exception:
            return None

    def add_attempt(self, task_id, student_id, answer):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM task WHERE Task_ID={task_id}")
            task = cursor.fetchone()
            real_answer = task[2]
            if answer == real_answer:
                verdict = "Принято"
                cursor.execute(f"SELECT * FROM attempt WHERE (StudentStudent_ID, TaskTask_ID)=('{student_id}', '{task_id}')")
                attempts = cursor.fetchall()
                for i in attempts:
                    if i[2] == "Принято":
                        break
                else:
                    cursor.execute(f"SELECT * FROM student_progress WHERE StudentStudent_ID={student_id}")
                    new_raiting = cursor.fetchone()[1] + task[3]
                    cursor.execute(f"UPDATE student_progress set Educational_Rating = {new_raiting} "
                                   f"WHERE StudentStudent_ID={student_id}")
                    cursor.fetchall()
            else:
                verdict = "Неверный ответ"

            cursor.execute(f"INSERT INTO attempt (Solution, Verdict, StudentStudent_ID, TaskTask_ID) VALUES"
                           f"('{answer}', '{verdict}', {student_id}, {task_id})")
            connection.commit()
        except Exception:
            return None

    def get_top(self):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM student_progress")
            student_progress = cursor.fetchall()
            student_progress = sorted(student_progress, key=lambda x: -x[1])[:10]
            data = []
            for i in student_progress:
                cursor.execute(f"SELECT Full_Name FROM student WHERE Student_ID = {i[2]}")
                name = cursor.fetchone()[0]
                data.append([i[1], name])
            return data
        except Exception:
            return []

    def get_student_rating(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Educational_Rating FROM student_progress WHERE StudentStudent_ID = {id}")
            return cursor.fetchone()[0]
        except Exception:
            return []



connection = mysql.connector.connect(host="localhost", user="root", password="root", database="curseusers")
my_database = Database(connection)