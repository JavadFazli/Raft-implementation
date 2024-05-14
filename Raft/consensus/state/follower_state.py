import threading
from Raft.consensus.state.state import State

class Follower_state(State, threading.Thread):
    
    def __init__(self, consensus):
        
        self.consensus = consensus
        threading.Thread.__init__(self)
        State.__init__(self, consensus)

    
    def run(self): 
        pass
    
    # TODO delete after test
    def Test(self):
        print("run of follower state")
    
    def receive_request_vote(self, message): 
        
        if message["term"] > self.consensus.current_term:
            self.send_request_vote_answer("Accept", message["id"])
            
        else:
            self.send_append_entries_answer("Reject", message["id"])
    
    def receive_append_entries(self, message):
        
        if message["term"] < self.consensus.current_term:
            self.send_append_entries_answer("Reject", message["id"])
            
        else:
            
            # Check commit
            if message["Leader Commite"] > self.consensus.commit_index:
                # TODO delete log
                self.consensus.commit_index = message["Leader Commite"]
            
            # Heartbeat
            if message["Entries"] == "":
                
                self.consensus.voted_for = message["id"]
            
            else:
                
                # Log isn't update
                if message["Prev Log Term"] == self.consensus.last_log_term and message["Prev Log Id"] != self.consensus.last_log_index:
                    self.send_append_entries_answer("Reject", message["id"])
                    return
                    
                elif message["Prev Log Term"] != self.consensus.last_log_term:
                    # TODO delete current entry
                    self.send_append_entries_answer("Reject", message["id"])
                    pass
                
                else:
                    self.consensus.last_log_index += 1
                    self.consensus.last_log_term = message["term"]
                    self.consensus.log.store(message["Entries"])
                    self.send_append_entries_answer("Accept", message["id"])
    
    def receive_request_vote_answer(self, message):
        
        if message["term"] > self.consensus.current_term:
            
            self.consensus.voted_for = message["id"]
            self.send_request_vote_answer("Accept", message["id"])
            self.consensus.current_term = message["term"]
            
        else:
            self.send_request_vote_answer("Accept", message["id"])
            
    
    def receive_append_entries_answer(self, message):
        # TODO rise exception
        pass
    
    def receive_client_message(self, message):
        # TODO rise exception
        pass
    
    def send_request_vote(self):
        # TODO rise exception
        pass
    
    def send_append_entries(self, entries: list, destination_id):
        # TODO rise exception
        pass
