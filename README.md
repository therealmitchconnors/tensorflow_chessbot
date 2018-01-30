# tensorflow_chessbot
Predict chessboard FEN layouts from images using TensorFlow

This project is loosely based on Sam Ansair's [tensorflow_chessbot](https://github.com/Elucidation/tensorflow_chessbot), which produces FEN Notation (chessboard layout notation) from images of chess diagrams.

The idea here is to take Sam's neural network and make it consumable from a mobile application like lichess.  The purpose is to allow users to take a picture of a chess diagram with their cell phone, and import the game into a chess app for them to play or analyze.  In particular, this should be valuable to students of chess who, like myself, are unable to hold positions in their heads.  Most chess books consist of many diagrams, followed by play notation and analysis, requiring less proficient students to constantly keep a chess board at hand, and to manually set up and reset positions.  

## Obstacles
There are several hurdles to this sort of application of machine learning:
### 1. Mobile platforms have inconsistent (at best) support for tensorflow
While solutions like TensorFlow Mobile exist, there is, at this writing, no plugin for Cordova and other cross-platform development frameworks exists to support them.  A more natural place to implement this logic would be on the server-side, but...

### 2. Most ML projects are implemented in Python, which is not commonly supported in server-side frameworks
In particluar, I am targeting the lichess mobile app, as it is open source and well supported.  The lichess API back-end is implemented in the Play Framework in Scala, so our Neural Network should be accessible from there, either by library or API call.  The most natural solution here would be to use tensorflow serving to call our model from scala using grpc but...

### 3. The tensorflow_chessbot, like many TF examples, is not implemented in pure tensorflow.  In particular, this application leverages PIL, numpy, cv2, and other libraries for data manipulation which would not be accessible over tensorflow serving.  This logic could, theoretically, be ported to Scala, but it is interweaved with TensorFlow operations in such a way that would represent unacceptable redundancy in back and forth communications between Scala and TensorFlow Serving.

## Project Plan

My initial goal is to migrate all of Sam's project into TensorFlow, so that the input of the graph is an arbitrary image file, and the output is FEN Notation requiring little or no manipulation for importing into lichess.  The model should also be easy to manipulate for training purposes, as a substantial amount of training data is available at reddit.com/r/chess, where Sam's model has been in use for over a year.  The steps in this project are roughly as follows

### At Pre-Train Time:
1. Generate a training dataset using our new, limited dependency list (see below)
2. Slice the training dataset into tiles using a tensorflow graph for computer vision (see Runtime step 1)
3. Train the model on our base dataset

### At Run Time: (via tensorflow serving)
1. Slice the chessboard into 64 tiles using same graph as above
2. For each tile, retrieve a classification array representing the probability of each possiblity
3. For each prediction, take the class with the highest score and assemble a FEN-like string.

Along with these steps, effort will be made to make the graph re-usable, i.e. capable of consuming local files as well as remote files, with FEN strings provided arbitrarily

## Dependencies:
In order to maximise the usability of this model, we will use TensorFlow 1.2 with Python 3.6, which (as far as I can tell) is available on all platforms.

## Stretch Goals
Currently, the model only consumes diagrams whose chessboards are perfectly parallel to the image edges, which is usually the case with images taken from chess programs, and is never the case from images coming from cameras.  More work will need to be done to find a chess diagram within an image and rectify the diagram, in case the image is captured at an angle.  A good deal of work has been done in this area for physical chessboards at [neural-chessboard](https://github.com/maciejczyzewski/neural-chessboard) and may be re-usable here.  In addition, it would be cool to be capable of recognizing physical board layouts as well...
