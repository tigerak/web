def decomposition(paragraph):
    sentences = paragraph.split('. ')
    sentence_dict ={} 
    for s_k, sent in enumerate(sentences):
        if len(sent) > 1:
            sentence_dict[s_k] = sent
        else:
            pass
    return sentence_dict


import re
def classification(form):
    get_keys = []
    key_list = []
    point_list = []
    
    for k in form.keys():
        get_keys.append(k)
        
    for u_k in get_keys:
        value = form[u_k]
        
        u_k_list = u_k.split('_')
        t_k = u_k_list[0]
        s_k = u_k_list[1]
        
        md = re.sub('\n', '', value)
        md = re.sub('\r', '', md)
        
        k_p = re.compile(f'(?<=\"KeyHighlight_{s_k}">)(.*?)(?=<\/span>)')
        p_p = re.compile(f'(?<=\"PointHighlight_{s_k}">)(.*?)(?=<\/span>)')
        
        key_list = k_p.findall(md)
        point_list = p_p.findall(md)
        
    return t_k, s_k, key_list, point_list


# from sqlalchemy import desc, and_
from models import Text_data, Sent_data, Point_data, Key_data
from extensions import db
class DB_edit():
    def __init__(self):
        pass

    def delete_text(self, del_text):
        empty_test = Key_data.query.filter_by(t_id=del_text).all()
        if len(empty_test) != 0:
            del_k_id = self.sum_num(empty_test)
            Point_data.query.filter(Point_data.k_id.in_(del_k_id)).delete()
            Key_data.query.filter_by(t_id=del_text).delete()
        Sent_data.query.filter_by(t_id=del_text).delete()
        Text_data.query.filter_by(id=del_text).delete()
        db.session.commit()

    def delete_key(self, del_key):
        Point_data.query.filter_by(k_id=del_key).delete()
        Key_data.query.filter_by(id=del_key).delete()
        db.session.commit()

    def db_search(self, t_id_list, p_t_num):
        
        p_t_id = int(t_id_list[-p_t_num])

        T_items = Text_data.query.filter_by(id=p_t_id).all()        
        S_items = Sent_data.query.filter_by(t_id=p_t_id).\
                                order_by(Sent_data.s_id).all()
        K_items = Key_data.query.filter_by(t_id=p_t_id).\
                                order_by(Key_data.id).all()
        k_id = self.sum_num(K_items)
        P_items = Point_data.query.filter(Point_data.k_id.in_(k_id)).\
                                order_by(Point_data.k_id).all()

        return T_items, S_items, K_items, P_items

    def sum_num(self, items):
        i_list = []
        for i in items:
            i_list.append(str(i))
        return i_list
    
    def check_p_t(self, p_t_num, total_text_num):
        if p_t_num < 1:
            p_t_num = 1
        elif p_t_num > total_text_num:
            p_t_num = total_text_num
        else:
            pass
        return p_t_num

### Load KoGPT Tokenizer
# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained(
#     'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
#     bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
#     )

# Deconposition : paragraph -> token
# def decomposition(paragraph):
#     sentences = paragraph.split('.')
#     output_list = []
#     for s_k, sent in enumerate(sentences):
#         input_idx = tokenizer.encode(sent)
#         output = {}
#         for w_k, i in enumerate(input_idx):
#             out = tokenizer.decode(i)
#             make_key = str(s_k) + '_' + str(w_k) + '_' + out
#             output[make_key] = out
#         output_list.append(output)
#     return output_list


### KoBERT Tokenizer
# from kobert.utils import get_tokenizer
# from kobert.pytorch_kobert import get_pytorch_kobert_model

# import gluonnlp as nlp

# bertmodel, vocab = get_pytorch_kobert_model()
# tokenizer = get_tokenizer()
# tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)