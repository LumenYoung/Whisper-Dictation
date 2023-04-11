import click
import socket
# Assuming these are imported from your project
from whisper_dictation.DictationDeamon import run_daemon, parse_args, initializing_daemon
from whisper_dictation.WhisperDictator import WhisperDictator
import selectors


@click.group()
def cli():
    pass


@click.command()
@click.option('--port', default=9000, help='The port for the dictation server.')
@click.option('--model_name', default="base", type=click.Choice(['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large']), help='The the whisper model used on the dictation server.')
def daemon(port, model_name):
    """Start the Whisper Dictation daemon."""

    dictator = initializing_daemon(model_name=model_name)
    selector: selectors.DefaultSelector = selectors.DefaultSelector()
    run_daemon('localhost', port, selector, dictator)

@click.command()
def hello():
    click.echo('Hello World!')


@click.command()
@click.option('--port', default=9000, help='The dictation server port to connect.')
@click.option('--language', default='en', help='Specify the language you want to use.')
def say(port, language):
    """Send a voice sample to the dictation server."""

    server_address = ('localhost', port)
    sock = socket.create_connection(server_address)
    sock.sendall(language.encode())
    sock.close()


cli.add_command(daemon)
cli.add_command(hello)
cli.add_command(say)

if __name__ == "__main__":
    cli()
