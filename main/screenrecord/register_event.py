# -*- coding: UTF-8 -*-

from config.configs import Config
from log.log import MLog
from device_info import getDeviceInfo


# 通过配置文件获取密码
def getPwdByConfig(device_name):
    conf = Config("device.ini")
    pwd = conf.getconf(device_name).password
    print "device_name = " + str(device_name) + " and " + "pwd = " + str(pwd)
    return pwd


def click_with_pos(d, class_name, res_id, pos_x, pos_y):
    if d(className=class_name,
         resourceId=res_id).wait.exists(timeout=50000):
        MLog.debug("click_with_pos:" + "x = " + str(pos_x) + "  y =" + str(pos_y))
        d.click(pos_x, pos_y)


def click_with_id(d, class_name, res_id):
    if d(className=class_name,
         resourceId=res_id).wait.exists(timeout=50000):
        d(className=class_name,
          resourceId=res_id).click()


def set_text_with_id(d, class_name, res_id, text_content):
    if d(className=class_name,
         resourceId=res_id).wait.exists(timeout=50000):
        d(className=class_name,
          resourceId=res_id).set_text(text_content)


# 监听输入密码,特殊的点击事件
def inputListener(d, data):
    machineName = getDeviceInfo()
    print 'register_event' + machineName
    if machineName == "OPPOR11Plusk":
        # if d(className="android.widget.EditText",
        #      resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
        #     d(className="android.widget.EditText",
        #       resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
        #         getPwdByConfig(machineName))
        set_text_with_id(d, "android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                         getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1602)
    print 1

    if machineName == "OPPOR9s":
        if d(className="android.widget.EditText",
             resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
            d(className="android.widget.EditText",
              resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(696, 1793)
    print 2

    if machineName == "PACM00":
        if d(className="android.widget.EditText",
             resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
            d(className="android.widget.EditText",
              resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1900)
    print 3

    if machineName == "OPPOA59a":
        if d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").wait.exists(
                timeout=50000):
            d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1900)
    print 4

    if machineName == "OPPOA83":
        MLog.debug(getPwdByConfig(machineName))

        MLog.debug(u"输入密码界面")
        set_text_with_id(d, "android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                         getPwdByConfig(machineName))

        MLog.debug(u"来至电脑端未知来源，只能自己配[222, 1160]")
        click_with_pos(d, "android.widget.LinearLayout", "com.android.packageinstaller:id/bottom_button_layout", 222,
                       1160)

        MLog.debug(u"完成")
        click_with_id(d, "android.widget.TextView", "com.android.packageinstaller:id/done_button")

    print 5

    if machineName == "OPPOA57":
        set_text_with_id(d, "android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                         getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(528, 1218)

    if machineName == "vivoX9":
        MLog.debug("vivoX9")
        click_with_pos(d, "android.widget.Button", "vivo:id/vivo_adb_install_ok_button", 298, 1845)
    print 6


# 注册一些点击事件
def registerEvent(d):
    d.watchers.remove()
    print u"registerEvent" + str(d.watchers)
    conf = Config("default.ini")
    event = conf.getconf("common").click_event
    # print event
    MLog.debug("event = " + event)
    num = event.split(',')
    for index in range(len(num)):
        key = 'event' + str(index)
        item = utf8(num[index])
        MLog.debug("key = " + key + " and " + "item = " + item)
        d.watcher(key).when(text=item).click(text=item)

    MLog.debug(u"列出所有watchers")
    print d.watchers


def getWatchNum():
    conf = Config("default.ini")
    event = conf.getconf("common").click_event
    # print event
    MLog.debug("event = " + event)
    num = event.split(',')
    return len(num)


# 运行点击事件
def runwatch(d, data):
    registerEvent(d)
    num = getWatchNum()
    while True:
        if len(d.watchers) != num:
            registerEvent(d)
        d.watchers.run()


def utf8(file_name):
    return file_name.decode('utf-8')
