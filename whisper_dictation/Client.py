import argparse
import socket

def main(args: argparse.Namespace):

    language: str = args.language
    server_address = ('localhost', args.port)

    print(f"Connecting to server and sending language: {language}")

    # Create a socket and connect to the server
    sock = socket.create_connection(server_address)

    # Send the language code
    sock.sendall(language.encode())

    # Close the socket
    sock.close()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Select a language for the Dictation app using the OpenAI whisper ASR model.'
    )
    parser.add_argument(
        '-l',
        '--language',
        type=str,
        choices=['en', 'zh', 'de'],
        default='en',
        help=('Specify the two-letter language code to use when connecting to the server. '
              'Options: en (English), zh (Chinese), de (German). Default: en.')
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=9000,
        help=
        'Specify the port to run the server on. Default: 9000.'
        'This is helpful if the default port is already in use.'
    )

    args = parser.parse_args()
    return args

def run_client():
    args = parse_args()
    print(args.port)
    main(args)

if __name__ == "__main__":
    run_client()