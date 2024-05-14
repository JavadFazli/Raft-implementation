import signal
import random
from Raft.consensus.log import Log
from Raft.broker.queue import RedisQueue
from Raft.consensus.state.follower_state import Follower_state
from Raft.consensus.state.candidate_state import Condidate_state
from Raft.consensus.state.leader_state import Leader_state
# from Raft.rpc.client import RaftClient
import json 

class Consensus:
    
    def __init__(self, id):
        self.id = id
        self.log = Log()
        self.current_term = 0
        self.state = Follower_state(self) # TODO out  put of init
        # self.send_queue = RedisQueue() # queue which subscriber put message in it
        self.receive_queue = RedisQueue(host='0.0.0.0', port=6379, db=0)
        self.voted_for = None
        self.last_log_term = -1 # save last index and term in receive TODO
        self.last_log_index = -1
        self.number_of_nodes = 3
        self.commit_index = 0
        self.last_applied = 0
        # self.client = RaftClient()
        
    def __handler(self, signum, frame):
        print('Signal handler called with signal', signum) # TODO delete Test
        self.__reset_timeout()
        self.set_state("Candidate")
        
    # TODO Listen to its queue
    def start(self):
        
        self.__reset_timeout()
        while(True):
            
            # TODO condition
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
        
    
    def send_request_vote(self, message: dict):
        pass
    
    def send_append_entries(self, message: dict):
        pass
    
    def send_request_vote_answer(self, message: dict):
        pass
    
    def send_append_entries_answer(self, message: dict):
        pass 

    def receive_request_vote(self):
        pass
    
    def receive_append_entries(self):
        pass
    
    def receive_request_vote_answer(self):
        pass
    
    def receive_append_entries_answer(self):
        pass
                
                
