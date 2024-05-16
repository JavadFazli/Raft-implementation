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
        self.current_term = 1
        self.state = Follower_state(self)
        self.queue = RedisQueue()
        self.voted_for = None
        self.leader = None
        self.last_log_term = -1 # save last index and term in receive TODO
        self.last_log_index = -1
        self.number_of_nodes = 3
        self.commit_index = 0
        self.last_applied = 0
        # self.client = RaftClient()
        
    def __handler(self, signum, frame):
        print('Signal handler called with signal', signum) # TODO delete Test
        self.__reset_timeout()
        self.state.join()
        self.set_state("Candidate")
        self.state.start()
        
    # TODO Listen to its queue
    def start(self):
        pubsub=self.queue.subscribe('server')
        self.__reset_timeout()
        self.state.start()
        for message in pubsub.listen():
            if message['type'] == 'message':
                message = message['data'].decode('utf-8')
                message = json.loads(message)
                print(message)
                # message=message['data']
                # TODO condition
                if message["kind"] == "Append Entries":
                    self.__reset_timeout()
                    # TODO error
                    print('Append')
                    # answer_receive_append_entries = self.state.receive_append_entries(message)
                    self.queue.publish('consensus',{'response':"Reject","node_id":1})

                elif message["kind"] == "Request Vote":
                    self.queue.publish('consensus',{'response':"Accept","node_id":3})

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
        # timeout = random.randint(7, 14)
        # signal.signal(signal.SIGALRM, self.__handler)
        # signal.alarm(timeout)
        pass
    
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
        # x = client.##
        # self.state.receive_request_vote_answer(x)
        print("send_request_vote")
    
    def send_append_entries(self, message: dict):
        # answer_follower_append_entries = client.
        # self.state.receive_append_entries_answer(answer_follower_append_entries)
        pass
    
    def send_request_vote_answer(self, message: dict):
        print("send_request_vote_answer")
    
    def send_append_entries_answer(self, message: dict):
        print("send_append_entries_answer") 

    def receive_request_vote(self, message: dict):
        # 
        pass
    
    def receive_append_entries(self):
        print("receive_append_entries")
    
    def receive_request_vote_answer(self):
        print("receive_request_vote_answer")
    
    def receive_append_entries_answer(self):
        print("receive_append_entries_answer")
                
                
