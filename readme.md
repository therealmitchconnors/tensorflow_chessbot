
**Chess FEN Prediction Service**: 
The service branch demonstrates how to run a grpc server
providing FEN predictions, as well as how to call the service.

The server's pre-requisites are the same as the master branch (see readme there), plus grpcio-tools and tensorflow-serving-api.

To install client prerequisites, run: 

    pip install beautifulsoup4
    pip install --no-cache-dir grpcio-tools
    pip install numpy

To generate the python-grpc classes for this service, run:

    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./ChessFenService.proto

To start the server, run `python CFServer.py`

To run the client, run: 

    python ChessFenClient.py --server_address=localhost:8500 --url='https://i.redd.it/nn19vktdi4101.png'

