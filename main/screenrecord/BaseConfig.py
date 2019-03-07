# -*- coding: UTF-8 -*-

from config.configs import Config


class BaseConfig(object):

    def __init__(self):
        self.conf = Config("default.ini")
        self.param = None
        print "BaseConfig init"

    def setParams(self, params):
        self.param = params

    # params.sdk_path = self.sdkPath
    # params.video_path = self.videoPath
    # params.install_method = self.installMethos
    # params.first_start_times = self.firstStartTime
    # params.normal_start_times = self.normaStartTime
    # params.enter_liveroom_times = self.enterLiveRoonTime
    # params.app_name = self.appName
    # params.package_name = self.packageName
    # params.app_path = self.appPath
    # params.features = self.features

    def getParms(self):
        return self.param

    def getFirstStartTime(self):
        return self.param.first_start_times
        # self.firstTime = self.conf.getconf("default").first_start
        # return self.firstTime

    def getNormalStartTime(self):
        return self.param.normal_start_times
        # self.normalTime = self.conf.getconf("default").normal_start
        # return self.normalTime

    def getEnterLiveRoom(self):
        return self.param.enter_liveroom_times
        # self.enterLiveRomm = self.conf.getconf("default").enter_liveroom
        # return self.enterLiveRomm

    def getApkName(self):
        self.apkName = self.conf.getconf("default").apk_name
        return self.apkName

    def getAppName(self):
        return self.param.app_name
        # self.appName = self.conf.getconf("default").app_name
        # return self.appName

    def getPackage(self):
        return self.param.package_name
        # self.packageName = self.conf.getconf("default").package
        # return self.packageName

    def getFeaturePath(self):
        self.featurePath = self.conf.getconf("default").feature_path
        return self.featurePath

    def getMethod(self):
        return self.param.install_method
