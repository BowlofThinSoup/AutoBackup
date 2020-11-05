#实现数据完全备份与增量备份
import time,os,hashlib,sys,tarfile
import pickle as p

src_dir = 'E:/test'
dst_dir = "E:/backup"
md5file = 'E:/backup/md5.data'
log_file = 'E:/backup/log.txt'

def walkdir(folder):
    md5dict = {}
    if os.path.exists(folder):
        contents = os.walk(folder)
        for path,folders,files in contents:
            for fname in files:
                full_path = os.path.join(path,fname)
                md5dict[full_path] = md5check(full_path)
        with open(md5file,'wb') as fobj:
            p.dump(md5dict,fobj)
    else:
        print("指定的目录不存在！")

def md5check(fname):
    if os.path.isfile(fname):
        m = hashlib.md5()
        with open(fname) as fobj:
            while True:
                data = fobj.read(4096)
                if not data:
                    break
                m.update(data.encode(encoding = "utf-8"))
        return m.hexdigest()
    else:
        print("校验文件不存在！")

def full_backup(src_dir,dst_dir,md5file):
    par_dir,base_dir = os.path.split(src_dir.rstrip("/"))
    back_name = "%s_full_%s.tar.gz" % (base_dir,time.strftime("%Y%m%d"))
    full_name = os.path.join(dst_dir,back_name)
    walkdir(src_dir)
    os.chdir(par_dir)
    tar = tarfile.open(full_name,'w:gz')
    tar.add(base_dir)
    tar.close()
    announce = "%s  All files have been backed up!\n" % time.strftime("%Y-%m-%d  %H:%M:%S")
    print(announce)
    with open(log_file,"a") as f:
        f.write(announce)

def inc_backup(src_dir,dst_dir,md5file):
    if os.path.exists(md5file):
        par_dir,base_dir = os.path.split(src_dir.rstrip("/"))
        back_name = "%s_inc_%s.tar.gz" % (base_dir,time.strftime("%Y%m%d"))
        full_name = os.path.join(dst_dir,back_name)
        md5new = {}
        if os.path.exists(src_dir):
            contents = os.walk(src_dir)
            for path,folders,files in contents:
                for fname in files:
                    full_path = os.path.join(path,fname)
                    md5new[full_path] = md5check(full_path)
            with open(md5file,'rb') as fobj:
                md5old = p.load(fobj)
            with open(md5file,'wb') as fobj:
                p.dump(md5new,fobj)
            os.chdir(par_dir)
            tar = tarfile.open(full_name,'w:gz')
            if len(md5new) < len(md5old):
                full_backup(src_dir,dst_dir,md5file)
            else:
                for key in md5new:
                    if md5old.get(key) != md5new[key]:
                        tar.add(key[key.find(base_dir):])
                tar.close()
                announce = "%s  some files have been changed!\n" % time.strftime("%Y-%m-%d  %H:%M:%S")
                print(announce)
                with open(log_file,"a") as f:
                    f.write(announce)

        else:
            print("指定的目录不存在！")
    else:
        full_backup(src_dir,dst_dir,md5file)

# if __name__ == "__main__":
    # src_dir = 'E:/test'
    # dst_dir = "E:/backup"
    # md5file = 'E:/backup/md5.data'
    # log_file = 'E:/backup/log.txt'
#     if time.strftime("%H") == "0":
#         full_backup(src_dir,dst_dir,md5file)
#     else:
#         inc_backup(src_dir,dst_dir,md5file)
