import mysql.connector, json

class Datebase:
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
            # task = list(i[1:])
            course = courses[i[3]]
            level = difficulty_levels[i[4]]
            data[course][level].append([i[0], i[1]])
            # tasks[i[0]][2] = courses[i[3]]
            # tasks[i[0]][3] = difficulty_levels[i[4]]
            # for ind in range(len(i[2])):
            #     self.cursor.execute(f"select * from education_material where Educational_Material={i[2][ind]}")
            #     tasks[i[0]][1][ind] = self.cursor.fetchall()[0][1:]

        return data

    def get_education_material(self, id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"Select * from chapter where Chapter_ID={id}")
            data = list(cursor.fetchone())[:3]
            # self.cursor.execute(f"Select Degree from difficulty_level where Difficulty_Level_ID={data[4]}")
            # data[4] = self.cursor.fetchone()[0]
            # self.cursor.execute(f"Select Title from course where Course_ID={data[3]}")
            # data[4] = self.cursor.fetchone()[0]
            data[2] = json.loads(data[2])
            for i in range(len(data[2])):
                cursor.execute(f"select * from education_material where Educational_Material={data[2][i]}")
                data[2][i] = list(cursor.fetchone())

            return data
        except Exception:
            return None

    def delete_education_material(self, task_id, material_id):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"Select * from chapter where Chapter_ID={task_id}")
            data = json.loads(cursor.fetchone()[2])
            data.remove(material_id)
            data = json.dumps(data)
            cursor.execute(f"UPDATE chapter set Content='{data}' where Chapter_ID={task_id}")
            self.connection.commit()
        except Exception:
            pass

    def delete_task(self, id):
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

    def add_task(self, course, level, name):
        try:
            self.connection.reconnect()
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT Course_ID FROM course WHERE Title = '{course}'")
            course_id = cursor.fetchall()[0][0]
            cursor.execute(f"SELECT Difficulty_Level_ID FROM difficulty_level WHERE Degree = '{level}'")
            level_id = cursor.fetchall()[0][0]
            cursor.execute(f"INSERT INTO chapter (Title, Content, CourseCourse_ID, "
                           f"Difficulty_LevelDifficulty_Level_ID, admin_Admin_ID) "
                           f"VALUES ('{name}', '[]', {course_id}, {level_id}, 1)")
            self.connection.commit()
        except Exception:
            pass