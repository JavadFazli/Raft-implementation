import signal
import random
from queue import Queue
from state.follower_state import Follower_state
from state.candidate_state import Condidate_state
from state.leader_state import Leader_state

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
        
    def __handler(signum, frame):
        print('Signal handler called with signal', signum) # Test
        self.__reset_timeout()
        self.set_state("Candidate")
        
    # Listen to its queue
    def start(self):
        
        self.__reset_timeout()
        while(True):
            
            if len(self.receive_queue) != 0:
                
                message = null # TODO reciever
                content = message.spilt("#")
                
                if content[0] == "Append Entries":
                    self.__reset_timeout()
                    self.state.receive_append_entries(content)
                    
                elif content[0] == "Request Vote":
                    self.__reset_timeout()
                    self.state.receive_request_vote(content)
                    
                elif content[0] == "Answer":
                    self.state.receive_answer(content)
                
                else:
                    # TODO rise exception
                    pass
                
         
    def __reset_timeout(self):
        timeout = random.randint(150, 300)/1000
        signal.setitimer(signal.ITIMER_REAL, timeout) #WHERE IS HANDLER??? TODO
    
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
        
    def send_message(self, message):
        pass
    
    def receive_message(self):
        pass
                
                
