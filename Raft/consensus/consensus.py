import signal
import random
from queue import Queue
from state.follower_state import Follower_state
from state.candidate_state import Condidate_state
from state.leader_state import Leader_state
from state.state import State
import json 

class Consensus:
    
    def __init__(self, id):
        self.id = id
        self.log = Log() # TODO
        self.current_term = 0
        self.state = Follower_state(self) # TODO out  put of init
        self.send_queue = Queue() # queue which subscriber put message in it
        self.receive_queue = Queue()
        self.voted_for = null
        self.last_log_term = -1 # save last index and term in receive TODO
        self.last_log_id = -1
        self.number_of_nodes = 3
        self.commit_index = 0
        self.last_applied = 0
        
    def __handler(self, signum, frame):
        print('Signal handler called with signal', signum) # Test
        self.__reset_timeout()
        self.set_state("Candidate")
        
    # Listen to its queue
    def start(self):
        
        self.__reset_timeout()
        while(True):
            
            if len(self.receive_queue) != 0:
                
                message = null # TODO reciever
                
                if message["kind"] == "Append Entries":
                    self.__reset_timeout()
                    self.state.receive_append_entries(message)
                    
                elif message["kind"] == "Request Vote":
                    self.__reset_timeout()
                    self.state.receive_request_vote(message)
                    
                elif message["kind"] == "Answer":
                    self.state.receive_answer(message)
                    
                elif message["kind"] == "Client":
                    self.state.receive_client_message(message)
                
                else:
                    # TODO rise exception
                    pass
                
         
    def __reset_timeout(self):
        timeout = random.randint(7, 14)
        signal.signal(signal.SIGALRM, self.__handler)
        signal.alarm(timeout)
    
    def set_state(self, kind):
        
        del self.state
        
        if kind == "Candidate":
            self.state = Condidate_state(self)
        elif kind == "Leader":
            self.state = Leader_state(self)
        elif kind == "Follower":
            self.state = Follower_state(self)
        else:
            # TODO rise exception
            pass
        self.state.start()
        
    def send_message(self, message: dict):
        string_message = json.dumps(message, indent=4)
        pass
    
    def receive_message(self):
        # dictionary_message = json.loads(jsonString)
        pass
                
                
