import threading
from state import State

class Follower_state(State, threading.Thread):
    
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
    
    def send_request_vote(self):
        pass
    
    def send_append_entries(self):
        pass
    
    def send_answer(self):
        pass

