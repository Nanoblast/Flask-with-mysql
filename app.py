from flask import Flask, request
from flask_restful import Api
from sqlalchemy import create_engine
import db
import json
app = Flask(__name__)
api = Api(app)
engine = create_engine('mysql+pymysql://root@localhost/CRUD')

@app.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'GET':
        return handle_GET_tasks(request)
    if request.method == 'POST':
        return handle_POST_tasks(request)
    return 'Error during handling the request', 500
def validate_json(data):
    pass

def handle_POST_tasks(request):
    data = request.get_json()
    session = get_mysql_session()
    session.add(db.DataModel(
        title=data['title'],
        description=data['description']
    ))
    session.commit()
    session.close()
    return 'Done', 200

def handle_GET_tasks(request):
    session = get_mysql_session()
    results = session.query(db.DataModel).all()
    query_results = [result.__dict__ for result in results]
    for query_result in query_results:
        query_result.pop('_sa_instance_state', None)
    session.close()
    return query_results, 200

def get_mysql_session():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    return Session()

@app.route('/tasks/<id>', methods=['GET', 'PUT', 'DELETE'])
def handle_tasks_by_id(id):
    if request.method == 'GET':
        return handle_GET_tasks_by_id(request, id)
    if request.method == 'PUT':
        return handle_PUT_tasks_by_id(request, id)
    if request.method == 'DELETE':
        return handle_DELETE_tasks_by_id(request,id)


def handle_GET_tasks_by_id(request, id):
    session = get_mysql_session()
    result = session.query(db.DataModel).filter_by(id=id).first()
    result = result.__dict__
    result.pop('_sa_instance_state', None)
    session.close()
    return result, 200

def handle_PUT_tasks_by_id(request, id):
    session = get_mysql_session()
    result = session.query(db.DataModel).filter_by(id=id).first()
    if not result:
        return "Missing data by ID", 406
    data = request.get_json()
    result.title = data['title']
    result.description = data['description']
    session.add(result)
    session.commit()
    session.close()
    return "Data succesfully updated", 200

def handle_DELETE_tasks_by_id(reqiest, id):
    session = get_mysql_session()
    result = session.query(db.DataModel).filter_by(id=id).delete()
    if not result:
        return "Missing data by ID", 406
    session.commit()
    return "Data succesfully deleted", 200
