import re
import sys
from threading import Thread
import utils
import time

def check_go_meter_exist(obj_ssh):
    cmd1 = "ls"
    result = utils.exec_cmd(cmd1,obj_ssh)
    info1 = re.findall(r'(go-meter.yaml)',result)
    info2 = re.findall(r'(main)',result)
    try:
        if info1[0] == "go-meter.yaml" and info2[0] == "main":
            print("go-meter检测存在")
        else:
            print("go-meter检测不存在")
            sys.exit()
    except:
        print("go-meter检测不存在")
        sys.exit()

# def judge_node_status(obj_ssh):
#     a = False
#     while a is False:
#         break
#     return True


class Check:
    def __init__(self):
        pass

    def check_node_disconnection(self,info, dis_node_name):
        flag = re.findall(r'(%s) connection:Connecting' % dis_node_name, info)
        if len(flag) == 0:
            print(f"{dis_node_name}节点的drbdadm status状态异常")
            sys.exit()
        else:
            print(f"{dis_node_name}节点已被正常关闭")

    def check_node_connection(self,info, recon_node_name):
        flag = re.findall(r'(%s) role:Secondary' % recon_node_name, info)
        if len(flag) == 0:
            print(f"{recon_node_name}节点的drbdadm status状态异常")
            sys.exit()
        else:
            print(f"{recon_node_name}节点已被正常开启")

    def check_nic_down(self,info):
        flag = re.findall(r'RUNNING',info)
        if len(flag) >= 1:
            print(f"节点的网卡未失去RUNNING标签")
            sys.exit()
        else:
            print(f"节点的网卡已失去RUNNING标签")

    def check_nic_up(self,info):
        flag = re.findall(r'RUNNING',info)
        if len(flag) >= 1:
            print(f"节点的网卡已获得RUNNING标签")
        else:
            print(f"节点的网卡未获得RUNNING标签")
            sys.exit()


class GoMeter:
    def __init__(self):
        pass

    def go_meter_write(self,obj_ssh):
        cmd = "./main write"
        info = utils.exec_cmd(cmd,obj_ssh)
        return info

    def go_meter_compare(self,obj_ssh):
        cmd = "./main compare"
        info = utils.exec_cmd(cmd,obj_ssh)
        return info

    def thread_go_meter_write(self,obj_ssh):
        state = Thread(target=self.go_meter_write,args=(obj_ssh,))
        state.setDaemon(True)
        state.start()
        return state

    def thread_go_meter_compare(self,obj_ssh):
        state = Thread(target=self.go_meter_compare,args=(obj_ssh,))
        state.setDaemon(True)
        state.start()
        return state

    def check_go_meter_status(self,state):
        a = False
        while a is False:
            time.sleep(5)
            if state.is_alive() is True:
                print("go-meter运行中......")
            else:
                print("go-meter结束")
                break

if __name__ == "__main__":
    pass


