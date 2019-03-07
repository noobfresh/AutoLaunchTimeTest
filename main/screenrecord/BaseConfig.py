# -*- coding: UTF-8 -*-

from config.configs import Config


class BaseConfig(object):

    def __init__(self):
        self.conf = Config("default.ini")
        self.param = None
        print "BaseConfig init"

    def setParams(self, params):
        self.param = params

    def getParms(self):
        return self.param

    def getFirstStartTime(self):
        if self.param:
            return self.param.first_start_times
        else:
            self.firstTime = self.conf.getconf("default").first_start
            return self.firstTime

    def getNormalStartTime(self):
        if self.param:
            return self.param.normal_start_times
        else:
            self.normalTime = self.conf.getconf("default").normal_start
            return self.normalTime

    def getEnterLiveRoom(self):
        if self.param:
            return self.param.enter_liveroom_times
        else:
            self.enterLiveRomm = self.conf.getconf("default").enter_liveroom
            return self.enterLiveRomm

    def getApkName(self):
        self.apkName = self.conf.getconf("default").apk_name
        return self.apkName

    def getAppName(self):
        if self.param:
            return self.param.app_name
        else:
            self.appName = self.conf.getconf("default").app_name
            return self.appName

    def getPackage(self):
        if self.param:
            return self.param.package_name
        else:
            self.packageName = self.conf.getconf("default").package
            return self.packageName

    def getFeaturePath(self):
        self.featurePath = self.conf.getconf("default").feature_path
        return self.featurePath

    def getMethod(self):
        return self.param.install_method

