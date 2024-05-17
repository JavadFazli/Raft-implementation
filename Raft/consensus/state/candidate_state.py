
import threading
from Raft.consensus.state.state import State

class Condidate_state(State, threading.Thread):
    
    def __init__(self, consensus):
        self.vote = []
        self.consensus = consensus
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
    
    def run(self):
        print("we are in candidate !!!")
        self.vote.append(self.consensus.id)
        for destination_id in range(self.consensus.number_of_nodes):
            if destination_id != self.consensus.id:
                self.send_request_vote(destination_id)
                # threading.Thread(target=self.send_request_vote, args=(destination_id)).start()
    
    def receive_request_vote(self, message): 
        self.send_request_vote_answer("Reject", message["id"])
    
    def receive_append_entries(self, message):
        
        # How about the message has log?
        if message["term"] >= self.consensus.current_term and message["Prev_Log_Term"] >= self.consensus.last_log_term and message["Prev_Log_Id"] >= self.consensus.last_log_index:
            # changing leader
            self.consensus.leader = message["id"]
            self.consensus.voted_for = None
            self.send_append_entries_answer("Accept", message["id"])
            self.consensus.set_state("Follower")
        else:
            self.send_append_entries_answer("Reject", message["id"])
            
    def receive_request_vote_answer(self, message):
        
        if message["Answer"] == "Accept":
            
            self.vote.append(message["id"])
            
            if len(self.vote) > self.consensus.number_of_nodes/2: 
                self.consensus.set_state("Leader")
                
        elif message["term"] > self.consensus.current_term:
            self.consensus.current_term = message["term"]
    
    def receive_append_entries_answer(self, message):
        raise Exception("Receive Append Entries Answer is not valid for Candidate !!!!")
        
    def receive_client_message(self, message):
        raise Exception("Receive Client Message is not valid for Candidate !!!!")
            
    def send_request_vote(self, destination_id):
        message = {}
        message["term"] = self.consensus.current_term
        message["id"]  = self.consensus.id
        message["Last_Log_Term"] = self.consensus.last_log_term
        message["Last_Log_Id"] = self.consensus.last_log_index
        message["Destination_Id"] = destination_id
        self.consensus.send_request_vote(message)
        
    def send_append_entries(self, entries: list):
        raise Exception("Send Append Entries is not valid for Candidate !!!!")