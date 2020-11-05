import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import myBack as b

class backup(LoggingEventHandler):
    def on_any_event(self, event):
        b.inc_backup(src_dir,dst_dir,md5file)
    

if __name__ == "__main__":
    src_dir = 'E:/test'
    dst_dir = "E:/backup"
    md5file = 'E:/backup/md5.data'
    log_file = 'E:/backup/log.txt'
    # src_dir = sys.argv[1]if len(sys.argv) > 1 else '.'
    # dst_dir = sys.argv[2]if len(sys.argv) > 2 else './backup'
    # md5file = sys.argv[1]+'/md5.data'if len(sys.argv) > 1 else './md5.data'
    # log_file = sys.argv[1]+'/log.txt'if len(sys.argv) > 1 else './log.txt'

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_file)
    b.full_backup(src_dir,dst_dir,md5file)
    print("ok")


    observer = Observer()
    event_handler = backup()
    observer.schedule(event_handler,src_dir,True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()