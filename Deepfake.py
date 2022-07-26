"""demo_toolbox_collab.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1uzo648FMIp--VTJipTEMDOZF-k8O7J16
Make sure GPU is enabled
Runtime -> Change Runtime Type -> Hardware Accelerator -> GPU
"""
!pip install inference-tools
# Clone git repo
!git clone https://github.com/CorentinJ/Real-Time-Voice-Cloning.gitcd Real-Time-Voice-Cloning/

# Install dependencies
!pip install -q -r requirements.txt
!apt-get install -qq libportaudio2

# Download dataset
!gdown https://drive.google.com/uc?id=1n1sPXvT34yXFLT47QZA6FIRGrwMeSsZc
!unzip pretrained.zip

# Code for recording audio from the browser
from IPython.display import Javascript
from google.colab import output
from base64 import b64decode
import IPython
import uuid
from google.colab import output


class InvokeButton(object):
  def __init__(self, title, callback):
    self._title = title
    self._callback = callback

  def _repr_html_(self):
    from google.colab import output
    callback_id = 'button-' + str(uuid.uuid4())
    output.register_callback(callback_id, self._callback)

    template = """<button id="{callback_id}" style="cursor:pointer;background-color:#EEEEEE;border-color:#E0E0E0;padding:5px 15px;font-size:14px">{title}</button>
        <script>
          document.querySelector("#{callback_id}").onclick = (e) => {{
            google.colab.kernel.invokeFunction('{callback_id}', [], {{}})
            e.preventDefault();
          }};
        </script>"""
    html = template.format(title=self._title, callback_id=callback_id)
    return html

RECORD = """
const sleep  = time => new Promise(resolve => setTimeout(resolve, time))
const b2text = blob => new Promise(resolve => {
  const reader = new FileReader()
  reader.onloadend = e => resolve(e.srcElement.result)
  reader.readAsDataURL(blob)
})
var record = time => new Promise(async resolve => {
  stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  recorder = new MediaRecorder(stream)
  chunks = []
  recorder.ondataavailable = e => chunks.push(e.data)
  recorder.start()
  await sleep(time)
  recorder.onstop = async ()=>{
    blob = new Blob(chunks)
    text = await b2text(blob)
    resolve(text)
  }
  recorder.stop()
})
"""

def record(sec=3):
  display(Javascript(RECORD))
  s = output.eval_js('record(%d)' % (sec*1000))
  b = b64decode(s.split(',')[1])
  with open('audio.wav','wb+') as f:
    f.write(b)
  return 'audio.wav'

# !pip install -q matplotlib-venn
# !apt-get -qq install -y libfluidsynth1

# # # To determine which version you're using:
# # !pip show tensorflow
# # # For the current version: 
# # !pip install --upgrade tensorflow
# # # For a specific version:
# # !pip install tensorflow==1.2

# # https://pypi.python.org/pypi/libarchive
# !apt-get -qq install -y libarchive-dev && pip install -q -U libarchive
# import libarchive

# # https://pypi.python.org/pypi/pydot
# !apt-get -qq install -y graphviz && pip install -q pydot
# import pydot

# !apt-get -qq install python-cartopy python3-cartopy
# import cartopy

# To determine which version you're using:
!pip show tensorflow
# # For the current version: 
!pip install --upgrade tensorflow
!pip install inference-tools
# For a specific version:
# !pip install tensorflow==1.2
# !pip install tensorflow==1.15.0
#!pip install tensorflow==1.14.0

!pip install unidecode 
!pip install webrtcvad
from IPython.display import Audio
from IPython.utils import io
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa
encoder_weights = Path("encoder/saved_models/pretrained.pt")
vocoder_weights = Path("vocoder/saved_models/pretrained/pretrained.pt")
syn_dir = Path("synthesizer/saved_models/logs-pretrained/taco_pretrained")
encoder.load_model(encoder_weights)
synthesizer = Synthesizer(syn_dir)
vocoder.load_model(vocoder_weights)

#@title Deep vocoder
def synth():
  text = "love you sama " #@param {type:"string"}
  print("Now recording for 10 seconds, say what you will...")
  
  ### record
  record(30)
  print("Audio recording complete")
  in_fpath = Path("audio.wav")
  reprocessed_wav = encoder.preprocess_wav(in_fpath)
  original_wav, sampling_rate = librosa.load(in_fpath)
  preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
  embed = encoder.embed_utterance(preprocessed_wav)
  print("Synthesizing new audio...")
  with io.capture_output() as captured:
    specs = synthesizer.synthesize_spectrograms([text], [embed])
  generated_wav = vocoder.infer_waveform(specs[0])
  generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
  display(Audio(generated_wav, rate=synthesizer.sample_rate))
InvokeButton('Start recording', synth)

https://github.com/Pawandeep-prog/deepfake-voice/blob/master/demo_toolbox_collab.py
