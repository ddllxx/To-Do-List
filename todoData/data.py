import pymysql
import datetime

# connect
conn = None
cursor = None

# the data struct for todo
class TodoData:
    def __init__(self, moduleTitle, title, deadline, description, difficulty, finish, id = None):
        self.deadline = deadline
        self.moduleTitle = moduleTitle
        self.title = title
        self.description = description
        self.finish = finish
        self.id = id
        self.difficulty = difficulty
        self.danger = False
    def __str__(self) -> str:
        return 'moudleTitle: ' + self.moduleTitle + '\ntitle: ' + self.title + '\ndeadline: ' + self.deadline + '\ndescription: ' + self.description + '\nfinsih: ' + self.finish + '\nnum: ' + self.num

# connect to the database
def connectTo(host = '127.0.0.1', user = 'todomgr', password = 'todomgr', database = 'todo_db', charset = 'utf8'):
    global conn
    conn = pymysql.connect(host = host, user = user, password = password, database=database, charset=charset)
    global cursor
    cursor = conn.cursor()

# disconnect
def disconnect():
    cursor.close()
    conn.close()

# select the data
def select(statu='all'):
    whereSub = ''
    if statu == 'yes':
        whereSub = ' WHERE finish = \'yes\''
    elif statu == 'no':
        whereSub = ' WHERE finish = \'no\''
    sql = 'SELECT * FROM todolist' + whereSub
    cursor.execute(sql)
    data = cursor.fetchall()
    ret = []
    for todo in data:
        ret.append(TodoData(todo[1], todo[2], todo[3].strftime('%Y-%m-%d'), todo[4], todo[6], todo[5], id = todo[0]))
        days = -(datetime.datetime.now() - todo[3]).days
        if days < 7 and todo[5] == 'no':
            ret[-1].danger = True
    return ret

# search by title
def searchByTitle(title):
    sql = f'SELECT * FROM todolist WHERE title LIKE \"%{title}%\"'
    cursor.execute(sql)
    data = cursor.fetchall()
    ret = []
    for todo in data:
        ret.append(TodoData(todo[1], todo[2], todo[3].strftime('%Y-%m-%d'), todo[4], todo[6], todo[5], id = todo[0]))
    return ret

# insert new data
def insert(todo : TodoData):
    sql = f'INSERT INTO todolist(moduleTitle, title, deadline, difficulty, description, finish) VALUES(\"{todo.moduleTitle}\", \"{todo.title}\", \"{todo.deadline + " 00:00:00"}\", \"{todo.difficulty}\", \"{todo.description}\", \"{todo.finish}\")'
    ret = cursor.execute(sql)
    print(ret)

# delete data
def delete(todo : TodoData):
    sql = f'DELETE FROM todolist WHERE id = \"{todo.id}\"'
    ret = cursor.execute(sql)
    print(ret)

# modify data
def modify(todo : TodoData):
    sql = f'UPDATE todolist SET moduleTitle=\"{todo.moduleTitle}\", title=\"{todo.title}\", deadline=\"{todo.deadline}\", difficulty=\"{todo.difficulty}\", description=\"{todo.description}\", finish=\"{todo.finish}\" WHERE id = \"{todo.id}\"'
    ret = cursor.execute(sql)
    print(ret)

# format the json to tododata
def getTodoDataFromJson(data):
    finish = None
    difficulty = None
    if data['finish'] == '1':
        finish = 'yes'
    else:
        finish = 'no'
    if data['difficulty'] == '1':
        difficulty = 'middle'
    elif data['difficulty'] == '0':
        difficulty = 'easy'
    elif data['difficulty'] == '2':
        difficulty = 'difficult'
    d = TodoData(data['moduleTitle'], data['title'], data['deadline'], data['description'], difficulty, finish, id=data["id"])
    return d

# commit the change
def commit():
    conn.commit()