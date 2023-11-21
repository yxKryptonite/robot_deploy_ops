import paramiko  # 用于调用scp命令
from scp import SCPClient
import time
import datetime
import os
import yaml

def get_scp_client(config_file="mm.yaml"):
    with open(config_file, "r") as f:
        cfg = yaml.load(f.read(), Loader=yaml.FullLoader)

    host = cfg['ip']  #服务器ip地址
    port = cfg['port']  # 端口号
    username = cfg['name']  # ssh 用户名
    password = cfg['pwd']  # 密码

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, username, password)
    scpclient = SCPClient(ssh_client.get_transport(),socket_timeout=15.0)
    
    return scpclient

# 将指定目录的图片文件上传到服务器指定目录
# remote_path远程服务器目录
# file_path本地文件夹路径
# img_name是file_path本地文件夹路径下面的文件名称
def upload_file(scpclient, remote_path, file_path):
    # img_name示例：07670ff76fc14ab496b0dd411a33ac95-6.webp
    scpclient.put(file_path, remote_path)

def download_file(scpclient, remote_path, file_path):
    scpclient.get(remote_path, file_path)
    
def generate_code():
    return str(datetime.datetime.now().timestamp()).replace('.', '')
    
def wait_for_result(scpclient, remote_path, file_path, code):
    while True:
        try:
            download_file(scpclient, remote_path, file_path)
            with open(file_path, "r") as f:
                result, new_code = f.read().split(' ')
            if new_code != code:
                return int(result), new_code
            else:
                time.sleep(0.1)
                continue
        except:
            time.sleep(0.1)
            continue

if __name__ == "__main__":
    start = time.time()
    scpclient = get_scp_client("mm.yaml")
    print('ssh time:', time.time()-start, 's')
    upload_file(scpclient, remote_path='/data/xxx/', file_path='mm.yaml')
    print(time.time()-start)
    start = time.time()
    upload_file(scpclient, remote_path='/data/xxx/', file_path='mm.yaml')
    print(time.time()-start)