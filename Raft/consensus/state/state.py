

class State: 
    
    def __init__(self, consensus):
        
        self.consensus = consensus
    
    def run(self): 
        pass
    
    def receive_request_vote(self, message): 
        pass
    
    def receive_append_entries(self, message):
        pass
    
    def receive_request_vote_answer(self, message):
        pass
    
    def receive_append_entries_answer(self, message):
        pass
    
    def receive_client_message(self, message):
        pass
    
    def send_request_vote(self):
        pass
    
    def send_append_entries(self, entries: list, destination_id):
        pass
      
    def send_request_vote_answer(self, answer, destination_id):
        
        message = {}
        message["Answer"] = answer
        message["term"] = self.consensus.current_term
        message["Destination_Id"] = destination_id
        message["Id"] = self.consensus.id
            
        self.consensus.send_request_vote_answer(message)
    
    def send_append_entries_answer(self, answer,  destination_id):
        
        message = {}
        message["Answer"] = answer
        message["term"] = self.consensus.current_term
        message["Destination_Id"] = destination_id
        message["Id"] = self.consensus.id
            
        self.consensus.send_append_entries_answer(message)
            

    
