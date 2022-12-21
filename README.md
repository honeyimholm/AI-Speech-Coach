# ai_speech_coach

This project performs real time detection of the filler word "Uhm" and triggers an arduino piezo buzzer to give real time feedback. In some limited tests I was able to reduce the amount of "uhm"s per minute of speaking when given this buzzer feedback

![hippo](https://s3.gifyu.com/images/ezgif.com-gif-makerde9df0ac86959cd5.gif)

# Setup

You'll need an arduino attached via serial and a piezo buzzer attached like this: 

![arduino](https://i.imgur.com/JJfMkgx.jpg) 

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
In some very limited tests I did on myself it reduced the amount of "umms" I said per minute of speaking from 5.4 (yikes!) to 3.4 (still yikes!).

![trial](https://i.imgur.com/dtrxDTa.png)

# Next Steps
I'd like to make this a full wearable using the nano ble sense 33. This would allow for speech coaching in more natural environments i.e. casually talking to friends

Augmentation of the "uhm" dataset needs to be performed - there are a bit of false positives around words like "the"

I'll be uploading more details as an end-to-end tutorial soon!
