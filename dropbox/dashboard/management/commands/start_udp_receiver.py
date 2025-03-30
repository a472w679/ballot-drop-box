import threading

from dashboard.udp_receiver import start_udp_receiver
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts the UDP receiver thread'

    def handle(self, *args, **options):
        thread = threading.Thread(target=start_udp_receiver, daemon=True)
        thread.start()
        self.stdout.write("UDP receiver started")
        while True:  # Keep command running
            pass
