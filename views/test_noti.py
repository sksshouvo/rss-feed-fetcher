import asyncio
from desktop_notifier import DesktopNotifier

notifier = DesktopNotifier()

async def main():
    n = await notifier.send(title="Hello world!", message="Sent from Python")
    
    await asyncio.sleep(5)  # wait a bit before clearing notification

    await notifier.clear(n)  # removes the notification
    await notifier.clear_all()  # removes all notifications for this app

asyncio.run(main())