# TTS-Radio-Generator

I wanted a tool to generate sound files as radio calls for my DCS missions.
It should use a Text-To-Speech engine, add some white noise and a click sound at the start and the end of the "transmission".
I searched the web and found some existing projects which sounds more or less the tool I want to have.

- [radio-message-generator][1]:
    No binary release and I don't want to build it.

- [DCS_RadioComm_VoiceLineGenerator][2]:
    A nearly perfect match, but I needed the features which are planned for the future.

I had the idea to fork DCS_RadioComm_VoiceLineGenerator, add the featrures I needed by myself and make a merge request.
But the way DCS_RadioComm_VoiceLineGenerator is coded is above my Python skill. So I was forced to create this tool from scratch.
But the code adamclmns has shared was a great help and a good insperation. So many thanks to him for his work!

# Features

- Use Windows or Google Text-To-Speach engine to generate sound files
- Choose the voice used for generation
- Use a csv text file for batch processing, each line creates one sond file
- Optionally add white noise to the sound files
- Optionally add start and end click sounds
- target codec is ogg to save disk space and use it for DCS
- Configurable sound volumes for white noise and target file
- Configurable values for Low and High pass filters

# Prerequisits

If you want to run the script with Python you need:

- Python
- All libraries from requirements.txt (run install.cmd to get them)
- ffmpeg installed by chocolaty

I'll will to to create a all-in-one exe file for a people who don't want to setup Python.

# How to use the source code

- Save this repo somewhere onto your hard disk
- Install all prerequisits
- Run `tts-radio-generator.py` without any parameters
- It will use `./conf/default.yml` and `./conf/example.csv` to create sound files with Microsoft TTS
- Install as much languages as you like to your windows, if you want to use Windows Text-To-Speech with another voice
- Copy `default.yml` to a new file, e.g. `custom-myproject.yml`
- Copy `example.csv` to a new file, e.g. `custom-myproject.csv`
- Change both files to match your needs
- Run `tts-radio-generator.py -c ./conf/custom-myproject.yml`
- If you want to use Google TTS you can use `default-google.yml` as a template

# How to use the release

- Save the release somewhere onto your hard disk
- Unzip it
- Run `tts-radio-generator.exe` without any parameters
- It will use `./conf/default.yml` and `./conf/example.csv` to create sound files with Microsoft TTS
- Install as much languages as you like to your windows, if you want to use Windows Text-To-Speech with another voice
- Copy `default.yml` to a new file, e.g. `custom-myproject.yml`
- Copy `example.csv` to a new file, e.g. `custom-myproject.csv`
- Change both files to match your needs
- Run `tts-radio-generator.exe -c ./conf/custom-myproject.yml`
- If you want to use Google TTS you can use `default-google.yml` as a template

# ToDo

- Maybe add more TTS engines like AWS or Azure

[1]: <https://github.com/akaAgar/radio-message-generator>
[2]: <https://github.com/adamclmns/DCS_RadioComm_VoiceLineGenerator>
