import os
import sys
import time
import logging
import Config
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import BackupFunctionLib as b

class backup(LoggingEventHandler):
    def on_created(self, event):
        super(backup, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)
        b.inc_backup(Config.src_dir,Config.dst_dir,Config.md5file)
    
    

if __name__ == "__main__":
    # src_dir = sys.argv[1]if len(sys.argv) > 1 else '.'
    # dst_dir = sys.argv[2]if len(sys.argv) > 2 else './backup'
    # md5file = sys.argv[1]+'/md5.data'if len(sys.argv) > 1 else './md5.data'
    # log_file = sys.argv[1]+'/log.txt'if len(sys.argv) > 1 else './log.txt'

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=Config.log_file)
    b.full_backup(Config.src_dir,Config.dst_dir,Config.md5file)


    observer = Observer()
    event_handler = backup()
    observer.schedule(event_handler,Config.src_dir,True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()