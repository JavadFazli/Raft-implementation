# compiler.sh - A shell script to compile gRPC code from .proto files
# Ensure that 'protoc' and 'grpcio-tools' are installed
# You can install them with: pip install grpcio-tools

# Set the path to the .proto files and the output directory
#PROTO_PATH="./rpc"  # Path to the directory containing .proto files
#OUTPUT_PATH="./rpc"  # Path to the output directory for generated code

#PROTO_PATH="./"  # Path to the directory containing .proto files
#OUTPUT_PATH="./"  # Path to the output directory for generated code
## Compile the .proto file to generate Python code for gRPC and Protocol Buffers
#protoc --proto_path="$PROTO_PATH" \
#       --python_out="$OUTPUT_PATH" \
#       --grpc_python_out="$OUTPUT_PATH" \
#       "$PROTO_PATH/raft.proto"

#python -m grpc_tools.protoc -I./rpc --python_out=./rpc --grpc_python_out=./rpc ./rpc/raft.proto
#!/bin/bash

# Define variables for paths
PROTO_DIR=./
PROTO_FILE=$PROTO_DIR/raft.proto
OUT_DIR=./

# Check if the proto file exists
if [ ! -f $PROTO_FILE ]; then
    echo "Error: Protocol Buffer file not found: $PROTO_FILE"
    exit 1
fi

# Compile Protocol Buffer file
python -m grpc_tools.protoc -I=$PROTO_DIR --python_out=$OUT_DIR --grpc_python_out=$OUT_DIR $PROTO_FILE

# Check if the compilation was successful
if [ $? -eq 0 ]; then
    echo "Proto compilation successful."
else
    echo "Error: Proto compilation failed."
fi
