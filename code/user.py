class User:
    def __init__(self,_id, username, password):
        self.id = _id #using _id since id is a keyword in python
        self.username = username
        self.password = password
