from consensus import Consensus

class State: 
    
    def __init__(self, consensus: Consensus):
        
        self.consensus = consensus
    
    def run(self): 
        pass
    
    def receive_request_vote(self, message): 
        pass
    
    def receive_append_entries(self, message):
        pass
    
    def receive_answer(self, message):
        pass
    
    def receive_client_message(self, message):
        pass
    
    def send_request_vote(self):
        pass
    
    def send_append_entries(self, entries: list):
        pass
    
    def send_answer(self):
            
        messsage = {}
        message["kind"] = "Answer"
        message["Answer"] = answer
        message["term"] = self.consensus.term
        message["Id"] = self.consensus.id
            
        self.consensus.send_message(message)
    
