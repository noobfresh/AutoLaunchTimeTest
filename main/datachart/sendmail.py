#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
#   说明：Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件
#   调用方式：python sendmail.py 发件人 发件人密码 收件人列表(逗号隔开) 标题 邮件正文文件 邮件类型(html,plain) 邮件附件(可选)
import os
import smtplib
import time
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

from config.configs import Config
from log.fileutil import make_patch, make_log_patch
from screenrecord.device_info import getDeviceInfo

chart_data_path = os.path.dirname(__file__) + os.sep + "dataresult" + os.sep


# 同时支持图片和文本附件
def sendEmail(authInfo, fromAdd, toAdd, subject, content, contentType='plain', patchFileList=None):
    def _format_addr(s):
        name, addr = parseaddr(s)  # 将email地址根据'< '符合分为两部分，如jack <jack@163.com,>会变成(jack,jack@163.com
        return formataddr(( \
            Header(name, 'utf-8').encode(), \
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    strFrom = fromAdd
    strTo = toAdd
    # 多个邮箱地址分割成list
    toAddList = toAdd.split(",")
    server = authInfo.get('server')
    smtpPort = 25
    sslPort = 465
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd):
        print 'incomplete login info, exit now'
        return

    # 设定root信息
    msgRoot = MIMEMultipart('alternative')
    msgRoot['Subject'] = Header(subject, 'utf-8').encode()
    msgRoot['From'] = _format_addr(u'%s<%s>' % (strFrom.split('@')[0], strFrom))
    msgRoot['To'] = strTo

    # 邮件正文内容
    if contentType == 'html':
        msgHtml = MIMEText(content, 'html', 'utf-8')
        msgRoot.attach(msgHtml)
    else:
        msgText = MIMEText(content, 'plain', 'utf-8')
        msgRoot.attach(msgText)

    # 设定附件信息
    if not patchFileList is None:
        for patchFile in patchFileList:
            print u"附件:" + patchFile
            with codecs.open(patchFile, 'rb') as f:
                patchFileName = patchFile.split("/")[-1]
                # 设置附件的MIME和文件名，这里是txt类型:
                msgPatch = MIMEBase('text', 'txt', filename=patchFileName)
                # 加上必要的头信息:
                msgPatch.add_header('Content-Disposition', 'attachment', filename=patchFileName)
                msgPatch.add_header('Content-ID', '<0>')
                msgPatch.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                msgPatch.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(msgPatch)
                # 添加到MIMEMultipart:
                msgRoot.attach(msgPatch)

    try:
        # 发送邮件
        smtp = smtplib.SMTP()
        # smtp.connect(server, smtpPort)
        # ssl加密方式，通信过程加密，邮件数据安全
        smtp = smtplib.SMTP_SSL()
        smtp.connect(server, sslPort)

        # 设定调试级别，依情况而定
        # smtp.set_debuglevel(1)
        smtp.login(user, passwd)
        smtp.sendmail(strFrom, toAddList, msgRoot.as_string())
        smtp.quit()
        print u"邮件发送成功!"
    except Exception, e:
        print u"失败：" + str(e)


def getContent(filename):
    contenttmp = ''
    if os.path.exists(filename):
        contentf = open(filename)
        contenttmp = contentf.read()
        contentf.close()
    return contenttmp


def sendEmailWithDefaultConfig():
    user = u"1146751867@qq.com"
    password = u"lcqctgdcbvklghde"
    to_users = u"191131464@qq.com, pengyangfan@yy.com,weiyi1@yy.com"
    conf = Config("default.ini")
    apk_name = conf.getconf("default").apk_name
    subject = getDeviceInfo() + apk_name + u"启动时间数据分析"
    content = u"数据分析详见附件："
    contentType = u"application/octet-stream"
    try:

        log_file = make_log_patch()

        patchFile = []
        print u"收集邮件附件："
        for files in os.walk(chart_data_path):
            for f in files[2]:
                new_file_path = files[0] + f
                patchFile.append(new_file_path)

        patchFile.append(log_file)

        print patchFile

    except Exception, e:
        print u"收集附件失败：" + e
        patchFile = None

    authInfo = {}
    authInfo['server'] = 'smtp.qq.com'
    authInfo['user'] = user
    authInfo['password'] = password
    fromAdd = user
    toAdd = to_users

    # with codecs.open(contentFile.encode("UTF-8"), 'r', 'utf-8') as fp:
    #         content = fp.read()

    sendEmail(authInfo, fromAdd, toAdd, subject, content, contentType, patchFile)


if __name__ == '__main__':
    sendEmailWithDefaultConfig()
