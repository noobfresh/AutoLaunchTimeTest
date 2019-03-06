# -*- coding: UTF-8 -*-

from config.configs import Config


class BaseConfig(object):

    def __init__(self):
        self.conf = Config("default.ini")
        print "BaseConfig init"

    def getFirstStartTime(self):
        self.firstTime = self.conf.getconf("default").first_start
        return self.firstTime

    def getNormalStartTime(self):
        self.normalTime = self.conf.getconf("default").normal_start
        return self.normalTime

    def getEnterLiveRoom(self):
        self.enterLiveRomm = self.conf.getconf("default").enter_liveroom
        return self.enterLiveRomm

    def getApkName(self):
        self.apkName = self.conf.getconf("default").apk_name
        return self.apkName

    def getAppName(self):
        self.appName = self.conf.getconf("default").app_name
        return self.appName

    def getPackage(self):
        self.packageName = self.conf.getconf("default").package
        return self.packageName

    def getFeaturePath(self):
        self.featurePath = self.conf.getconf("default").feature_path
        return self.featurePath
