<template>
  <div id="app">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <h3 class="md-title" style="flex: 1">
          Xinyi's Speech Recognition Project
        </h3>
        <md-tabs class="md-primary" md-alignment="right">
          <md-tab
            id="tab-intro"
            md-label="Introduction"
            href="#intro_card"
          ></md-tab>
          <md-tab
            id="tab-speech"
            md-label="Motivation"
            href="#motivation_card"
          ></md-tab>
          <md-tab id="tab-model" md-label="Model" href="#model_card"></md-tab>
          <md-tab id="tab-demo" md-label="Demo" href="#demo_card"></md-tab>
        </md-tabs>
      </md-app-toolbar>
      <md-app-content>
        <md-card id="intro_card">
          <md-card-header>
            <div class="md-title">Introduction</div>
          </md-card-header>
          <md-card-content>
            <p>
              This webpage is created for Xinyi's MAIS 202 term project --
              Atypical Speech Recognition.<br />
              You will read about some big-picture infomation on how this
              project came to existence, some technical detail about the model,
              and get to try out a demo of this tool at the end.
            </p>
          </md-card-content>
        </md-card>
        <md-card id="motivation_card">
          <md-card-header>
            <div class="md-title">Motivation</div>
          </md-card-header>

          <md-card-content>
            <p>
              Automatic speech recognition has brought our lives with great
              convenience: it helps us write faster, take notes, and with
              smart-home devices, it can even manage out daily life. However,
              while we who have a "typical" speech have been enjoying this
              advance in technology, those who have atypical speech are being
              left out due to the fact that the data that have been used to
              train the models are mostly typical speech. This is why I would
              like to develop a speech recognition tool for people with atypical
              speech, and especifically, people with dysarthria.
            </p>
            <p>
              Dysarthria is a motor-speech disorder caused by muscle weakness.
              It usually results from a brain injury or neurological condition.
              People with dysarthria have difficulty controlling the muscles
              that they need to make normal speech, and that leads to them being
              difficult to understand. It is also not trivial to cure, if even
              possible to fully recover at all.
            </p>
            <p>
              In the following audio clip, a patient with dysarthria pronounces
              "Giving those who observe him a pronounced feeling of the utmost
              respect.":
            </p>

            <audio controls>
              <source src="./assets/sample_d1.mp3" type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>

            <p>
              The sentence above is fairly complex, even for a "typical" speech
              recognition tool. So, I decided to focus the development of my
              tool (and the machine learning model it would be based on) on the
              recognition of simple commands, such as directions ("up", "down",
              "left", "right"), digits (0 to 9) and some others ("yes", "no",
              "go").
            </p>
          </md-card-content>
        </md-card>
        <md-card id="model_card">
          <md-card-header>
            <div class="md-title">Model</div>
          </md-card-header>

          <md-card-content>
            <div class="md-subhead">Dataset</div>
            <p>
              In order to attempt to solve the issue described in the motivation
              section, I tried to find a database of speech from dysarthria
              patients. I found the
              <a
                href="http://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html"
                >TORGO database</a
              >, a database developed by University of Toronto. Without going
              into too much detail, this dataset contains audio samples from
              different speakers with and without dysarthria. The samples are
              accompanied by files that give the associated prompts (for
              example, "yes"), as well as phonemic transcriptions of the
              samples. There is also data on articulatory positions, but it was
              not used for this project due to its complexity.
            </p>
            <div class="md-subhead">Preprocessing</div>
            <div>
              <p>
                To be able to use the data from the dataset in a Machine
                Learning model, it has to be preprocessed and transformed into
                an input-to-label format. To achieve this, the following steps
                were done:
              </p>
              <ol>
                <li>
                  The audio files were filtered for words of interest (commands
                  described above), based on the prompt files.
                </li>
                <li>
                  The relevant audio was extracted from the files using the
                  phonemic transcription (containing timestamps).
                </li>
                <li>
                  The audio was associated to its labels (prompts) and
                  cleaned/standardized (duration of 1 second, filter noise...).
                </li>
                <li>
                  The audio was transformed into spectrograms (see below), so
                  that it becomes an "image".
                </li>
                <li>
                  The audio was also augmented using data augmentation
                  techniques (pitch/speed change, white noise added) to increase
                  the size of the training set.
                </li>
              </ol>
              <p>
                Here is an example of a spectrogram coming from preprocessing :
              </p>
              <md-card-media>
                <img
                  src="./assets/spectrogram.png"
                  alt="Spectrogram"
                  style="max-width: 400px; margin-bottom: 2em"
                />
              </md-card-media>
            </div>
            <div class="md-subhead">Machine Learning Model</div>
            <div>
              <p>
                Once the input had been preprocessed, a convolutional neural
                network (CNN) was trained using that as its dataset. The goal of
                using a CNN was for the network to recognize the visual
                "features" on the spectrograms, that are in fact the phonemes
                making up the different words. The spectrograms are also a
                better visual representation of the words compared to a
                one-dimensional audio wave (amplitude) signal; spectrograms
                actually give information that can help linguists identify
                phonemes (and eventually words) by just looking at them. This is
                what I wanted to emulate with my CNN model.
              </p>
              <p>
                The network is based on a "typical" CNN architecture, comprising
                2-dimensional "convolution" layers, "pooling" layers, "dropout"
                layers (to avoid overfitting), as well as a final stage
                comprised of "dense" layers that are actually responsible for
                categorizing the learned features and making a prediction on the
                output label. It achieves approximately 77% accuracy on a
                randomly-split validation set.
              </p>
              <p>
                Below is the confusion matrix for the predictions of the model
                on the validation set:
              </p>
              <md-card-media>
                <img
                  src="./assets/confusion.png"
                  alt="Confusion Matrix"
                  style="max-width: 400px; margin-bottom: 2em"
                />
              </md-card-media>
            </div>
          </md-card-content>
        </md-card>
        <md-card id="demo_card">
          <md-card-header>
            <div class="md-title">Demo</div>
          </md-card-header>

          <md-card-content>
            Couldn't finish this, sorry.
          </md-card-content>
        </md-card>
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import Vue from "vue";
import VueMaterial from "vue-material";
import "vue-material/dist/vue-material.min.css";
import "vue-material/dist/theme/default-dark.css";

Vue.use(VueMaterial);

export default {
  name: "App",
  components: {
    //HelloWorld
  },
  methods: {
  },
};
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.md-app {
  max-height: 100vh;
}

.md-card {
  width: 90vw;
  margin: 4px;
  margin-left: auto;
  margin-right: auto;
  display: inline-block;
  vertical-align: top;
}

audio:not(.md-image) {
  height: 54px;
}
</style>
