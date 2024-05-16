import grpc
import raft_pb2, raft_pb2_grpc  # Import generated gRPC files
from Raft.app.config import Config  # Import configuration settings


class RaftClient:
    def __init__(self):
        # Create a gRPC channel to communicate with the server
        self.channel = grpc.insecure_channel(f'{Config.RAFT_NODE_HOST}:{Config.RAFT_NODE_PORT}')

        # Create a stub for the Raft service
        self.stub = raft_pb2_grpc.RaftServiceStub(self.channel)

    def create_stub(self,node_id):
        channel = grpc.insecure_channel(f'{Config.NODE_HOSTS[node_id]}:{Config.NODE_PORTS[node_id]}')
        stub = raft_pb2_grpc.RaftServiceStub(channel)
        return stub
    def request_vote(self, message):
        # Create a request for the RequestVote RPC
        term=message["term"]
        node_id=message["id"]
        Last_Log_Term=message["Last Log Term"]
        Last_Log_Id=message["Last Log Id"]
        request = raft_pb2.VoteRequest(node_id = node_id, term = term, Last_Log_Term = Last_Log_Term, Last_Log_Id = Last_Log_Id
)
        # node_id = node_id, term = term, Last_Log_Term = Last_Log_Term, Last_Log_Id = Last_Log_Id
        # request.node_id = node_id

        # Call the RequestVote RPC and return the response

        response = self.create_stub(node_id).RequestVote(request)
        return response.vote_granted

    def append_entries(self, message):
        term = message["term"]
        id = message["id"]
        destination_id = message["Destination Id"]
        prev_log_term = message["Prev Log Term"]
        prev_log_id = message["Prev Log Id"]
        entries = message["Entries"]
        leader_commit = message["Leader Commite"]

        request = raft_pb2.LogEntry(
            term=term,
            id=id,
            Destination_Id=destination_id,
            Prev_Log_Term=prev_log_term,
            Prev_Log_Id=prev_log_id,
            Entries=entries,
            Leader_Commite=leader_commit
        )
        # Call the AppendEntries RPC and return the response

        response = self.create_stub(destination_id).AppendEntries(request)
        return response.success


# Example usage:
if __name__ == "__main__":
    client = RaftClient()

    # Example RequestVote RPC
    message={"term":2,"id":3,"Last Log Term":4,"Last Log Id":5}
    vote_granted = client.request_vote(message)
    print("Vote Granted:", vote_granted)

    # Example AppendEntries RPC
    message2={"term":2, "id":1, "Destination Id":1 ,"Prev Log Term":2 ,"Prev Log Id":2 ,"Entries":"22" ,"Leader Commite":5}
    success = client.append_entries(message2)
    print("Append Entries Success:", success)
