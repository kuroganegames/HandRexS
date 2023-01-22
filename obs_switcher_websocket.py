#coding:utf-8

import subprocess
import tkinter as tk
from tkinter import ttk
import threading
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
from configparser import ConfigParser
import obsws_python as obs


# obs-cliを動かすためのクラス
class obsclipy:
    # def __init__(self, host = "192.168.56.1", port="4444", password="password"):
    def __init__(self):
        global config_ini, cl
        # self.i_host = host
        # self.i_port = port
        # self.s_pass = password
        
        # self.cl = obs.ReqClient(host=self.i_host, port=self.i_port, password=self.s_pass)
        
    def record_start(self):
        print("start record!")
        # return subprocess.run(["obs-cli", "recording", "start", "--password", self.s_pass, "--port", self.i_port])
        cl.start_record()
    def record_end(self):
        print("end record")
        # return subprocess.run(["obs-cli", "recording", "stop", "--password", self.s_pass, "--port", self.i_port])
        cl.stop_record()
    def scene_change(self,s_scene):
        print(f"scene changer {s_scene}")
        # return subprocess.run(["obs-cli", "scene", "current",s_scene, "--password", self.s_pass, "--port", self.i_port])
        cl.set_current_program_scene(s_scene)




#軽いので一旦更新機能は未実装
class OBSSwitcher:
    def __init__(self):
        global config_ini, cl
        
        self.root = tk.Tk()
        self.root.geometry('350x250')

        self.style = ttk.Style()
        self.style.theme_use("winnative")
        self.style.configure("office.TCombobox", selectbackground="blue")

        self.list_combo = []
        self.list_combo_val = []
        self.list_label = []
        
        # cp = subprocess.run(["obs-cli", "scene", "list", "--password", "72WNjq6N", "--port", "4444"],
                     # encoding='utf-8', 
                     # stdout=subprocess.PIPE)
        # self.list_scene = cp.stdout.splitlines()

        l_scene = cl.get_scene_list()
        self.list_scene = [i_scene['sceneName'] for i_scene in l_scene.scenes]

        self.module = ('tkinter', 'math', 'os', 'pyinstaller', 'pathlib', 'sys')

        self.v = tk.StringVar()
        
        self.set_gui()

    def set_gui(self):
        l_scene_all = tk.Label(self.root,  text="シーン一覧")
        l_scene_all.grid(row=0, column=0)
        l_scene_reg = tk.Label(self.root,  text="シーン登録")
        l_scene_reg.grid(row=0, column=1)

        var2 = tk.StringVar()
        var2.set(self.list_scene)
        lb = tk.Listbox(self.root, listvariable=var2)
        lb.grid(row=1, column=0, rowspan=9)

        self.set_combo(c_row=1)
        self.set_combo(c_row=2)
        self.set_combo(c_row=3)
        self.set_combo(c_row=4)
        self.set_combo(c_row=5)
        self.set_combo(c_row=6)
        self.set_combo(c_row=7)
        self.set_combo(c_row=8)
        # self.set_combo(c_row=9)
    
        
    def set_combo(self, c_row=1, c_column=1,init_com = ""):
        
        self.list_label.append(tk.Label(self.root,  text=f"scene{c_row}"))
        self.list_label[len(self.list_label)-1].grid(row=c_row, column=c_column)

        self.list_combo_val.append(tk.StringVar())
        self.list_combo.append(ttk.Combobox(self.root, textvariable= self.list_combo_val[len(self.list_combo_val)-1], values=self.list_scene, style="office.TCombobox"))
        self.list_combo[len(self.list_combo)-1].bind("<<ComboboxSelected>>",self.combo_selected)
        self.list_combo[len(self.list_combo)-1].grid(row=c_row, column=c_column+1)
        


    def combo_selected(self, event):
    
        l_scene_selected = [i.get() for i in self.list_combo_val]
        print(l_scene_selected)
        
        for i_scene in range(8):
            config_ini['SCENES'][f'SCENE{i_scene}'] = l_scene_selected[i_scene]
        
        with open("setting.ini", "w", encoding="utf-8") as configfile:
            # 指定したconfigファイルを書き込み
            config_ini.write(configfile)

    def run(self):
        self.root.mainloop()



