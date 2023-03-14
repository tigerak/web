import json

class ChatGPT():
    def __init__(self, para):
        self.para = para
        
    def send(self):
        temp = {
            'content' : self.para
        }
        param = json.dumps(temp)
        
        return param