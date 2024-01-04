#!/usr/bin/python3
#UTF-8

import os
import shutil
import locale
from plyer import notification
from crontab import CronTab
import getpass

def main():

    # Define the source file path
    source_file = os.path.realpath(__file__)

    # Define the destination directory
    destination_dir = os.path.expanduser('~/.cleaner')

    # Define the destination file path
    destination_file = os.path.join(destination_dir, os.path.basename(source_file))

    # Check if the file already exists in the destination directory
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    if not os.path.exists(destination_file):
        # Copy the file
        shutil.move(source_file, destination_dir)

    # Create a new cron tab that runs at every reboot if not already there
    username = getpass.getuser()
    cron = CronTab(user=username)
    for job in cron:
        if  'cleaner.py' not in job.command:
            job = cron.new(command='/usr/bin/python3 ~/.cleaner/cleaner.py')
            job.every_reboot()
            cron.write()
    if  len(cron.crons) == 0:
            job = cron.new(command='/usr/bin/python3 ~/.cleaner/cleaner.py')
            job.every_reboot()
            cron.write()

    # Get locale & specify the path
    def_locale = locale.getdefaultlocale()
    if def_locale[0][:2] == "en":
        path_en = os.path.expanduser('~/Downloads')
    else:
        path = os.path.expanduser('~/Téléchargements/')

    # use listdir() method from the os module
    files = os.listdir(path)

    for file in files:
        # Get the file extension
        extension = os.path.splitext(file)[1].strip('.')
        # Create a new directory path
        new_dir = os.path.join(path, extension)
        # Create a new directory if it doesn't exist
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        # Define the destination path
        destination_path = os.path.join(new_dir, file)
        # Move the file to the new directory if the destination file doesn't exist
        if not os.path.exists(destination_path):
            shutil.move(os.path.join(path, file), new_dir)


    # Send a desktop notification
    file_counts = {}
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]

    for subfolder in subfolders:
        file_counts[os.path.basename(subfolder)] = len(os.listdir(subfolder))

    message = '\n'.join([f'{folder}: {count} files' for folder, count in file_counts.items()])

    notification.notify(
        title='File Organization Complete',
        message=message,
        app_name='File Organizer Script',
        timeout=10,  # seconds
)

if __name__ == "__main__":
    main()