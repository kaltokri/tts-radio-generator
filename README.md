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

Python is able to process wav files directly, but for saving the file in ogg format ffmpeg is needed.
There are different way to get ffmpeg:

- The easiest is to use [chocolaty][3] to install [ffmpeg][4] with the command `choco install ffmpeg`
- Then change the value `FfMpegHome` in your yml file (an example is included in `defaul.yml`)

Another way is to download it directly from BtbN:
- Download [ffmpeg-master-latest-win64-gpl-shared.zip][5]
- Place it in the same folder as `tts-radio-generator.exe`
- Extract it and rename it to create the following structure: `ffmpeg\bin\ffmpeg.exe`
- Adopt the path to the bin folder in your yml configuration file (an example is included in `defaul.yml`)

# How to use the source code

If you want to run the script with Python you need:

- Python 3.x
- All libraries from requirements.txt (run `install.cmd`` to get them)
- Save this repo somewhere onto your hard disk
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
[3]: <https://chocolatey.org/install>
[4]: <https://community.chocolatey.org/packages/ffmpeg>
[5]: <https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip>
