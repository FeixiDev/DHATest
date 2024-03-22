import time
import utils
import action


class TestOperation:
    def __init__(self):
        self.obj_yaml = utils.Yaml()
        self.yaml_info = self.obj_yaml.yaml_read()
        self.obj_diskful_01 = utils.SSHconn(host=self.yaml_info['diskful_node_info'][0]['ip']
                                     ,password=self.yaml_info['diskful_node_info'][0]['password'])
        self.obj_diskful_02 = utils.SSHconn(host=self.yaml_info['diskful_node_info'][1]['ip']
                                     ,password=self.yaml_info['diskful_node_info'][1]['password'])
        self.obj_diskless = utils.SSHconn(host=self.yaml_info['diskless_node_info']['ip']
                                     ,password=self.yaml_info['diskless_node_info']['password'])
        self.obj_go_meter = action.GoMeter()
        self.obj_check = action.Check()
        self.cmd_check_drbd = f"drbdadm status {self.yaml_info['resource_name']}"

    def diskless_shutdown(self):
        action.check_go_meter_exist(self.obj_diskless)
        print("使用多线程：在diskless节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskless)
        time.sleep(10)
        print(f"shutdown关闭其中一台diskful节点：{self.yaml_info['diskful_node_info'][1]['name']}")
        utils.exec_cmd("shutdown now",self.obj_diskful_02)
        time.sleep(5)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd,self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info,self.yaml_info["diskful_node_info"][1]["name"])

        print(f'请恢复{self.yaml_info["diskful_node_info"][1]["name"]}的电源')
        time.sleep(120)

        info = utils.exec_cmd(self.cmd_check_drbd,self.obj_diskful_01)
        self.obj_check.check_node_connection(info,self.yaml_info["diskful_node_info"][1]["name"])

        print("在diskless节点使用go-meter compare")
        self.obj_go_meter.go_meter_compare(self.obj_diskless)
        print("diskless shutdown 完成")

    def diskless_poweroff(self):
        action.check_go_meter_exist(self.obj_diskless)
        print("使用多线程：在diskless节点使用go-meter写")
        time.sleep(10)
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskless)
        print(f"poweroff关闭其中一台diskful节点：{self.yaml_info['diskful_node_info'][1]['name']}")
        utils.exec_cmd("poweroff", self.obj_diskful_02)
        time.sleep(5)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info["diskful_node_info"][1]["name"])

        print(f'请恢复{self.yaml_info["diskful_node_info"][1]["name"]}的电源')
        time.sleep(120)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info["diskful_node_info"][1]["name"])

        print("在diskless节点使用go-meter compare")
        self.obj_go_meter.go_meter_compare(self.obj_diskless)
        print("diskless poweroff 完成")

    def diskless_ifconfig(self):
        action.check_go_meter_exist(self.obj_diskless)
        print("使用多线程：在diskless节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskless)
        time.sleep(5)
        print(f"down掉diskless节点的网卡：{self.yaml_info['diskless_node_info']['name']}")
        utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']} down", self.obj_diskless)
        time.sleep(2)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}",self.obj_diskless)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskless_node_info']['name'])

        print(f"up {self.yaml_info['diskless_node_info']['name']}的网卡")
        utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']} up",self.obj_diskless)
        utils.exec_cmd(f"nmcli d connect {self.yaml_info['diskless_node_info']['NIC']}",self.obj_diskless)
        time.sleep(2)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}",self.obj_diskless)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskless_node_info']['name'])

        print("在diskless节点使用go-meter compare")
        self.obj_go_meter.go_meter_compare(self.obj_diskless)
        print("diskless ifconfig 完成")

    def diskless_line(self):
        action.check_go_meter_exist(self.obj_diskless)
        print("使用多线程：在diskless节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskless)

        print(f"请拔掉diskless节点的网线：{self.yaml_info['diskless_node_info']['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}", self.obj_diskless)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskless_node_info']['name'])

        print(f"请恢复diskless节点的网线：{self.yaml_info['diskless_node_info']['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}", self.obj_diskless)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskless_node_info']['name'])

        self.obj_go_meter.go_meter_compare(self.obj_diskless)

    def diskless_port(self):
        obj_telnet = utils.Telnetconn(ip=self.yaml_info['switch_info']['ip'])
        action.check_go_meter_exist(self.obj_diskless)
        print("使用多线程：在diskless节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskless)

        print(f"关断diskless节点的端口：{self.yaml_info['diskless_node_info']['name']}")
        obj_telnet.exec_cmd("configure en")
        obj_telnet.exec_cmd("configure terminal")
        obj_telnet.exec_cmd(f"interface {self.yaml_info['diskless_node_info']['port']}")
        obj_telnet.exec_cmd("shutdown")
        time.sleep(2)

        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}", self.obj_diskless)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskless_node_info']['name'])

        print(f"恢复diskless节点的端口：{self.yaml_info['diskless_node_info']['name']}")
        obj_telnet.exec_cmd("no shutdown")
        time.sleep(2)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskless_node_info']['name'])

        self.obj_go_meter.go_meter_compare(self.obj_diskless)

    def diskless_switch(self):
        action.check_go_meter_exist(self.obj_diskless)
        print("使用多线程：在diskless节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskless)

        print(f"请关闭交换机：{self.yaml_info['diskless_node_info']['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}", self.obj_diskless)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskless_node_info']['name'])

        print(f"请开启交换机：{self.yaml_info['diskless_node_info']['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskless_node_info']['NIC']}", self.obj_diskless)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskless_node_info']['name'])

        self.obj_go_meter.go_meter_compare(self.obj_diskless)

    def diskful_shutdown(self):
        action.check_go_meter_exist(self.obj_diskful_01)
        print("使用多线程：在其中一个diskful节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskful_01)
        time.sleep(10)
        print(f"shutdown关闭另一台diskful节点：{self.yaml_info['diskful_node_info'][1]['name']}")
        utils.exec_cmd("shutdown now",self.obj_diskful_02)
        time.sleep(15)
        self.obj_go_meter.check_go_meter_status(thread1)

        time.sleep(10)
        info = utils.exec_cmd(self.cmd_check_drbd,self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info,self.yaml_info["diskful_node_info"][1]["name"])

        print(f'请恢复{self.yaml_info["diskful_node_info"][1]["name"]}的电源')
        time.sleep(120)

        info = utils.exec_cmd(self.cmd_check_drbd,self.obj_diskful_01)
        self.obj_check.check_node_connection(info,self.yaml_info["diskful_node_info"][1]["name"])
        print("在diskful节点使用go-meter compare")
        self.obj_go_meter.go_meter_compare(self.obj_diskful_01)
        print("diskful shutdown 完成")

    def diskful_poweroff(self):
        action.check_go_meter_exist(self.obj_diskful_01)
        print("使用多线程：在其中一个diskful节点使用go-meter写")
        time.sleep(10)
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskful_01)
        print(f"poweroff关闭另一台diskful节点：{self.yaml_info['diskful_node_info'][1]['name']}")
        utils.exec_cmd("poweroff", self.obj_diskful_02)
        time.sleep(5)
        self.obj_go_meter.check_go_meter_status(thread1)
        time.sleep(5)
        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info["diskful_node_info"][1]["name"])

        print(f'请恢复{self.yaml_info["diskful_node_info"][1]["name"]}的电源')
        time.sleep(120)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info["diskful_node_info"][1]["name"])

        print("在diskful节点使用go-meter compare")
        self.obj_go_meter.go_meter_compare(self.obj_diskful_01)
        print("diskful poweroff 完成")

    def diskful_ifconfig(self):
        action.check_go_meter_exist(self.obj_diskful_01)
        print("使用多线程：在其中一个diskful节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskful_01)

        print(f"down掉此diskful节点的网卡：{self.yaml_info['diskful_node_info'][0]['name']}")
        utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info'][0]['NIC']} down", self.obj_diskful_01)
        time.sleep(2)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info'][0]['NIC']}",self.obj_diskful_01)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskful_node_info'][0]['name'])

        print(f"up {self.yaml_info['diskful_node_info'][0]['name']}的网卡")
        utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info'][0]['NIC']} up",self.obj_diskful_01)
        utils.exec_cmd(f"nmcli d connect {self.yaml_info['diskful_node_info'][0]['NIC']}",self.obj_diskful_01)
        time.sleep(2)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info'][0]['NIC']}",self.obj_diskful_01)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskful_node_info'][0]['name'])

        print("在diskful节点使用go-meter compare")
        self.obj_go_meter.go_meter_compare(self.obj_diskful_01)
        print("diskful ifconfig 完成")

    def diskful_line(self):
        action.check_go_meter_exist(self.obj_diskful_01)
        print("使用多线程：在其中一个diskful节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskful_01)

        print(f"请拔掉diskful节点的网线：{self.yaml_info['diskful_node_info'][0]['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info']['NIC']}", self.obj_diskful_01)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskful_node_info'][0]['name'])

        print(f"请恢复diskful节点的网线：{self.yaml_info['diskful_node_info'][0]['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info'][0]['NIC']}", self.obj_diskful_01)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskful_node_info'][0]['name'])

        self.obj_go_meter.go_meter_compare(self.obj_diskful_01)

    def diskful_port(self):
        obj_telnet = utils.Telnetconn(ip=self.yaml_info['switch_info']['ip'])
        action.check_go_meter_exist(self.obj_diskful_01)
        print("使用多线程：在其中一个diskful节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskful_01)

        print(f"关断diskful节点的端口：{self.yaml_info['diskful_node_info'][0]['name']}")
        obj_telnet.exec_cmd("configure en")
        obj_telnet.exec_cmd("configure terminal")
        obj_telnet.exec_cmd(f"interface {self.yaml_info['diskful_node_info'][0]['port']}")
        obj_telnet.exec_cmd("shutdown")
        time.sleep(2)

        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info'][0]['NIC']}", self.obj_diskful_01)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskful_node_info'][0]['name'])

        print(f"恢复diskful节点的端口：{self.yaml_info['diskful_node_info'][0]['name']}")
        obj_telnet.exec_cmd("no shutdown")
        time.sleep(2)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskful_node_info'][0]['name'])

        self.obj_go_meter.go_meter_compare(self.obj_diskful_01)

    def diskful_switch(self):
        action.check_go_meter_exist(self.obj_diskful_01)
        print("使用多线程：在其中一个diskful节点使用go-meter写")
        thread1 = self.obj_go_meter.thread_go_meter_write(self.obj_diskful_01)

        print(f"请关闭交换机：{self.yaml_info['diskful_node_info'][0]['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info']['NIC']}", self.obj_diskful_01)
        self.obj_check.check_nic_down(info)
        self.obj_go_meter.check_go_meter_status(thread1)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_disconnection(info, self.yaml_info['diskful_node_info'][0]['name'])

        print(f"请开启交换机：{self.yaml_info['diskful_node_info'][0]['name']}")
        time.sleep(30)
        info = utils.exec_cmd(f"ifconfig {self.yaml_info['diskful_node_info']['NIC']}", self.obj_diskful_01)
        self.obj_check.check_nic_up(info)

        info = utils.exec_cmd(self.cmd_check_drbd, self.obj_diskful_01)
        self.obj_check.check_node_connection(info, self.yaml_info['diskful_node_info'][0]['name'])

        self.obj_go_meter.go_meter_compare(self.obj_diskful_01)
