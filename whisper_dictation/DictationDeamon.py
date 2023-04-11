import socket
import selectors
from typing import List
import argparse
from whisper import load_model
from whisper_dictation.WhisperDictator import WhisperDictator, Transcriber

recording: bool = False


def initializing_daemon(model_name:str) -> WhisperDictator:

    print("Loading Model....")
    model = load_model(model_name)

    transcriber = Transcriber(model)
    dictator = WhisperDictator(transcriber=transcriber, save_audio=True)

    print("Load Complete!")
    return dictator


def run_daemon(host, port, selector, dictator):
    # Initialize daemon
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    sock.setblocking(False)
    selector.register(sock, selectors.EVENT_READ, event_handler(
        dictator))  # Pass the dictator instance here

    # Event loop
    while True:
        events = selector.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


def event_handler(dictator):
    def wrapper(sock):
        global recording

        # Accept incoming connections
        conn, addr = sock.accept()
        print('Accepted connection from:', addr)

        # Receive language from the client, assuming a single language code from the client
        language = conn.recv(2).decode()

        if recording:
            # Stop recording
            dictator.stop()
        else:
            # Start recording
            dictator.start(language)

        recording = not recording
        print(
            f'State toggled: {"On" if recording else "Off"}, Language: {language}')

        # Close connection
        conn.close()

    return wrapper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Dictation app using the OpenAI whisper ASR model.')
    parser.add_argument(
        '-m',
        '--model_name',
        type=str,
        choices=[
            'tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en',
            'medium', 'medium.en', 'large'
        ],
        default='base',
        help='Specify the whisper ASR model to use. Options: tiny, base, small, medium, or large. '
        'To see the  most up to date list of models along with model size, memory footprint, and estimated '
        'transcription speed check out this [link](https://github.com/openai/whisper#available-models-and-languages). '
        'Note that the models ending in .en are trained only on English speech and will perform better on English '
        'language. Note that the small, medium, and large models may be slow to transcribe and are only recommended '
        'if you find the base model to be insufficient. Default: base.')
    parser.add_argument(
        '-l',
        '--language',
        type=str,
        default=None,
        help='Specify the two-letter language code (e.g., "en" for English) to improve recognition accuracy. '
        'This can be especially helpful for smaller model sizes.  To see the full list of supported languages, '
        'check out the official list [here](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py).'
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=9000,
        help='Specify the port to run the server on. Default: 9000.'
        'This is helpful if the default port is already in use.'
    )

    args = parser.parse_args()

    # if args.language is not None:
    #     args.language = args.language.split(',')

    if args.model_name.endswith('.en') and args.language is not None and any(
            lang != 'en' for lang in args.language):
        raise ValueError(
            'If using a model ending in .en, you cannot specify a language other than English.'
        )

    return args


if __name__ == "__main__":
    pass

