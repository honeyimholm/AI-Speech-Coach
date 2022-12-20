import pyaudio
import struct
import numpy as np
import time
import serial
import tensorflow as tf

class ExportModelRealTime(tf.Module):
  def __init__(self, model):
    self.model = model

    # Accept either a string-filename or a batch of waveforms.
    # YOu could add additional signatures for a single wave, or a ragged-batch. 
    self.__call__.get_concrete_function(
        x=tf.TensorSpec(shape=(), dtype=tf.string))
    self.__call__.get_concrete_function(
       x=tf.TensorSpec(shape=[None, 16000], dtype=tf.float32))


  @tf.function
  def __call__(self, x):
    # If they pass a string, load the file and decode it. 
    # TODO: check if this is also float
    if x.dtype == tf.string:
      x = tf.io.read_file(x)
      x, _ = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000,)
      tf.print(x)
      tf.print(tf.reduce_max(x))
      tf.print(tf.reduce_min(x))
      tf.print(tf.shape(x))
      x = tf.squeeze(x, axis=-1)
      x = x[tf.newaxis, :]
    
    x = get_spectrogram(x)  
    result = self.model(x, training=False)
    
    class_ids = tf.argmax(result, axis=-1)
    class_names = tf.gather(label_names, class_ids)
    return {'predictions':result,
            'class_ids': class_ids,
            'class_names': class_names}

# we'll run detection on overlapping 1 second windows of audio to increase real time prediciton
buffered_vals = []
# chunk controls window offset - 4000 samples is a quarter second
chunk = 4000
sample_format = pyaudio.paInt16  
channels = 1
fs = 16000  

# each trial is 60 seconds
seconds = 30

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording!')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# initialize model 
imported_model = tf.saved_model.load("uhm_detector")
# saving this code for full walkthrough
# export = ExportModelRealTime(model)

#initialize serial communication with arduino for buzzer
ARDUINO_ENABLED = True
if(ARDUINO_ENABLED): arduino = serial.Serial('COM8', 9600, timeout=0)

# only output detection if prediction exceeds confidence threshold
CONFIDENCE_THRESHOLD = .95
# don't want to double count umm's
TIME_THRESHOLD = 1

# keep track of umm detections so overlapping windows don't double detect
prev_detection = 0
prev_umm_time = time.time()

# total umm count
umm_count = 0

for i in range(0, int(fs / chunk * seconds)):
    # audio is streamed as a string of bytes
    block = stream.read(chunk)
    count = len(block)/2
    format = "%dh"%(count)
    # convert stream to 16 bit signed int
    shorts = struct.unpack( format, block )
    # convert to normalized floats
    float_vals = [float(val)/32768  for val in shorts]
    if(i < fs/chunk): 
      buffered_vals += float_vals
      continue
    else:
      buffered_vals = buffered_vals[chunk:] + float_vals
      converted_frames = tf.convert_to_tensor(buffered_vals)
      converted_frames = tf.expand_dims(converted_frames, 0)
      prediction = imported_model(converted_frames)
      normalized_predictions = tf.nn.softmax(prediction["predictions"])
      confidence = normalized_predictions[0][prediction["class_ids"][0]]
      if(confidence > CONFIDENCE_THRESHOLD):
        if(prediction["class_names"][0] == "uhm" and time.time() - prev_umm_time > TIME_THRESHOLD):
          #keep track of total umm's 
          prev_umm_time = time.time()
          umm_count += 1
          # trigger arduino
          if(ARDUINO_ENABLED): arduino.write(b'u')
          print(f"Uhm detected! Confidence: {confidence}")

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
#close arduino serial port
arduino.close()
# print results
print(f"Final umm count: {umm_count}")