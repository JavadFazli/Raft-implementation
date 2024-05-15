import threading
from Raft.consensus.state.state import State
import numpy as np

class Leader_state(State, threading.Thread):

    def __init__(self, consensus):
        
        self.consensus = consensus
        self.next_index = np.full(shape=self.consensus.number_of_nodes-1, fill_value=1+self.consensus.last_log_index, dtype=np.int)
        self.match_index = np.zeros(self.consensus.number_of_nodes)
        
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
        
    
    def run(self):
         
        for destination_index in range(self.next_index):
            threading.Thread(target=self.send_append_entries, args=("", destination_index)).start()
        
        self.__heartbeat()
    
    def receive_request_vote(self, message): 
        # TODO rise exception
        pass
    
    def receive_append_entries(self, message):
        # TODO rise exception
        pass
                
    
    def receive_request_vote_answer(self, message):
        # TODO rise exception
        pass

    
    def receive_append_entries_answer(self, message):

        if message["Answer"] == "Accept":
            
            self.next_index[message["Id"]] += 1
            
            if self.consensus.last_log_index >= self.next_index[message["Id"]]:
                
                self.send_append_entries("get", message["Id"]) #TODO get entry
                
            
        if message["Answer"] == "Reject":
            
            if self.consensus.current_term < message["term"]:
                
                self.consensus.set_state("Follower")
                self.consensus.state.start()
                
            else:
                self.next_index[message["Id"]] -= 1
                self.send_append_entries("get", message["Id"]) #TODO get entry
            
        
    def receive_client_message(self, message):
        
        self.consensus.last_log_index += 1
        self.consensus.last_log_term = self.consensus.current_term
        self.consensus.log.store(message) # TODO Type of message is considered string
        self.__send_to_all()
        
    
    def send_request_vote(self):
        # TODO rise exception
        pass
    
    def send_append_entries(self, entries: list, destination_id):
        
        message = {}
        message["term"] = self.consensus.term
        message["id"]  = self.consensus.id
        message["Destination Id"] = destination_id
        message["Prev Log Term"] = -1 # TODO
        message["Prev Log Id"] = -1 # TODO
        message["Entries"] = s = '#'.join(entries)
        message["Leader Commite"] = self.consensus.commit_index

        self.consensus.send_append_entries(message)
        
        
    def __handler(self, signum, frame):
        
        self.__heartbeat()
        for destination_index in range(self.next_index):
            threading.Thread(target=self.send_append_entries, args=("", destination_index)).start()
        
    def __heartbeat(self):
        signal.signal(signal.SIGALRM, self.__handler)
        signal.alarm(3)
        
    def __commiting_log(self):
        # TODO
        pass
    
    def __send_to_all(self):
        
        for destination_index in range(self.next_index):
            
            if self.next_index[destination_index] <= self.consensus.last_log_index:
                
                threading.Thread(target=self.send_append_entries, args=(10, destination_index)).start() # TODO get next_index entry
                
