import threading
from state import State
import numpy as np
from consensus import Consensus

class Leader_state(State, threading.Thread):

    def __init__(self, consensus: Consensus):
        
        self.consensus = consensus
        self.next_index = np.full(shape=self.consensus.number_of_nodes, fill_value=1+self.consensus.last_log_id, dtype=np.int)
        self.match_index = np.zeros(self.consensus.number_of_nodes)
        
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
        
    
    def run(self): 
        
        self.__heartbeat()
    
    def receive_request_vote(self, message): 
        # TODO rise exception
        pass
    
    def receive_append_entries(self, message):
        # TODO rise exception
        pass
    
    def receive_answer(self, message):

        if message["Answer"] == "Accept":
            # TODO and check for commiting
            pass
        
        elif message["Answer"] == "Reject":
            # TODO
            pass
            
        
    def receive_client_message(self, message):
        # TODO add it to log
        pass
    
    def send_request_vote(self):
        # TODO rise exception
        pass
    
    def send_append_entries(self, entries: list):
        
        message = {}
        message["kind"] = "Append Entries"
        message["term"] = self.consensus.term
        message["id"]  = self.consensus.id
        message["Prev Log Term"] = 0 # TODO
        message["Prev Log Id"] = 0 # TODO
        message["Entries"] = s = '#'.join(entries)
        message["Leader Commite"] = self.consensus.commit_index
        
        self.consensus.send_message(message)
        
        
    def __handler(self, signum, frame):
        
        self.__heartbeat()
        
        # TODO send heartbeat message (call send_append_entries with null entries)
        
    def __heartbeat(self):
        signal.signal(signal.SIGALRM, self.__handler)
        signal.alarm(3)
        
    def __commiting_log(self):
        # TODO
        pass
