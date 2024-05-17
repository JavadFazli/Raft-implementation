import threading
from Raft.consensus.state.state import State
import numpy as np
import signal
import time
from Raft.app.config import (Config)

class Leader_state(State, threading.Thread):

    def __init__(self, consensus):
        
        self.consensus = consensus
        self.next_index = np.full(shape=self.consensus.number_of_nodes, fill_value=1+self.consensus.last_log_index, dtype=int)
        self.match_index = np.zeros(self.consensus.number_of_nodes)
        self.flag = False
        
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
        
        print("I'm a leader now !!") 
    
    def run(self):
        # TODO uncomment it
        # threading.Thread(target=self.__heartbeat)
        pass
    
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
            
            self.next_index[message["id"]] += 1
            
            if self.consensus.last_log_index >= self.next_index[message["id"]]:
                self.send_append_entries(self.next_index[message["id"]], message["id"]) #TODO get entry
                
            
        if message["Answer"] == "Reject":
            
            if self.consensus.current_term < message["term"]:
                print("change to follower")
                self.consensus.set_state("Follower")
                
            else:
                self.next_index[message["id"]] -= 1
                self.send_append_entries(self.next_index[message["id"]], message["id"]) #TODO get entry    
        
    def receive_client_message(self, message):
        
        self.consensus.last_log_index += 1
        self.consensus.last_log_term = self.consensus.current_term
        if self.flag == False:
            self.flag = True
            self.__send_to_all()
        message["index"] = self.consensus.last_log_index
        message["term"] = self.consensus.last_log_term
        # self.consensus.log.store(message)
    
    def send_request_vote(self):
        # TODO rise exception
        pass
    
    def send_append_entries(self, message_idex, destination_id):
        
        message = {}
        message["term"] = self.consensus.current_term
        message["id"]  = self.consensus.id
        message["Destination_Id"] = destination_id
        message["Prev_Log_Term"] = self.consensus.last_log_term
        message["Prev_Log_Id"] = self.consensus.last_log_index
        message["Entries"] =  message_idex
        # TODO True one:
        # message["Entries"] = self.consensus.log.find_log_by_index(message_idex)["log_entry"]
        message["Leader_Commite"] = self.consensus.commit_index

        self.consensus.send_append_entries(message)
        
    def __heartbeat(self):
        
        while(True):
            for destination_index in range(len(self.next_index)):
                threading.Thread(target=self.send_append_entries, args=("", destination_index)).start()
            
            time.sleep(Config.HEARTBEAT)
        
    def __commiting_log(self):
        # TODO
        pass
    
    def __send_to_all(self):

        for destination_id in range(len(self.next_index)):
            
            if self.next_index[destination_id] <= self.consensus.last_log_index and destination_id != self.consensus.id:
                print("sending !!")
                threading.Thread(target=self.send_append_entries, args=(self.next_index[destination_id], destination_id)).start()
                self.next_index[destination_id] += 1
                
        self.flag = False
                
