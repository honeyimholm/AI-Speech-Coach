# ai_speech_coach

This is the repo for the speech corrector hackathon submission. This project performs real time detection of "Uhm" and triggers an arduino piezo buzzer to give real time feedback.

# Architecture

[TODO] neural network architecture/pipeline
[TODO] upload arduino diagram

# Setup

You'll need an arduino attached via serial and a piezo buzzer attached like this: [TODO] 

In the code the port is set to COM8 which will need to change based on your configuration. 

If you don't have an arduino attached you can just set the variable "ARDUINO_ENABLED" in driver.py to false

You can also configure the following variables to in driver.py 

```
# only output detection if prediction exceeds confidence threshold
CONFIDENCE_THRESHOLD = .95
# min time between detections
TIME_THRESHOLD = 1
```

# Usage

Start the arduino code in buzzer.ino 

```run python driver.py```

If you say "uhm" you should recieve a terminal output with the confidence which will trigger the piezo buzzer:
>Uhm detected! Confidence: 0.9995760321617126

# Results
[TODO] upload trials

# Next Steps
I'd like to make this a full wearable using the nano ble sense 33. This would allow for speech coaching in more natural environments i.e. casually talking to friends

Augmentation of the "uhm" dataset needs to be performed - there are a bit of false positives around words like "the"

I'll be uploading more details as an end-to-end tutorial soon!
