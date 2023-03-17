from make_data.extensions import db

class Text_data(db.Model):
    __tablename__='text_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    text = db.Column(db.Text)
    s_w = db.relationship('Sent_data', backref='text_data')
    
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        
    def __repr__(self):
        return f'{self.user_id} : {self.text[:20]}'
    
class Sent_data(db.Model):
    __tablename__='sent_data'
    
    id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer, db.ForeignKey('text_data.id'))
    sent = db.Column(db.Text)
    k_w = db.relationship('Key_data', backref='sent_data')
    p_w = db.relationship('Point_data', backref='sent_data')
    
    def __init__(self, sent):
        self.sent = sent
        
    def __repr__(self):
        return f'{self.sent}'
    
    
class Key_data(db.Model):
    __tablename__='key_data'
    
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('sent_data.id'))
    key = db.Column(db.String)
    p_w = db.relationship('Point_data', backref='key_data')
    
    def __init__(self, key):
        self.key = key
        
    def __repr__(self):
        return f'{self.key}'
    
class Point_data(db.Model):
    __tablename__='point_data'
    
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey('sent_data.id'))
    k_id = db.Column(db.Integer, db.ForeignKey('key_data.id'))
    point = db.Column(db.String)
    
    def __init__(self, point):
        self.point = point
        
    def __repr__(self):
        return f'{self.point}'
    
class User_only(db.Model):
    __tablename__='user_only'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    prompt = db.Column(db.Text)
    completion = db.Column(db.Text)
    
    def __init__(self, user_id, prompt, completion):
        self.user_id = user_id
        self.prompt = prompt
        self.completion = completion
        
    def __repr__(self):
        return f'{self.user_id}'