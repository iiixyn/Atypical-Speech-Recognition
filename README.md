# Atypical-Speech-Recognition

This repository contains the different parts of Xinyi's Atypical Speech Recognition project for the MAIS 202 AI Bootcamp. It is comprised of 3 main elements:
1. A Jupyter notebook named `asr.ipynb` at the project's root;
2. A Vue.js front-end client in the `client` folder;
3. A Flask (Python) back-end server in the `server` folder.

## Jupyter Notebook
The Jupyter notebook is the main project that has been developed over the course of the MAIS 202 AI Bootcamp. It contains all the necessary functions to preprocess the TORGO database and train a convolutional neural network on it to predict simple commands such as yes/no/up/down...

In order to preprocess the TORGO database, the decompressed files must be placed in the folder that is walked through in cell 3 of the notebook:
```python
for directory, subdirectories, files in os.walk("../../../Data/"):
```

The path can be changed to suit the actual location of the data you want to preprocess.

The notebook also contains useful individual functions that apply transformations to WAV files, such as cleaning them up using a reference timestamp file, and transforming them into spectrograms so that a 2D CNN can use it as input.

The final cells of the notebook constitute the actual model. It is also saved in the repository, and can be reloaded through Keras using the following line:
```python
model = keras.models.load_model('best_model_augmented.hdf5')
```

Some optional cells at the end of the notebook can also be run to augment the input audio data if its size is insufficient (like in my case).

## Vue.js Front-End
The Vue.js front-end is a demo website that explains the project in detail. It contains information about the motivation for this project as well as the implementation of the model.

To run the website, use the following commands from the root directory of the project:
```bash
cd client
npm run serve
```

It will then be running on `http://localhost:8080/`.

A demo will eventually be added in the "Demo" section to communicate with the back-end by sending it some audio data, and receiving a prediction made by the ASR model.

## Flask Back-End
The Flask back-end hosts the ASR model for use through a very simple REST API. It exposes one route: `/predict`, which accepts POST requests submitting an audio blob in the `"audio"` field of the request data. If the POST request is done correctly, the server will run the ASR model on the data (after having it preprocessed first) and will return a response containing the predicted label (in the `"predict"` field of the data) and a success flag (in the `"success"` field of the data).

To run the Flask back-end, simply run `serve.py` using a Python environment. In order to run, certain modules need to be installed:
```bash
pip install numpy scipy tensorflow scikit-learn flask flask-cors
```

The back-end will then run on `http://localhost:5000/`. To use the model, send a POST request to the `/predict` endpoint with the correct data inside (see above).