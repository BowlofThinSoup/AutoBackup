import time,os,tarfile,pickle,json
from apscheduler.schedulers.blocking import BlockingScheduler
import Config

#全量备份函数
def full_backup(src_dir,dst_dir,log_file):
    par_dir,base_dir = os.path.split(src_dir.rstrip("/"))
    back_name = "%s_full_%s.tar.gz" % (base_dir,time.strftime("%Y%m%d"))
    full_name = os.path.join(dst_dir,back_name)
    os.chdir(par_dir)
    tar = tarfile.open(full_name,'w:gz')
    tar.add(base_dir)
    tar.close()
    announce = "\n"+"%s  All files have been backed up!\n" % time.strftime("%Y-%m-%d  %H:%M:%S")+"\n"
    print(announce)
    with open(log_file,"a") as f:
        f.write(announce)

#创建任务
def func():
    full_backup(Config.src_dir,Config.dst_dir,Config.log_file)


def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,每天备份
    scheduler.add_job(func, 'cron', day_of_week='0-6',hour=23, minute=59,id='DilyBackup')
    # scheduler.add_job(func, 'interval', seconds=15,id='DilyBackuptest')
    scheduler.start()

dojob()