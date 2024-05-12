
import threading
from state import State
from consensus import Consensus

class Condidate_state(State, threading.Thread):
    
    def __init__(self, consensus: Consensus):
        self.vote = []
        self.consensus = consensus
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
    
    def run(self):
    
        self.vote.append(self.consensus.id)
        
        # TODO send paraller
    
    def receive_request_vote(self, message): 
        self.send_answer("Reject")
    
    def receive_append_entries(self, message):
        
        # How about the message has log?
        if message["term"] >= self.consensus.term: # TODO also last index and term
            # changing voted for
            self.consensus.voted_for = message["term"]
            self.send_answer("Accept")
            # TODO check log
            self.consensus.set_state("Follower")
        else:
            self.send_answer("Reject")
        
    def receive_answer(self, message):
        
        if message["Answer"] == "Accept":
            
            self.vote.append(message["Id"])
            
            if len(self.vote) > self.consensus.number_of_nodes/2:
                
                self.consensus.set_state("Leader")
                
        elif message["term"] > self.consensus.current_term:
            # TODO update term?
            pass
        
    def receive_client_message(self, message):
        # TODO rise exception
        pass
            
    
    def send_request_vote(self):
        message = {}
        message["kind"] = "Request Vote"
        message["term"] = self.consensus.term
        message["id"]  = self.consensus.id
        message["Last Log Term"] = self.consensus.last_log_term
        message["Last Log Id"] = self.consensus.last_log_id
        self.consensus.send_message(message)
        
    def send_append_entries(self, entries: list):
        # TODO rise exception
        pass