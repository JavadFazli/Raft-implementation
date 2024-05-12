import grpc
import raft_pb2, raft_pb2_grpc  # Import generated gRPC files
from app.config import Config  # Import configuration settings


class RaftClient:
    def __init__(self):
        # Create a gRPC channel to communicate with the server
        self.channel = grpc.insecure_channel(f'{Config.RAFT_NODE_HOST}:{Config.RAFT_NODE_PORT}')

        # Create a stub for the Raft service
        self.stub = raft_pb2_grpc.RaftServiceStub(self.channel)

    def request_vote(self, node_id, term):
        # Create a request for the RequestVote RPC
        request = raft_pb2.VoteRequest(node_id=node_id, term=term)

        # Call the RequestVote RPC and return the response
        response = self.stub.RequestVote(request)
        return response.vote_granted

    def append_entries(self, term, command):
        # Create a request for the AppendEntries RPC
        request = raft_pb2.LogEntry(term=term, command=command)

        # Call the AppendEntries RPC and return the response
        response = self.stub.AppendEntries(request)
        return response.success


# Example usage:
if __name__ == "__main__":
    client = RaftClient()

    # Example RequestVote RPC
    vote_granted = client.request_vote(node_id="node_2", term=10)
    print("Vote Granted:", vote_granted)

    # Example AppendEntries RPC
    success = client.append_entries(term=10, command="Add new entry to log")
    print("Append Entries Success:", success)
