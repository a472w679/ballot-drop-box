#!/usr/bin/env python3

# Name of code artifact: start.py 
# Brief description of what the code does: starts the entire drop box scanning system
# Programmer’s name: Xavier Ruyle   
# Date the code was created: 3/19/25
# Preconditions: virtual environment reuqirments installed  and everything setup following the README.md
# Postconditions: dropbox scanning system started
# Return values or types, and their meanings: N/A
# Error and exception condition values or types that can occur, and their meanings: N/A
# Side effects: 
# Invariants: N/A

# TODO: make a soft link to the script on the desktop of the raspberry pi

import os
import subprocess
import signal 
import time
import webbrowser


# TODO: NEED TO TEST ON RASPBERRY PI 
terminal_type = "" 

script_dir = os.path.dirname(os.path.realpath(__file__))

# Path to the virtual environment's activate script
venv_activate_path = os.path.join(script_dir, "..", ".venv", "bin", "activate")  
udevadm_command = "sudo udevadm control --reload && sudo udevadm trigger"

django_path = os.path.join(script_dir, "manage.py")
django_command = f". {venv_activate_path} && {terminal_type} python3 {django_path} runserver"  

scanning_path = os.path.join(script_dir, "scanner/scanning.py")
scanning_command = f". {venv_activate_path} && {terminal_type} python3 {scanning_path}"  

# List to hold the process objects
processes = []


def run_command(command): 
    try:
        # Construct the full command to activate the venv and run the script
        process = subprocess.Popen(command, shell=True)
        processes.append(process)
        print(f"Started {command} with PID {process.pid}\n")
    except Exception as e:
        print(f"Failed to start {command}: {e}\n")

def open_frontend(): 
    # Django development server URL
    django_url = "http://127.0.0.1:8000/"
    try:
        webbrowser.get('chromium').open(django_url)
        print("----------")
        print(f"OPENING FRONT END AT {django_url}")
        print("----------\n")
    except Exception as e:
        print(f"Failed to open {django_url} in the browser: {e}")


if __name__ == "__main__": 
    print("---------------")
    print("SCANNING SYSTEM STARTING")
    print("---------------\n")

    run_command(udevadm_command)
    run_command(django_command)
    time.sleep(1) 
    open_frontend()
    run_command(scanning_command)

    # Wait for all processes to complete
    for process in processes:
        process.send_signal(signal.SIGINT)
        process.wait()


    # attempting to reattach scanner to kernel 
    
    '''
    except KeyboardInterrupt:  # this is out of place but it's the only way I could get the scanner to reattach
        dev = usb.core.find(idVendor=0x0c2e, idProduct=0x0aaf)
        if dev is None:
            raise ValueError('USB device not found')

        dev.reset()
        dev.attach_kernel_driver(0)
        print("Reattached USB device to kernel driver")
    '''




    print("All processes have completed.")
