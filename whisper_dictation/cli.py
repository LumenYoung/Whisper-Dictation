import click
import socket
from whisper_dictation.DictationDeamon import run_daemon, parse_args, initializing_deamon # Assuming these are imported from your project
from whisper_dictation.WhisperDictator import WhisperDictator
import selectors

@click.group()
def cli():
    pass

@click.command()
@click.option('--port', default=9000, help='The port for the dictation server.')
def daemon(host, port):
    """Start the Whisper Dictation daemon."""

    args = parse_args()
    if args.port is not port:
        args.port = port
    dictator = initializing_deamon(args)
    selector: selectors.DefaultSelector = selectors.DefaultSelector()
    run_daemon('localhost', port, selector, dictator)

@click.command()
@click.option('--port', default=9000, help='The dictation server port to connect.')
@click.option('--language', default='en', help='Specify the language you want to use.')
def say(host, port, language):
    """Send a voice sample to the dictation server."""

    server_address = ('localhost', port)
    sock = socket.create_connection(server_address)
    sock.sendall(language.encode())
    sock.close()

cli.add_command(daemon)
cli.add_command(say)

if __name__ == "__main__":
    cli()