from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime
from pymongo import MongoClient
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/ct'
db = SQLAlchemy(app)
mongo = MongoClient('127.0.0.1', 27017).test

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    content = db.Column(db.Text)
    category = db.relationship('Category', backref='f')

    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content

    def __repr__(self):
        return '<File: %r>' % self.title
    
    def add_tag(self, tag_name):
        filess = mongo.files.find_one({'file_id': self.id})
        if filess:
            tags = filess['tags']
            if tag_name not in tags:
                tags.append(tag_name)
            mongo.files.update_one({'file_id': self.id}, {'$set': {'tags': tags}})
        else:
            tags = [tag_name]
            mongo.files.insert_one({'file_id': self.id, 'tags': tags})

    def remove_tag(self, tag_name):
        filess = mongo.files.find_one({'file_id': self.id})
        tags = filess['tags'].remove(tag_name)
        mongo.files.update_one({'file_id': self.id},{'$set': {'tags': tags}})


    @property
    def tags(self):
        filess = mongo.files.find_one({'file_id': self.id})
        return filess['tags']


@app.route('/')
def index(): 
    lists = []
    files = File.query.all()
    for x in files:
        strs = '{"id":%d,"title":"%s", "tag":"%s"}' % (x.id, x.title,x.tags)
        new = json.loads(strs)
        lists.append(new)
    return render_template('index.html',lists=lists)	


@app.route('/files/<file_id>')
def file(file_id):
    files = File.query.get(file_id)
    if files != None:
        content = str(files.content)
        time = str(files.created_time)
        info = str((Category.query.get(files.category_id)).name)
        tag = str(files.tags)
        return render_template('file.html', content=content, time=time, info=info, tag=tag)
    else:
        abort(404)
	
@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404




if __name__ == '__main__':
    app.run()
