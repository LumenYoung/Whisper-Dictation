import asyncio
from dbus_next import Message, BusType, Variant
from dbus_next.aio import MessageBus

async def main():
    bus = await MessageBus(bus_type=BusType.SESSION).connect()

    # Fetch introspection data
    introspect = await bus.introspect("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop")
    portal = bus.get_proxy_object("org.freedesktop.portal.Desktop",
                                  "/org/freedesktop/portal/desktop",
                                  introspect)

    global_shortcuts_interface = portal.get_interface("org.freedesktop.portal.GlobalShortcuts")

    app_id = ""  # Use your application's ID here

    # Create a session
    session_options = {}
    session_handle = await global_shortcuts_interface.call_create_session(session_options)
    print("Session created:", session_handle)

    # Bind a global shortcut
    shortcuts = [
        (
            "shortcut_1",
            {
                "description": "My custom global shortcut",
                "preferred_trigger": "Ctrl+Alt+D"
            }
        )
    ]
    bind_options = {}
    request_handle = await global_shortcuts_interface.call_bind_shortcuts(session_handle, shortcuts, "", bind_options)
    print("Shortcuts binding requested:", request_handle)

    def on_activated(*args):
        if args[0] == session_handle and args[1] == "shortcut_1":
            print("Shortcut activated")

    bus.add_message_handler(lambda msg: on_activated(*msg.body) if msg.member == "Activated" else None)

    # Keep the script running to listen for the "Activated" signal
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Exiting...")