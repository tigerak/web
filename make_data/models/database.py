from make_data.extensions import db

class Para_data(db.Model):
    __tablename__='para_data'
    
    id = db.Column(db.Integer, primary_key=True)
    para = db.Column(db.Text)
    decom = db.relationship('Sent_data', backref='para_data')
    
    def __init__(self, para):
        self.para = para
        
    def __repr__(self):
        return f'{self.para}'
    
    
class Sent_data(db.Model):
    __tablename__='sent_data'
    
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('para_data.id'))
    sent = db.Column(db.String)
    
    def __init__(self, sent):
        self.sent = sent
        
    def __repr__(self):
        return f'{self.sent}'