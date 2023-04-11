## Whisper-dictation

This is an app using openai's whisper to dictate on KDE wayland.  

The project is designed as a dictation server that runs at background (To avoid the time to load model each time starts the dictation) and a client to toggle if the server should be recording. You can assign a shortcut to toggle the server to start/stop the recording (`whisper_dicatation -l [language_code]`).

Whenever the dictation is stopped, the content will be sent to your clipboard and a notification will be displayed.

The project depends on the `kdialog` [package](https://archlinux.org/packages/extra/x86_64/kdialog/) and `wl-copy` (from `wl-clipboard` [package](https://github.com/bugaevc/wl-clipboard)).

This project is designed to work on KDE wayland. Other wayland platforms might work as well, but without the ability to send a notification.

## Installation

```
pip install whisper_dictation
```

## Usage

To start the project manually, you should use two terminals:

```
whisper_dictation daemon [--port 9000] [--model_name base]
```

See `whisper_dictation daemon --help for all the available models`

You can use a command to trigger the daemon, or assign a shortcut to this command in order to use it. Press once for start, and press the second time to stop the recording.

```
whisper_dictation say [--language en]
```

You should assign a language code, it can help with the performance especially using a small model.

Alternatively, you can use the systemd service unit provided inside this repo to make the daemon running in the background. Place it in your `~/.config/systemd/user/`, enable and start it.

## TODO

- [x] add system integration for a shortcut to start/stop dictation
- [ ] output the dictation to where the cursor is (planned as fcitx addon).
- [ ] optional(A system tray)


## Requirements

1. `wl-clipboard`
2. `kdialog`
