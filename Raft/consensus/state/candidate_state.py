
import threading
from Raft.consensus.state.state import State

class Condidate_state(State, threading.Thread):
    
    def __init__(self, consensus):
        self.vote = []
        self.consensus = consensus
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
    
    def run(self):
    
        self.vote.append(self.consensus.id)
        # TODO send paraller
    
    def receive_request_vote(self, message): 
        self.send_answer("Reject")
    
    def receive_append_entries(self, message, destination_id):
        
        # How about the message has log?
        if message["term"] >= self.consensus.term: # TODO also last index and term
            # changing voted for
            self.consensus.voted_for = message["term"]
            self.send_append_entries_answer("Accept", message["id"])
            self.consensus.set_state("Follower")
        else:
            self.send_append_entries_answer("Reject", message["id"])
            
    def receive_request_vote_answer(self, message):
        
        if message["Answer"] == "Accept":
            
            self.vote.append(message["Id"])
            
            if len(self.vote) > self.consensus.number_of_nodes/2:
                
                self.consensus.set_state("Leader")
                
        elif message["term"] > self.consensus.current_term:
            
            self.consensus.current_term = message["term"]
    
    def receive_append_entries_answer(self, message):
        # TODO rise exception
        pass
        
    def receive_client_message(self, message):
        # TODO rise exception
        pass
            
    def send_request_vote(self):
        message = {}
        message["term"] = self.consensus.term
        message["id"]  = self.consensus.id
        message["Last Log Term"] = self.consensus.last_log_term
        message["Last Log Id"] = self.consensus.last_log_index
        self.consensus.send_request_vote(message)
        
    def send_append_entries(self, entries: list):
        # TODO rise exception
        pass