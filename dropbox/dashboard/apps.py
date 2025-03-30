import os
import threading

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            from .udp_receiver import start_udp_receiver
            thread = threading.Thread(target=start_udp_receiver, daemon=True)
            thread.start()

