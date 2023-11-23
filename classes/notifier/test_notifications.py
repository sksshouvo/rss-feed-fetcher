import os
import dbus
import dbus.mainloop.glib
import dbus.exceptions


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


class LinuxNotificationHandler:
    def show_notification(self, notification_details):
        bus = dbus.SessionBus()
        notifications = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
        interface = dbus.Interface(notifications, "org.freedesktop.Notifications")

        notification_id = str(os.getpid())

        notification_data = {"app_pid": notification_id}

        interface.Notify(
            notification_details.get("app_name"),
            0,
            notification_details.get("icon"),
            notification_details.get("title"),
            notification_details.get("message"),
            [],
            notification_data,
            10000
        )
        notifications.connect_to_signal("NotificationClosed", self.onclick_function)

    # def get_clicked_event(self, onclick_function):
    #     bus = dbus.SessionBus()
    #     notifier = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
    #     notifier.connect_to_signal("ActionInvoked", onclick_function)

    def onclick_function(self, notification_id, action, *args):
        # Assuming the notification_id contains the PID of the application
        try:
            pid = int(notification_id)  # Extract PID from the notification ID (this could be a unique identifier)
            os.system(f"wmctrl -ia {pid}")  # Bring the window with the specified PID to the foreground
        except ValueError:
            print("Invalid PID")


# lnh = LinuxNotificationHandler()
# lnh.show_notification("Random Title", "Random details")
