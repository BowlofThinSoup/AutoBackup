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