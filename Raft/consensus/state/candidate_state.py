
import threading
from state import State
from consensus import Consensus

class Condidate_state(State, threading.Thread):
    
    def __init__(self, consensus: Consensus):
        self.vote = []
        self.consensus = consensus
    
    def run(self):
    
        self.vote.append(self.consensus.id)
        
        # TODO send paraller
    
    def receive_request_vote(self, message): 
        self.send_answer("Reject")
    
    def receive_append_entries(self, message):
        
        # How about the message has log?
        if int(message[1]) >= self.consensus.term: # TODO also last index and term
            # changing voted for
            self.consensus.voted_for = int(message[2])
            self.send_answer("Accept")
            self.consensus.set_state("Follower")
        else:
            self.send_answer("Reject")
        
    def receive_answer(self, message):
        
        if message[1] == "Accept":
            
            self.vote.append(int(message[3]))
            
            if len(self.vote) > self.consensus.number_of_nodes/2:
                
                self.consensus.set_state("Leader")
            
    
    def send_request_vote(self):
        message = "Request Vote" + "#" + str(self.consensus.term) + "#" + str(self.consensus.id) + "#" +  str(self.consensus.last_log_term) + "#" + str(self.consensus.last_log_id) #remain
        self.consensus.send_message(message)
        
    def send_append_entries(self):
        # TODO rise exception
        pass
    
    def send_answer(self, answer):
        
        if answer == "Accept":
            message = "Answer" + "#" + "Accept" + "#" + str(self.consensus.term) + "#" + str(self.consensus.id)
            self.consensus.send_message(message)
            
        elif answer == "Reject":
            message = "Answer" + "#" + "Reject" + "#" + str(self.consensus.term) + "#" + str(self.consensus.id)
            self.consensus.send_message(message)
            
        else:
            # TODO rise exception
            pass