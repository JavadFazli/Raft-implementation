import threading
from Raft.consensus.state.state import State
import time

class Follower_state(State, threading.Thread):
    
    def __init__(self, consensus):
        
        self.consensus = consensus
        threading.Thread.__init__(self)
        State.__init__(self, consensus)

    def run(self): 
        print("Follower state !!!")
        pass
    
    def receive_request_vote(self, message): 
        
        if message["term"] > self.consensus.current_term and message["Last_Log_Term"] >= self.consensus.last_log_term and message["Last_Log_Id"] >= self.consensus.last_log_index and self.consensus.voted_for == None:
            self.consensus.voted_for = message["id"]
            self.send_request_vote_answer("Accept", message["id"])
            self.consensus.current_term = message["term"]
            
        else:
            self.send_request_vote_answer("Reject", message["id"])
    
    def receive_append_entries(self, message):
        
        if message["term"] < self.consensus.current_term:
            self.send_append_entries_answer("Reject", message["id"])
            
        else:
            # Check commit
            if message["Leader_Commite"] > self.consensus.commit_index:
                while self.consensus.commit_index < message["Leader_Commite"]:
                    self.consensus.log.delete_log_by_index(self.consensus.commit_index)
                    self.consensus.commit_index -= 1
                self.consensus.commit_index = message["Leader_Commite"]
            
            # Heartbeat
            if message["Entries"] == "":
                print("Heartbeat !!!")
                self.consensus.voted_for = None
                self.consensus.leader = message["id"]
            
            else:
                
                # Log isn't update
                if message["Prev_Log_Term"] == self.consensus.last_log_term and message["Prev_Log_Id"] != self.consensus.last_log_index:
                    self.send_append_entries_answer("Reject", message["id"])
                    return
                    
                elif message["Prev_Log_Term"] != self.consensus.last_log_term:
                    # TODO delete current entry
                    self.send_append_entries_answer("Reject", message["id"])
                    pass
                
                else:
                    self.consensus.last_log_index += 1
                    self.consensus.last_log_term = message["term"]
                    message["index"] = self.consensus.last_log_index
                    self.send_append_entries_answer("Accept", message["id"])
                    self.consensus.log.store(message)
    
    def receive_request_vote_answer(self, message):
        raise Exception("Receive Request Vote Answer is not valid for Follower !!!!")  
    
    def receive_append_entries_answer(self, message):
        raise Exception("Receive Append Entries Answer is not valid for Follower !!!!")
    
    def receive_client_message(self, message):
        raise Exception("Receive Client Message is not valid for Follower !!!!")
    
    def send_request_vote(self):
        raise Exception("Send Request Vote is not valid for Follower !!!!")
    
    def send_append_entries(self, entries: list, destination_id):
        raise Exception("Send Append Entries is not valid for Follower !!!!")

