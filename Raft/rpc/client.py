import grpc
from Raft.rpc import raft_pb2, raft_pb2_grpc  # Import generated gRPC files
from Raft.app.config import Config  # Import configuration settings
from google.protobuf.json_format import MessageToDict


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
        id=message["id"]
        Last_Log_Term=message["Last_Log_Term"]
        Last_Log_Id=message["Last_Log_Id"]
        request = raft_pb2.VoteRequest(id = id, term = term, Last_Log_Term = Last_Log_Term, Last_Log_Id = Last_Log_Id
)
        # node_id = node_id, term = term, Last_Log_Term = Last_Log_Term, Last_Log_Id = Last_Log_Id
        # request.node_id = node_id

        # Call the RequestVote RPC and return the response

        response = self.create_stub(id).RequestVote(request)
        response_dict = MessageToDict(request, preserving_proto_field_name=True)

        return response_dict


    def append_entries(self, message):
        term = message["term"]
        id = message["id"]
        destination_id = message["Destination_Id"]
        prev_log_term = message["Prev_Log_Term"]
        prev_log_id = message["Prev_Log_Id"]
        entries = message["Entries"]
        leader_commit = message["Leader_Commite"]

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
        response_dict = MessageToDict(request, preserving_proto_field_name=True)

        return response_dict

# Example usage:
if __name__ == "__main__":
    client = RaftClient()

    # # Example RequestVote RPC
    message={"term":2,"id":1,"Last_Log_Term":1,"Last_Log_Id":1}
    vote_granted = client.request_vote(message)
    print("Vote Granted:", vote_granted)

    # Example AppendEntries RPC
    message2={"term":2, "id":1, "Destination_Id":1 ,"Prev_Log_Term":2 ,"Prev_Log_Id":2 ,"Entries":"22" ,"Leader_Commite":5}
    success = client.append_entries(message2)
    print("Append Entries Success:", success)
