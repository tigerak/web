import json
import openai

from config import Openai_api
from make_data.extensions import db
from make_data.models.database import User_only
        
    
class SendToChatGPT():
    def save_db(self, user_id, query):
        prompt = query['api_prompt'] + ' : '
        completion = query['api_completion']
        
        User_only.query.filter_by(user_id=user_id).delete()
        send_api_data = User_only(user_id, prompt, completion)
        db.session.add(send_api_data)
        db.session.commit()
        
    def make_data(self, user_id):
        prompt = User_only.query.filter_by(user_id=user_id).with_entities(User_only.prompt).first()[0]
        completion = User_only.query.filter_by(user_id=user_id).with_entities(User_only.completion).first()[0]
        
        self.data = {
            "prompt" : prompt,
            "completion" : completion
        }
        return json.dumps(self.data)
    
        
class ChatGPT():
    def __init__(self):
        openai.api_key = Openai_api.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"

    def ping(self, query):
        prompt = query['api_prompt'] + ' : '
        completion = query['api_completion']
        
        params = prompt + completion

        messages = [
                {"role": "user", "content": params}
        ]

        response = openai.ChatCompletion.create(
            model= self.model,
            messages=messages
        )
        answer = response['choices'][0]['message']['content']
        
        return answer