def com_receive():
    #osc通信の監視、GUI変数の監視、シーン切り替え機能をここに導入
    
    #設定ファイル「setting.ini」を読み込みます。
    global config_ini, cl

    # i_host = config_ini['OBS']['HOST']
    # i_port = config_ini['OBS']['PORT']
    # s_pass = config_ini['OBS']['PASS']
    
    IP = config_ini['VRCosc']['IP']
    PORT = int(config_ini['VRCosc']['PORT'])
    
    # SCENES = [config_ini['SCENES'][f'SCENE{i_scene}'] for i in range(8)]
    
    for i_scene in range(8):
        osw.list_combo_val[i_scene].set(config_ini['SCENES'][f'SCENE{i_scene}']) 
    
    
    ocp = obsclipy()

    # oscで受信した時の関数です
    def obs_recoreder(unused_addr, isRecord):
        
        print(f"recieved {isRecord}")
        if isRecord:
            ocp.record_start()
        else:
            ocp.record_end()

    # oscで受信した時のシーン切り替え用関数群です
    def obs_switcher1(unused_addr, isSwitch1):
        print(f"recieved {isSwitch1}")
        if isSwitch1:
            print(osw.list_combo_val[0].get())
            ocp.scene_change(osw.list_combo_val[0].get())
    def obs_switcher2(unused_addr, isSwitch2):
        print(f"recieved {isSwitch2}")
        if isSwitch2:
            ocp.scene_change(osw.list_combo_val[1].get())
    def obs_switcher3(unused_addr, isSwitch3):
        print(f"recieved {isSwitch3}")
        if isSwitch3:
            ocp.scene_change(osw.list_combo_val[2].get())
    def obs_switcher4(unused_addr, isSwitch4):
        print(f"recieved {isSwitch4}")
        if isSwitch4:
            ocp.scene_change(osw.list_combo_val[3].get())
    def obs_switcher5(unused_addr, isSwitch5):
        print(f"recieved {isSwitch5}")
        if isSwitch5:
            ocp.scene_change(osw.list_combo_val[4].get())
    def obs_switcher6(unused_addr, isSwitch6):
        print(f"recieved {isSwitch6}")
        if isSwitch6:
            ocp.scene_change(osw.list_combo_val[5].get())
    def obs_switcher7(unused_addr, isSwitch7):
        print(f"recieved {isSwitch7}")
        if isSwitch7:
            ocp.scene_change(osw.list_combo_val[6].get())
    def obs_switcher8(unused_addr, isSwitch8):
        print(f"recieved {isSwitch8}")
        if isSwitch8:
            ocp.scene_change(osw.list_combo_val[7].get())
    # def obs_switcher9(unused_addr, isSwitch9):
        # print(f"recieved {isSwitch9}")
        # if isSwitch9:
            # ocp.scene_change(osw.list_combo_val[8].get())





    #osc通信の設定
    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/recording", obs_recoreder)
    dispatcher.map("/avatar/parameters/scene1", obs_switcher1)
    dispatcher.map("/avatar/parameters/scene2", obs_switcher2)
    dispatcher.map("/avatar/parameters/scene3", obs_switcher3)
    dispatcher.map("/avatar/parameters/scene4", obs_switcher4)
    dispatcher.map("/avatar/parameters/scene5", obs_switcher5)
    dispatcher.map("/avatar/parameters/scene6", obs_switcher6)
    dispatcher.map("/avatar/parameters/scene7", obs_switcher7)
    dispatcher.map("/avatar/parameters/scene8", obs_switcher8)
    # dispatcher.map("/avatar/parameters/scene9", obs_switcher9)

    #受信サーバーを動かす
    server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)
    print(f"Serving on {server.server_address}")
    server.serve_forever()
    

def com_start():
    th=threading.Thread(target=com_receive)
    th.start()


if __name__ == "__main__":

    config_ini = ConfigParser()
    config_ini.read("setting.ini", encoding="utf-8")
    
    s_host = config_ini['OBS']['HOST']
    i_port = config_ini['OBS']['PORT']
    s_pass = config_ini['OBS']['PASS']
    cl = obs.ReqClient(host=s_host, port=i_port, password=s_pass)
    
    osw = OBSSwitcher()
    com_start()
    osw.run()
