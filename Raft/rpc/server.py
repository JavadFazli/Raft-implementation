import json

import grpc
from concurrent import futures
from Raft.rpc import raft_pb2, raft_pb2_grpc  # Import generated gRPC files
from Raft.consensus.log import Log  # Import Log class from your project
from Raft.app.config import (Config)
from Raft.broker.queue import RedisQueue
from google.protobuf.json_format import MessageToDict


class RaftServicer(raft_pb2_grpc.RaftServiceServicer):
    def __init__(self):
        self.log = Log()  # Initialize the Log instance
        self.queue=RedisQueue()
    def RequestVote(self, request, context):
        """
        gRPC method to handle RequestVote RPC.
        Implement the logic to handle vote requests here.
        """
        request_dict = MessageToDict(request, preserving_proto_field_name=True)
        request_dict["kind"] = "RequestVote"
        pubsub = self.queue.subscribe('consensus')

        self.queue.publish('server', request_dict)

        for message in pubsub.listen():
            # print(message)
            if message['type'] == 'message':
                message = message['data'].decode('utf-8')
                message = json.loads(message)
                # print(message['node_id'], request_dict['node_id'])
                if message['Destination_Id'] == request_dict['id']:
                    if message['Answer'] == 'Accept':
                        return raft_pb2.VoteResponse(Answer='Accept',term=message['term'],id=message['id'])
                    else:
                        return raft_pb2.VoteResponse(Answer='Reject',term=message['term'],id=message['id'])
                    break


    def AppendEntries(self, request, context):
        """
        gRPC method to handle AppendEntries RPC.
        Implement the logic to handle appending log entries here.
        """
        request_dict = MessageToDict(request, preserving_proto_field_name=True)
        request_dict["kind"] = "AppendEntries"
        pubsub = self.queue.subscribe('consensus')
        print(request_dict)
        self.queue.publish('server',request_dict)

        for message in pubsub.listen():
            print(message)
            if message['type'] == 'message':
                message = message['data'].decode('utf-8')
                message = json.loads(message)
                print(message['id'],request_dict['Destination_Id'])
                if message['id']==request_dict['Destination_Id']:
                    if message['Answer']=='Accept':
                        return raft_pb2.AppendResponse(success=True,term=message['term'],id=message['id'])
                    else:
                        return raft_pb2.AppendResponse(success=False,term=message['term'],id=message['id'])
                    break

        # Implement your logic here (e.g., append log entries to the log)


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
