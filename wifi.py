#encoding: utf-8
import os,time
from xml.etree.ElementTree import ElementTree,Element
from tm import km
import Tkinter as tk
def read_xml(in_path):  
    '''''读取并解析xml文件 
       in_path: xml路径 
       return: ElementTree'''  
    tree = ElementTree()  
    tree.parse(in_path)  
    return tree  

def str2hex(str):
    return str.encode("hex").upper()
def exc_cmd(cmd):
    result = os.system(cmd)
    return result

def add_config(file_path):
    cmd = "netsh wlan add profile filename={}".format(file_path)
    print(cmd)
    exc_cmd(cmd)


def delet_config(ssid):
    cmd = "netsh wlan delete profile name=*"
    exc_cmd(cmd)

def connect_wifi(ssid):
    modifyconfig(ssid)
    cmd = "netsh wlan connect name={}".format(ssid)
    exc_cmd(cmd)

def disconnect_wifi():
    cmd = "netsh wlan disconnect"
    exc_cmd(cmd)

def modifyconfig(ssid):
    ssid_file = os.path.join(os.path.abspath('.'),"xml","ssid.xml").replace("\\","/")
    wifi_file = os.path.join(os.path.abspath('.'),"xml","wifi.xml").replace("\\","/")
    delet_config(ssid)
    tree = read_xml(ssid_file)
    root = tree.getroot()
    filename = root.find("{http://www.microsoft.com/networking/WLAN/profile/v1}name")
    filename.text = ssid
    config_node = root.find("{http://www.microsoft.com/networking/WLAN/profile/v1}SSIDConfig")
    ssid_node = config_node.find("{http://www.microsoft.com/networking/WLAN/profile/v1}SSID")
    hex_node = ssid_node.find("{http://www.microsoft.com/networking/WLAN/profile/v1}hex")
    name_node = ssid_node.find("{http://www.microsoft.com/networking/WLAN/profile/v1}name")
    hex_node.text = str2hex(ssid)
    name_node.text = ssid
    tree.write(wifi_file)
    add_config(wifi_file)
def begin(ssid,run_time=20):
    connect_wifi(ssid)
    timeOut = 20
    while timeOut:
        exit_code = exc_cmd('ping 192.168.13.101')
        if exit_code:
            print exit_code
            time.sleep(1)
        else:
            break
    if timeOut == 0:
        return False
    time.sleep(10)
    km_obj=km()
    kargs={"sip":"192.168.13.100","dip":"192.168.13.101","sum_pair":10,"tx_pair":10,"proto":"TCP","run_time":run_time}
    through = km_obj.run_Ixchariot(**kargs)
    return through

begin("GL-AR150-10c")