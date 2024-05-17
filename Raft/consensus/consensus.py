import signal
import random
from Raft.app.config import (Config)
from Raft.consensus.log import Log
from Raft.broker.queue import RedisQueue
from Raft.consensus.state.follower_state import Follower_state
from Raft.consensus.state.candidate_state import Condidate_state
from Raft.consensus.state.leader_state import Leader_state
from Raft.rpc.client import RaftClient
import json 
import threading


class Consensus:
    
    def __init__(self, id):
        self.id = id
        self.log = Log()
        self.current_term = 1
        self.state = Follower_state(self)
        self.queue = RedisQueue()
        self.voted_for = None
        self.leader = None
        self.last_log_term = -1
        self.last_log_index = -1
        self.number_of_nodes = Config.NODES_NUMBER
        self.commit_index = 0
        self.last_applied = 0
        # self.client = RaftClient()
        
    def __handler(self, signum, frame):
        print('Timeout') # TODO delete Test
        self.__reset_timeout()
        self.set_state("Candidate")
        

    def start(self):
        
        pubsub=self.queue.subscribe('server')
        self.__reset_timeout()
        self.state.start()
        for message in pubsub.listen():
            if message['type'] == 'message':
                message = message['data'].decode('utf-8')
                message = json.loads(message)
                # print(message)
                # TODO condition

                if message["kind"] == "AppendEntries":

                    # message2 = {}
                    # message2["Answer"] = 'Accept'
                    # message2["term"] = self.current_term
                    # message2["Destination_Id"] = message['id']
                    # message2["id"] = self.id
                    # self.queue.publish('consensus', message2)

                    self.__reset_timeout()
                    # TODO error
                    threading.Thread(target=self.receive_append_entries, args=(message,)).start()
                    
                elif message["kind"] == "RequestVote":
                    self.__reset_timeout()
                    threading.Thread(target=self.receive_request_vote, args=(message,)).start()

                    # message2 = {}
                    # message2["Answer"] = 'Accept'
                    # message2["term"] = self.current_term
                    # message2["Destination_Id"] = message['id']
                    # message2["id"] = self.id
                    # self.queue.publish('consensus', message2)

                elif message["kind"] == "Client":
                    threading.Thread(target=self.state.receive_client_message, args=(message,)).start()
                    
                # TODO delete all answers
                elif message["kind"] == "RequestVoteAnswer":
                    threading.Thread(target=self.receive_request_vote_answer, args=(message,)).start()
                    
                elif message["kind"] == "AppendEntriesAnswer":
                    threading.Thread(target=self.receive_append_entries_answer, args=(message,)).start()

                else:
                    # TODO rise exception
                    pass
                
         
    def __reset_timeout(self):
        timeout = random.randint(Config.START_TIMEOUT, Config.STOP_TIMEOUT)
        signal.signal(signal.SIGALRM, self.__handler)
        signal.alarm(timeout)
        pass
    
    def set_state(self, kind):
        
        del self.state
        # TODO uncomment it
        # self.state.join()
        
        if kind == "Candidate":
            self.state = Condidate_state(self)
        elif kind == "Leader":
            signal.alarm(0)
            self.state = Leader_state(self)
        elif kind == "Follower":
            signal.alarm(7)
            self.state = Follower_state(self)
        else:
            raise Exception("Not Valid type state !!!")
        
        self.state.start()
        
    
    def send_request_vote(self, message: dict):
        print("send_request_vote")
        print(message)
        print()
        # answer = self.client.request_vote(message)
        # self.receive_request_vote_answer(answer)
        
        
    
    def send_append_entries(self, message: dict):
        print("send_append_entries")
        print(message)
        print()
        # answer = self.client.append_entries(message)
        # self.receive_append_entries_answer(answer)

    
    def send_request_vote_answer(self, message: dict):
        print("send_request_vote_answer")
        print(message)
        print()
        # self.queue.publish('consensus',message)
        
    
    def send_append_entries_answer(self, message: dict):
        print("send_append_entries_answer") 
        print(message)
        print()
        # self.queue.publish('consensus',message)


    def receive_request_vote(self, message: dict):
        print("receive_request_vote")
        print(message)
        print()
        self.state.receive_request_vote(message)

    
    def receive_append_entries(self, message: dict):
        print("receive_append_entries")
        print(message)
        print()
        self.state.receive_append_entries(message)

    
    def receive_request_vote_answer(self, message: dict):
        print("receive_request_vote_answer")
        print(message)
        print()
        self.state.receive_request_vote_answer(message)

    
    def receive_append_entries_answer(self, message: dict):
        print("receive_append_entries_answer")
        print()
        self.state.receive_append_entries_answer(message)

                
                
