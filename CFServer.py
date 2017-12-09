import tensorflow_chessbot
import ChessFenService_pb2_grpc
import ChessFenService_pb2
import numpy as np
import time
import concurrent.futures as futures
import grpc

import argparse

parser = argparse.ArgumentParser(description='Run a FEN prediction service with grpc')
parser.add_argument('--insecure_port', help='port on which to listen (default is [::]:8500)')

class ChessFenServicer(ChessFenService_pb2_grpc.ChessFenServiceServicer):
    def __init__(self):
        self.cb = tensorflow_chessbot.ChessboardPredictor()

    def PredictFen(self, request, context):
        print(time.time())
        image2d = np.array(bytearray(request.Image), dtype=np.float32).reshape([request.ImageWidth, request.ImageHeight])
        [fen, certainty] = self.cb.getPredictionFromArray(image2d)
        print(time.time())
        return ChessFenService_pb2.FenResponse(FenString=fen, Score=certainty)

def start(insecure_port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    ChessFenService_pb2_grpc.add_ChessFenServiceServicer_to_server(ChessFenServicer(), server)
    server.add_insecure_port(insecure_port)
    server.start()
    return server

if __name__ == '__main__':
    args = parser.parse_args()

    server = None
    if (args.insecure_port):
        server = start(insecure_port)
    else: 
        server = start("[::]:8500")

    try:
        while(True):
            time.sleep(60)    
    except:
        server.stop(2) # 2 seconds grace time on stop
        raise