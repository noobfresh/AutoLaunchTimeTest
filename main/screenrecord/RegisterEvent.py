# -*- coding: UTF-8 -*-

from config.configs import Config
from log.log import MLog

# 通过配置文件获取密码
from screenrecord.BaseConfig import BaseConfig
from screenrecord.DeviceInfo import DeviceInfo


class RegisterEvent(BaseConfig):

    def __init__(self, sernum):
        super(RegisterEvent, self).__init__()
        self.serNum = sernum
        self.device = DeviceInfo(sernum)
        self.machineName = self.device.getDeviceInfo()

    def getPwdByConfig(self, device_name):
        conf = Config("device.ini")
        pwd = conf.getconf(device_name).password
        return pwd

    def click_with_pos(self, d, class_name, res_id, pos_x, pos_y):
        if d(className=class_name,
             resourceId=res_id).exists(timeout=50):
            MLog.debug("click_with_pos:" + "x = " + str(pos_x) + "  y =" + str(pos_y))
            d.click(pos_x, pos_y)

    def click_with_id(self, d, class_name, res_id):
        if d(className=class_name,
             resourceId=res_id).exists(timeout=50):
            d(className=class_name,
              resourceId=res_id).click()

    def set_text_with_id(self, d, class_name, res_id, text_content):
        if d(className=class_name,
             resourceId=res_id).exists(timeout=70):
            d(className=class_name,
              resourceId=res_id).set_text(text_content)

    # 监听输入密码,特殊的点击事件
    def inputListener(self, d, data, serialNum):

        if self.machineName == "OPPOR11Plusk":
            self.set_text_with_id(d, "android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                                  self.getPwdByConfig(self.machineName))
            if d(className="android.widget.LinearLayout",
                 resourceId="com.android.packageinstaller:id/bottom_button_layout").exists(timeout=50):
                d.click(458, 1602)

        if self.machineName == "OPPOR9s":
            if d(className="android.widget.EditText",
                 resourceId="com.coloros.safecenter:id/et_login_passwd_edit").exists(timeout=50):
                d(className="android.widget.EditText",
                  resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                    self.getPwdByConfig(self.machineName))
            if d(className="android.widget.LinearLayout",
                 resourceId="com.android.packageinstaller:id/bottom_button_layout").exists(timeout=50):
                d.click(696, 1793)

        if self.machineName == "PACM00":
            if d(className="android.widget.EditText",
                 resourceId="com.coloros.safecenter:id/et_login_passwd_edit").exists(timeout=70):
                print 'PACM00 1'
                d(className="android.widget.EditText",
                  resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                    self.getPwdByConfig(self.machineName))
                print 'PACM00 2'
            if d(className="android.widget.LinearLayout",
                 resourceId="com.android.packageinstaller:id/bottom_button_layout").exists(timeout=70):
                print 'PACM00 3'
                d.click(458, 1900)

        if self.machineName == "OPPOA59a":
            if d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").exists(
                    timeout=50):
                d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").set_text(
                    self.getPwdByConfig(self.machineName))
            if d(className="android.widget.LinearLayout",
                 resourceId="com.android.packageinstaller:id/bottom_button_layout").exists(timeout=50):
                d.click(458, 1900)

        if self.machineName == "OPPOA83":
            MLog.debug(u"等待OPPOA83输入密码界面")
            self.set_text_with_id(d, "android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                                  self.getPwdByConfig(self.machineName))
            MLog.debug(u"输入密码完成")
            MLog.debug(u"来至电脑端未知来源，只能自己配[222, 1160]")
            self.click_with_pos(d, "android.widget.LinearLayout",
                                "com.android.packageinstaller:id/bottom_button_layout",
                                222,
                                1160)
            MLog.debug(u"点击完成")
            # click_with_id(d, "android.widget.TextView", "com.android.packageinstaller:id/done_button")

        if self.machineName == "OPPOA57":
            self.set_text_with_id(d, "android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                                  self.getPwdByConfig(self.machineName))
            if d(className="android.widget.LinearLayout",
                 resourceId="com.android.packageinstaller:id/bottom_button_layout").exists(timeout=50):
                d.click(528, 1218)
        if self.machineName == "vivoX9":
            self.click_with_pos(d, "android.widget.Button", "vivo:id/vivo_adb_install_ok_button", 298, 1845)

    # 注册一些点击事件
    def registerEvent(self, d):
        d.watchers.remove()
        conf = Config("default.ini")
        event = conf.getconf("common").click_event
        MLog.debug(u"从配置文件中读取到的注册事件: event = " + event)
        num = event.split(',')
        d.watchers.remove()
        d.watchers.watched = False
        for index in range(len(num)):
            key = 'event' + str(index)
            item = num[index]
            MLog.debug("key = " + key + " and " + "item = " + item)
            d.watcher(key).when(text=item).click(text=item)

        d.watchers.watched = True
        d.watchers.run()
        MLog.debug(u"列出所有注册上的watchers")
        print d.watchers

    def getWatchNum(self):
        conf = Config("default.ini")
        event = conf.getconf("common").click_event
        num = event.split(',')
        return len(num)

    # 运行点击事件
    def runwatch(self, d, data):
        self.registerEvent(d)
        num = self.getWatchNum()
        while True:
            if len(d.watchers) != num:
                self.registerEvent(d)
