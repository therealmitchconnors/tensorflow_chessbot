
import grpc
import ChessFenService_pb2_grpc
import ChessFenService_pb2
import helper_functions
import numpy as np
import time

import argparse

parser = argparse.ArgumentParser(description='Predict a chessboard FEN from supplied local image link or URL')
parser.add_argument('--url', help='URL of image (ex. http://imgur.com/u4zF5Hj.png)')
parser.add_argument('--filepath', help='filepath to image (ex. u4zF5Hj.png)')
parser.add_argument('--server_address', help='path to server (defaluts to "localhost:8500"')

class ChessFenClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = ChessFenService_pb2_grpc.ChessFenServiceStub(channel)

    def getPrediction(self,img):
        img_arr = np.asarray(img.convert("L"), dtype=np.uint8)
        param = ChessFenService_pb2.FenRequest()
        param.Image = str(bytearray(img_arr))
        param.ImageWidth, param.ImageHeight = img_arr.shape
        print(time.time())
        resp = self.stub.PredictFen(param)
        print(time.time())
        print('done')
        return resp.FenString, resp.Score
    
    
    def makePrediction(self,image_url):
        """Return FEN prediction, and certainty for a URL"""
        # Try to load image url
        img = helper_functions.loadImageURL(image_url)

        if img == None:
            print("Couldn't load image url: %s" % image_url)
            return None, 0.0

        # Make prediction
        fen, certainty = self.getPrediction(img)
        if fen:
            return fen, certainty
        else:
            return None, 0.0

    def makePredictionFromFile(self,image_path):
        """Return FEN prediction, and certainty for a image file"""
        # Try to load image url
        img = helper_functions.loadImageFromPath(image_path)

        if img == None:
            print("Couldn't load image path: %s" % image_path)
            return None, 0.0

        # Make prediction
        fen, certainty = self.getPrediction(img)
        if fen:
            return fen, certainty
        else:
            return None, 0.0

###########################################################
# MAIN

if __name__ == '__main__':
    args = parser.parse_args()

    # Initialize predictor, takes a while, but only needed once
    predictor = ChessFenClient(args.server_address)

    if args.filepath:
        fen, certainty = predictor.makePredictionFromFile(args.filepath)
        print("Predicted FEN: %s" % fen)
        print("Certainty: %.1f%%" % (certainty*100))
    else:
        if args.url:
            url = args.url
        else:
            url = 'http://imgur.com/u4zF5Hj.png'

        fen, certainty = predictor.makePrediction(url)
        print("Predicted FEN: %s" % fen)
        print("Certainty: %.1f%%" % (certainty*100))

    print("Done")