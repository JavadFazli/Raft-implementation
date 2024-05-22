import threading
from Raft.consensus.state.state import State
import numpy as np
import signal
import time
from Raft.app.config import (Config)

class Leader_state(State, threading.Thread):

    def __init__(self, consensus):
        
        self.consensus = consensus
        self.next_index = np.full(shape=self.consensus.number_of_nodes, fill_value=self.consensus.last_log_index+1, dtype=int)
        self.match_index = np.zeros(self.consensus.number_of_nodes)
        self.flag = False
        
        threading.Thread.__init__(self)
        State.__init__(self, consensus)
        
        print("I'm a leader now !!") 
    
    def run(self):
        # threading.Thread(target=self.__heartbeat).start()
        pass
    
    def receive_request_vote(self, message): 
        raise Exception("Receive Request Vote is not valid for Leader !!!!") 
    
    def receive_append_entries(self, message):
        raise Exception("Receive Append Entries is not valid for Leader !!!!")        
    
    def receive_request_vote_answer(self, message):
        raise Exception("Receive Request Vote Answer is not valid for Leader !!!!") 
    
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
        
        message["index"] = self.consensus.last_log_index+1
        message["term"] = self.consensus.current_term
        message["Leader_Commite"] = self.consensus.commit_index
        message["Prev_Log_Term"] = self.consensus.last_log_term
        message["Prev_Log_Id"] = self.consensus.last_log_index
        message["id"]  = self.consensus.id
        message["Destination_Id"] = self.consensus.id
        
        self.consensus.log.store(message)
        self.consensus.last_log_index += 1
        self.consensus.last_log_term = self.consensus.current_term
        
        if self.flag == False:
            self.flag = True
            self.__send_to_all()
        
    
    def send_request_vote(self):
        raise Exception("Send Request Vote Answer is not valid for Leader !!!!") 
    
    def send_append_entries(self, message_idex, destination_id):
        
        # It's heartbeat
        if message_idex == -1:
            message = {}
            message["kind"] = "AppendEntries"
            message["index"] = -1
            message["term"] = self.consensus.current_term
            message["id"] = self.consensus.id
            message["Leader_Commite"] = self.consensus.commit_index
            message["Destination_Id"] = destination_id
            message["Prev_Log_Term"] = self.consensus.last_log_term
            message["Prev_Log_Id"] = self.consensus.last_log_index
            message["Entries"] = ""
        
        else:

            message = self.consensus.log.find_log_by_index(int(message_idex))
            message["Destination_Id"] = destination_id
            message["Leader_Commite"] = self.consensus.commit_index
            message["kind"] = "AppendEntries"


        self.consensus.send_append_entries(message)
        
    def __heartbeat(self):
        
        while(True):
            
            for destination_index in range(len(self.next_index)):
                if destination_index != self.consensus.id:
                    threading.Thread(target=self.send_append_entries, args=(-1, destination_index)).start()
            
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
        
        print("Sending to all ended")        
        self.flag = False
                
