from make_web.extensions import db
from datetime import datetime


class Text_data(db.Model):
    __tablename__='text_data'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64))
    text = db.Column(db.Text)
    s_w = db.relationship('Sent_data', backref='text_data')
    
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        
    def __repr__(self):
        return f'{self.user_id} : {self.text[:20]}'
    
    # QueryObject type -> Dictionary
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
    
    
class Sent_data(db.Model):
    __tablename__='sent_data'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer, db.ForeignKey('text_data.id'))
    sent = db.Column(db.Text)
    k_w = db.relationship('Key_data', backref='sent_data')
    p_w = db.relationship('Point_data', backref='sent_data')
    
    def __init__(self, sent):
        self.sent = sent
        
    def __repr__(self):
        return f'{self.sent}'
    
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
    
    
class Key_data(db.Model):
    __tablename__='key_data'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('sent_data.id'))
    key = db.Column(db.String(255))
    p_w = db.relationship('Point_data', backref='key_data')
    
    def __init__(self, key):
        self.key = key
        
    def __repr__(self):
        return f'{self.key}'
    
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
    
    
class Point_data(db.Model):
    __tablename__='point_data'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('sent_data.id'))
    k_id = db.Column(db.Integer, db.ForeignKey('key_data.id'))
    point = db.Column(db.String(255))
    
    def __init__(self, point):
        self.point = point
        
    def __repr__(self):
        return f'{self.point}'
    
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}
    
    
class User_only(db.Model):
    __tablename__='user_only'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.String(64))
    prompt = db.Column(db.Text)
    completion = db.Column(db.Text)
    
    def __init__(self, user_id, prompt, completion):
        self.user_id = user_id
        self.date = datetime.now()
        self.prompt = prompt
        self.completion = completion
        
    def __repr__(self):
        return f'{self.user_id}'
    
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}