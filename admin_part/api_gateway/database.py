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

    def delete_education_material(self, chapter_id, material_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"Select * from chapter where Chapter_ID={chapter_id}")
            data = json.loads(cursor.fetchone()[2])
            data.remove(material_id)
            data = json.dumps(data)
            cursor.execute(f"UPDATE chapter set Content='{data}' where Chapter_ID={chapter_id}")
            self.connection.commit()
        except Exception:
            pass

    def delete_chapter(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM chapter WHERE Chapter_ID={id}")
            self.connection.commit()
        except Exception:
            pass

    def add_material(self, id, type, name):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO education_material (Type, Content) VALUES ('{type}', '{name}')")
            cursor.execute(f"SELECT Content FROM chapter WHERE Chapter_ID = {id}")
            data = json.loads(cursor.fetchone()[0])
            cursor.execute(f"SELECT Educational_Material From education_material WHERE (Type, Content) = ('{type}', '{name}')")
            data.append(cursor.fetchone()[0])
            data = json.dumps(data)
            cursor.fetchall()
            cursor.execute(f"UPDATE chapter set Content='{data}' where Chapter_ID={id}")
            self.connection.commit()
        except Exception:
            pass

    def add_chapter(self, course, level, name, admin_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Course_ID FROM course WHERE Title = '{course}'")
            course_id = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT Difficulty_Level_ID FROM difficulty_level WHERE Degree = '{level}'")
            level_id = cursor.fetchall()[0][0]
            cursor.execute(f"INSERT INTO chapter (Title, Content, CourseCourse_ID, "
                           f"Difficulty_LevelDifficulty_Level_ID, admin_Admin_ID) "
                           f"VALUES ('{name}', '[]', {course_id}, {level_id}, {admin_id})")
            self.connection.commit()
        except Exception:
            pass

    def add_course(self, name):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO course (Title) VALUES ('{name}')")
            self.connection.commit()
        except Exception:
            pass

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
            course = courses[i[6]]
            level = difficulty_levels[i[7]]
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

    def update_practical_task(self, id, name, description, reward, answer):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE task set Name='{name}', Description='{description}', Reward={reward}, "
                           f"Answer='{answer}' where Task_ID={id}")
            self.connection.commit()
            return True
        except Exception:
            return False

    def delete_practical_task(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM attempt WHERE TaskTask_ID={id}")
            cursor.execute(f"DELETE FROM task WHERE Task_ID={id}")
            self.connection.commit()
            return True
        except Exception:
            return False

    def add_practical_task(self, course, level, name, description, reward, answer, admin_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Course_ID FROM course WHERE Title = '{course}'")
            course_id = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT Difficulty_Level_ID FROM difficulty_level WHERE Degree = '{level}'")
            level_id = cursor.fetchall()[0][0]
            cursor.execute(f"INSERT INTO task (Name, Answer, Reward, "
                           f"Description, admin_Admin_ID, difficulty_level_Difficulty_Level_ID, course_Course_ID) "
                           f"VALUES ('{name}', '{answer}', {reward}, '{description}', {admin_id}, {level_id}, {course_id})")
            self.connection.commit()
        except Exception:
            pass

    def check_admin(self, email, password):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM admin WHERE (Email, password)=('{email}', '{password}')")
            res = cursor.fetchall()
            if len(res):
                return res[0]
        except Exception:
            return False

    def get_all_users(self):
        try:
            users = {"admins": [], "students": []}
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM admin")
            users["admins"] = cursor.fetchall()
            cursor.execute(f"SELECT * FROM student")
            users["students"] = cursor.fetchall()

            return users
        except Exception:
            return None

    def delete_student(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM attempt WHERE StudentStudent_ID={id}")
            cursor.execute(f"DELETE FROM student_progress WHERE StudentStudent_ID={id}")
            cursor.execute(f"DELETE FROM student WHERE Student_ID={id}")
            self.connection.commit()
        except Exception:
            return None

    def get_student(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM student WHERE Student_ID={id}")
            return cursor.fetchone()
        except Exception:
            return None

    def update_student(self, id, name, email):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE student set Full_Name='{name}', Email='{email}' where Student_ID={id}")
            self.connection.commit()
        except Exception:
            return None

    def add_student(self, name, email, password):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO student (Full_Name, Email, Password) VALUES "
                           f"('{name}', '{email}', '{password}')")
            self.connection.commit()
        except Exception:
            return None

    def add_admin(self, name, email, password, role):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO admin (Full_Name, Email, Password, Role) VALUES ('{name}', '{email}', "
                           f"'{password}', {role})")
            self.connection.commit()
        except Exception:
            return None

    def get_admin(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM admin WHERE Admin_ID={id}")
            return cursor.fetchone()
        except Exception:
            return None

    def update_admin(self, id, name, email, role):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"UPDATE admin set Full_Name='{name}', Email='{email}', Role={role} where Admin_ID={id}")
            self.connection.commit()
        except Exception:
            return None


connection = mysql.connector.connect(host="localhost", user="root", password="root", database="curseusers")
my_database = Database(connection)