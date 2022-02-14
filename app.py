from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#create models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)


# Create data abstraction layer
class TaskSchema(Schema):
    id = fields.Integer()
    title = fields.Str(required=True)
    description = fields.Str()

    class Meta:
        type_ = 'tasks'
        self_view = 'task_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'tasks_many'
    

class TaskMany(ResourceList):
    schema = TaskSchema
    data_layer = {'session': db.session,
                  'model': Task}

class TaskOne(ResourceDetail):
    schema = TaskSchema
    data_layer = {'session': db.session,
                  'model': Task}

db.create_all()

api = Api(app)
api.route(TaskMany, 'tasks_many', '/tasks')
api.route(TaskOne, 'task_one', '/task/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
