import signal
import random
import threading

from Raft.app.config import Config
from Raft.consensus.log import Log
from Raft.broker.queue import RedisQueue
from Raft.consensus.state.follower_state import Follower_state
from Raft.consensus.state.candidate_state import Condidate_state
from Raft.consensus.state.leader_state import Leader_state
# from Raft.rpc.client import RaftClient
import json

from Raft.rpc.client import RaftClient


class Consensus:
    
    def __init__(self, id):
        self.id = id
        self.log = Log()
        self.current_term = 1
        self.state = Follower_state(self)
        self.state_kind = "Follower"
        self.queue = RedisQueue(host='0.0.0.0', port=6379)
        self.voted_for = None
        self.leader = None
        self.last_log_term = -1 # save last index and term in receive TODO
        self.last_log_index = -1
        self.number_of_nodes = 3
        self.commit_index = 0
        self.last_applied = 0
        self.timer=None
        self.client = RaftClient()
        
    def __handler(self, signum=0, frame=0):
        print('Timeout', signum) # TODO delete Test
        self.__reset_timeout()
        if self.state_kind == "Candidate":
            self.current_term += 1
        self.set_state("Candidate")
        
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
                # TODO condition

                if message["kind"] == "AppendEntries":

                    message2 = {}
                    message2["Answer"] = 'Accept'
                    message2["term"] = self.current_term
                    message2["Destination_Id"] = message['id']
                    message2["id"] = self.id
                    self.queue.publish('consensus', message2)

                    self.__reset_timeout()
                    # TODO error
                    self.receive_append_entries(message)
                    
                elif message["kind"] == "RequestVote":
                    self.__reset_timeout()
                    self.receive_request_vote(message)

                    message2 = {}
                    message2["Answer"] = 'Accept'
                    message2["term"] = self.current_term
                    message2["Destination_Id"] = message['id']
                    message2["id"] = self.id
                    self.queue.publish('consensus', message2)

                elif message["kind"] == "Client":
                    self.state.receive_client_message(message)

                else:
                    # TODO rise exception
                    pass
                
         
    def __reset_timeout(self):
        if self.timer:
            self.timer.cancel()
        timeout = random.randint(Config.START_TIMEOUT, Config.STOP_TIMEOUT)
        self.timer = threading.Timer(timeout, self.__handler)
        self.timer.start()
        # signal.signal(signal.SIGALRM, self.__handler)
        # signal.alarm(timeout)
        pass
    
    def set_state(self, kind):
        
        del self.state
        # TODO uncomment it
        # self.state.join()
        
        if kind == "Candidate":
            self.state_kind = "Candidate"
            self.state = Condidate_state(self)
        elif kind == "Leader":
            self.timer.stop()
            self.state_kind = "Leader"
            self.state = Leader_state(self)
        elif kind == "Follower":
            self.state_kind = "Follower"
            self.state = Follower_state(self)
        else:
            # TODO rise exception
            pass
        self.state.start()
        
    
    def send_request_vote(self, message: dict):
        # answer = self.client.request_vote(message)
        # self.receive_request_vote_answer(answer)
        print("send_request_vote")
    
    def send_append_entries(self, message: dict):
        answer = self.client.append_entries(message)
        self.receive_append_entries_answer(answer)
        print("send_append_entries")
    
    def send_request_vote_answer(self, message: dict):
        self.queue.publish('consensus',message)
        print(message)
        print("send_request_vote_answer")
        
    
    def send_append_entries_answer(self, message: dict):
        self.queue.publish('consensus',message)
        print("send_append_entries_answer") 

    def receive_request_vote(self, message: dict):
        self.state.receive_request_vote(message)
        print("receive_request_vote")
    
    def receive_append_entries(self, message: dict):
        self.state.receive_append_entries(message)
        print("receive_append_entries")
    
    def receive_request_vote_answer(self, message: dict):
        self.state.receive_request_vote_answer(message)
        print()
        print("receive_request_vote_answer")
    
    def receive_append_entries_answer(self, message: dict):
        print()
        self.state.receive_append_entries_answer(message)
        print("receive_append_entries_answer")
                
                
