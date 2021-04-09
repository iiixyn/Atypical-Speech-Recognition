from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow import keras
import scipy.io as sio
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy import signal


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

model = None

classes = ["down", "eight", "five", "four", "go", "left", "nine", "no", "one", "right", "seven", "six", "three", "two", "up", "yes", "zero"]

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("audio"):
            # read the image in PIL format
            audio = flask.request.files["audio"].read()
            wav = sio.wavfile.read(io.BytesIO(audio))
            specgram = prepare_audio(wav)

            prob=model.predict(specgram.reshape(1, 124, 129, 1))
            index=np.argmax(prob[0])
            predicted =  classes[index]
            data["predicted"] = predicted
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)

def load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    model = keras.models.load_model('best_model_augmented.hdf5')

# Standardize a waveform to be 16000 samples (1 second) long.
def standardize_wave(wave):
    wave = np.array(wave)
    wave_size = np.shape(wave)[0]
    # If longer than 16000 samples, cut it to the first 16000.
    if wave_size > 16000:
        wave = wave[0:16000]
    # If shorter, zero-pad it to 16000 samples.
    elif wave_size < 16000:
        wave = np.pad(wave, (0, 16000 - wave_size), mode='constant')
    return wave

# SFFT function to transform a waveform into a spectrogram.
# From https://www.kaggle.com/alphasis/light-weight-cnn-lb-0-74

def custom_fft(y, fs):
    T = 1.0 / fs
    N = y.shape[0]
    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    # FFT is symmetrical, so we take just the first half
    # FFT is also complex, to we take just the real part (abs)
    vals = 2.0/N * np.abs(yf[0:N//2])
    return xf, vals

def log_specgram(audio, sample_rate, window_size=16,
                 step_size=8, eps=1e-10):
    nperseg = int(round(window_size * sample_rate / 1e3))
    noverlap = int(round(step_size * sample_rate / 1e3))
    freqs, times, spec = signal.spectrogram(audio,
                                    fs=sample_rate,
                                    window='hann',
                                    nperseg=nperseg,
                                    noverlap=noverlap,
                                    detrend=False)
    return freqs, times, np.log(spec.T.astype(np.float32) + eps)

def prepare_audio(wav):
    _, _, specgram = log_specgram(standardize_wave(wav), sample_rate=16000)

if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run()