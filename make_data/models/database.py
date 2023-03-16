from make_data.extensions import db

class Para_data(db.Model):
    __tablename__='para_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    para = db.Column(db.Text)
    decom = db.relationship('Sent_data', backref='para_data')
    # work = db.relationship('User_only', backref='para_data')
    
    def __init__(self, user_id, para):
        self.user_id = user_id
        self.para = para
        
    def __repr__(self):
        return f'{self.user_id} : {self.para[:20]}'
    
    
class Sent_data(db.Model):
    __tablename__='sent_data'
    
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('para_data.id'))
    sent = db.Column(db.String)
    
    def __init__(self, sent):
        self.sent = sent
        
    def __repr__(self):
        return f'{self.sent}'
    
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