import os
import pyttsx3
import sys
import getopt
from google.cloud import texttospeech
from pydub import AudioSegment, generators
from ruamel.yaml import YAML
from os.path import exists
#from charset_normalizer import md__mypyc

version='0.0.3'

###############################################################################
# Function to show installed tts voices
###############################################################################
def showVoices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("\nCurrently available System voices:")
    i=0
    configuredVoiceFound = False
    for voice in voices:
        if voice.id == conf_voice:
            configuredVoiceFound = True
        print( f"[{i}]: {voice.id}" )
        i=i+1
    print("You can use the id of the desired voice in the config file.")
    if not configuredVoiceFound:
        print( f"\nERROR: Configured voice not found on your system!" )
        print( f"Config: {conf_voice}")
        print("Please double check your configuration for typos.")
        print("System default [0] is used!")
    else:
        print( f"Using {conf_voice}")
    print("\n")

###############################################################################
# Function to find silence at the start or end of a sound
###############################################################################
def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    # sound is a pydub.AudioSegment
    # silence_threshold in dB
    # chunk_size in ms
    # iterate over chunks until you find the first one with sound
    trim_ms = 0

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

###############################################################################
# Run when script is executed.
###############################################################################
if __name__ == '__main__':
    print( f"\nTool version {version} started\n" )

    confFilePath = "./conf/default.yml"

    # Parse command line arguments
    argv = sys.argv[1:]
    try:
        options, args = getopt.getopt(argv, "c:")
    except:
        print("Error: Command line argument unknown")

    for name, value in options:
        if name in ['-c']:
            confFilePath = value

    # Read the configuration file
    print( f"\nUsing configuration: {confFilePath}" )
    confFile = open(confFilePath, "r")

    yaml=YAML(typ='safe')
    conf=yaml.load(confFile)

    # Configuration values
    outFolderWav = conf['Config']['Output']['DirWav']
    outFolderOgg = conf['Config']['Output']['DirOgg']

    conf_voice = conf['Config']['TTS']['Voice']
    conf_volume = conf['Config']['Audio']['Volume']
    conf_filter_boost = conf['Config']['Audio']['Filter']['Boost']
    conf_white_noise_decrease = conf['Config']['Audio']['WhiteNoise']['VolumeDecrease']
    conf_high_pass_filter_arg = conf['Config']['Audio']['Filter']['ArgHighPass']
    conf_low_pass_filter_arg = conf['Config']['Audio']['Filter']['ArgLowPass']
    # Audio files for 'click in' and 'click out'
    conf_IN_WAV = conf['Config']['Audio']['PreSound']['File']
    conf_OUT_WAV = conf['Config']['Audio']['PostSound']['File']
    conf_ffmpegHome = conf['Config']['FfMpegHome']
    conf_TtsEngine = conf['Config']['TTS']['Engine']

    print("Using FFMPEG_HOME: ", conf_ffmpegHome)
    if exists(conf_ffmpegHome+"\\ffmpeg.exe"):
        AudioSegment.converter = conf_ffmpegHome+"\\ffmpeg.exe"
        AudioSegment.ffmpeg = conf_ffmpegHome+"\\ffmpeg.exe"
        AudioSegment.ffprobe = conf_ffmpegHome+"\\ffprobe.exe"
    else:
        print("ERROR: ffmpeg not found!")
        print("Download and extract ffmpeg and change the path in your config file.\n")
        sys.exit(1)

    # Show all installed voices and the one which will be used
    if conf_TtsEngine == 'Windows':
        print("Using TextToSpeech engine from Windows.")
        showVoices()
        engine = pyttsx3.init()
        engine.setProperty('volume', conf['Config']['TTS']['Volume'])
        engine.setProperty('rate', conf['Config']['TTS']['Rate'])
        engine.setProperty('voice', conf_voice)

    if conf_TtsEngine == 'Google':
        print("Using TextToSpeech engine from Google.")
        print("\nHere you will find a list with all voices:")
        print("https://cloud.google.com/text-to-speech/docs/voices\n")
        if exists(conf['Config']['TTS']['CredFile']):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = conf['Config']['TTS']['CredFile']
        else:
            sys.exit("Unable to find json file with google credentials specified in the config.\n")

        client = texttospeech.TextToSpeechClient()
        voice = texttospeech.VoiceSelectionParams(
            language_code=(conf['Config']['TTS']['Voice'])[:5],
            name=conf['Config']['TTS']['Voice']
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,
            speaking_rate=conf['Config']['TTS']['Rate'],
            pitch = conf['Config']['TTS']['Pitch'],
            volume_gain_db = conf['Config']['TTS']['Volume'],
            effects_profile_id=['large-automotive-class-device']
        )

    # Read file with text lines for tts
    print( "Reading text lines from csv file\n" )
    textfile = open( conf['Config']['InputCsv'], 'r' )
    allLines = textfile.readlines()
    # Remove all blank lines
    allLines = (line.rstrip() for line in allLines)
    allLines = (line for line in allLines if line)

    # Process each line with text
    for line in allLines:

        fileNameWav = line.replace(" ", "-") + ".wav"
        outFullPathWav = outFolderWav + "/" + fileNameWav

        # Run TextToSpeech and save the result as WAV file
        if conf_TtsEngine == 'Windows':
            engine.save_to_file(line, outFullPathWav)
            engine.runAndWait()
            print(f'Temporary wav file: {outFullPathWav}')

        if conf_TtsEngine == 'Google':
            synthesis_input = texttospeech.SynthesisInput(text=line)
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            # The response's audio_content is binary.
            with open(outFullPathWav, "wb") as out:
                # Write the response to the output file.
                out.write(response.audio_content)
                print(f'Temporary wav file: {outFullPathWav}')

        # Audio manipulation
        audioStream = AudioSegment.from_file(outFullPathWav)

        if conf['Config']['Audio']['Trimm']:
            audioDuration=len(audioStream)
            start_trim = detect_leading_silence(audioStream)
            end_trim = detect_leading_silence(audioStream.reverse())

            print( f"audioDuration: {audioDuration}" )
            print( f"start_trim: {start_trim}" )
            print( f"end_trim: {end_trim}" )

            audioStreamTrimmed = audioStream[start_trim:audioDuration-end_trim]
            audioStream = audioStreamTrimmed
            audioDuration=len(audioStream)
            print( f"New audioDuration: {audioDuration}" )

        if conf['Config']['Audio']['Filter']['Apply']:
            audioStream = audioStream.high_pass_filter(conf_high_pass_filter_arg)
            audioStream = audioStream.low_pass_filter(conf_low_pass_filter_arg)
            audioStream = audioStream + conf_filter_boost

        # Adding pre sound
        if conf['Config']['Audio']['PreSound']['Add']:
            print( f"Adding pre sound file:  '{conf_IN_WAV}'" )
            startClick = AudioSegment.from_wav(conf_IN_WAV)
            startClick = startClick - conf['Config']['Audio']['PreSound']['VolumeDecrease']
            audioStream = startClick + audioStream

        # Adding post sound
        if conf['Config']['Audio']['PostSound']['Add']:
            print( f"Adding post sound file: '{conf_OUT_WAV}'\n" )
            endClick = AudioSegment.from_wav(conf_OUT_WAV)
            endClick = endClick - conf['Config']['Audio']['PostSound']['VolumeDecrease']
            audioStream = audioStream + endClick

        audioDuration=len(audioStream)

        # white noise profile generated
        if conf['Config']['Audio']['WhiteNoise']['Add']:
            print( f"Adding white noise" )
            whiteNoise = generators.WhiteNoise().to_audio_segment(duration=audioDuration)
            audioStream = audioStream.overlay(whiteNoise - conf_white_noise_decrease)

        # bump volume of all audio
        audioStream = audioStream + conf_volume

        # Save target file
        fileNameOgg = fileNameWav.replace(".wav", "")
        postfix = ""
        if conf['Config']['Output']['AddLengthPostfix']:
            postfix = f"_{audioDuration}"
            postfix = postfix[:-1]
            print( f"Soundfile is {audioDuration} ms long. Adding postfix {postfix}")
        fileNameOgg = f"{fileNameOgg}{postfix}.ogg"
        outFullPathOgg = outFolderOgg + "/" + fileNameOgg
        print( f"Saving target file to: {outFullPathOgg}\n" )
        audioStream.export(outFullPathOgg, format='ogg')

    print("\nSkript finished!\n")
