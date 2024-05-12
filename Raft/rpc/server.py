import grpc
from concurrent import futures
import raft_pb2, raft_pb2_grpc  # Import generated gRPC files
from Raft.consensus.log import Log  # Import Log class from your project


class RaftServicer(raft_pb2_grpc.RaftServiceServicer):
    def __init__(self):
        self.log = Log()  # Initialize the Log instance

    def RequestVote(self, request, context):
        """
        gRPC method to handle RequestVote RPC.
        Implement the logic to handle vote requests here.
        """
        # Implement your logic here (e.g., send vote response based on node's state)
        # For demonstration purposes, we'll simply return a granted vote
        return raft_pb2.VoteResponse(vote_granted=True)

    def AppendEntries(self, request, context):
        """
        gRPC method to handle AppendEntries RPC.
        Implement the logic to handle appending log entries here.
        """
        # Implement your logic here (e.g., append log entries to the log)
        # For demonstration purposes, we'll simply return a success response
        return raft_pb2.AppendResponse(success=True)


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add the RaftServicer to the server
    raft_pb2_grpc.add_RaftServiceServicer_to_server(RaftServicer(), server)

    # Listen on the specified port
    server.add_insecure_port('[::]:' + str(Config.GRPC_PORT))

    # Start the server
    server.start()
    print(f"Server started on port {Config.GRPC_PORT}")

    # Keep the server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the server on KeyboardInterrupt
        server.stop(0)


if __name__ == '__main__':
    serve()
