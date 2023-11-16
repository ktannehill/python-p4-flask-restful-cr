#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        response_dict = {
            'message': 'Welcome to the Newsletter RESTful API'
        }
        return response_dict, 200
    
api.add_resource(Home, '/')

class Newsletters(Resource):
    def get(self):
        resp_dict_list = [news.to_dict() for news in Newsletter.query.all()]
        return resp_dict_list, 200
    
    def post(self):
        new_record = Newsletter(
            title = request.form['title'],
            body = request.form['body']
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record.to_dict(), 201
    
api.add_resource(Newsletters, '/newsletters')

class NewsletterByID(Resource):
    def get(self, id):
        resp_dict = db.session.get(Newsletter, id).to_dict()
        return resp_dict, 200
    
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
