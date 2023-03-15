from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, request, redirect
import todoData.data as tdata
import checkData

# init flask
app = Flask(__name__)

bootstrap = Bootstrap4(app)

# connect to database
tdata.connectTo(host = '127.0.0.1', user = 'todoman', password = '123456', database = 'todo_db', charset = 'utf8')

# check the data
def check(jsondata:dict):
    if 'deadline' not in jsondata.keys():
        return False
    if not checkData.checkDateStr(jsondata['deadline']):
        return False
    if 'id' not in jsondata.keys():
        jsondata['id'] = '0'
    if 'description' not in jsondata.keys():
        jsondata['description'] = ''
    if 'moduleTitle' not in jsondata.keys():
        jsondata['moduleTitle'] = ''
    if 'title' not in jsondata.keys():
        jsondata['title'] = ''
    if jsondata['title'] == '':
        return False
    if 'difficulty' not in jsondata.keys():
        jsondata['difficulty'] = 'easy'
    return True

def mainPage(data, tip=0):
    errFlag = dict()
    errFlag['tip'] = 'placeholder'
    errFlag['color'] = ''
    if tip == 0:
        tip = tdata.TodoData('module title', 'title', 'deadline', None, None, None, None)
    elif tip == 1:
        tip = tdata.TodoData('module title', 'could not be empty', 'format: xxxx-xx-xx', None, None, None, None)
        errFlag['color'] = 'error'
        errFlag['tip'] = 'value'
    return render_template('index.html', data=data, tip=tip, errFlag=errFlag)

# the root
@app.route('/')
def index():
    data = tdata.select()
    if data == None:
        data = tdata.select()
    return mainPage(data, tip=0)

# get all item
@app.route('/all', methods=['POST'])
def index_all():
    data = tdata.select()
    return mainPage(data, 0)

# get finish item
@app.route('/finish', methods=['POST'])
def index_finish():
    data = tdata.select('yes')
    return mainPage(data, 0)

# get todo item
@app.route('/todo', methods=['POST'])
def index_todo():
    data = tdata.select('no')
    return mainPage(data, 0)

# search by title
@app.route('/search')
def search():
    query = request.args['title']
    data = tdata.searchByTitle(query)
    return mainPage(data, 0)

# if something error
@app.route('/error')
def dealError():
    data = tdata.select()
    return mainPage(data, 1)

# modify the content
@app.route('/change')  # type: ignore
def modify():
    jsondata = request.args
    print('change', jsondata)
    jsondata = dict(jsondata)
    if check(jsondata):
        tdata.modify(tdata.getTodoDataFromJson(jsondata))
        tdata.commit()
    else:
        return redirect('/error')
    return redirect('/')
    # return render_template('index.html', data=tdata.select())

# add new todo
@app.route('/add')
def add():
    jsondata = request.args
    print('add', jsondata)
    jsondata = dict(jsondata)
    jsondata['id'] = '0'    # this is a dummy id
    if check(jsondata):
        tdata.insert(tdata.getTodoDataFromJson(jsondata))
        tdata.commit()
    else:
        return redirect('/error')
    return redirect('/')
    # return render_template('index.html', data=tdata.select())

# delete todo
@app.route('/delete')
def delete():
    jsondata = request.args
    print('delete', jsondata)
    jsondata = dict(jsondata)
    tdata.delete(tdata.getTodoDataFromJson(jsondata))
    tdata.commit()
    # return render_template('index.html', data = tdata.select())
    return redirect('/')

app.run()
