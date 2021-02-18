import os
import time
import sys
import smtplib
import pytz
from datetime import datetime
import os
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Constants(object):
    def __init__(self):
        super(Constants, self).__init__()
        self._repository = 'git clone git@bitbucket.org:ajayranwaembibe/fiber_checklist.git'
        self._directory = 'fiber_checklist/'
        self._command = 'python3 fiber_flow.py "https://fiberdemoms.embibe.com" "8th CBSE" "CBSE"'
        self._filename = ''
        self._from_address = 'automation-ui@embibe.com'
        self._to_address = ['tanishq.rohela@embibe.com']
        self._email_subject = "Automated Regression Suite for All Goals & Exams - Fiberdemo Environment"
        self._email_body = "<html><body><p><center><font color='red'><i>*****This is an auto-generated email. Please do not reply.*****</i></font></center></p><p>Hi All,<br> PFA the output files for "+self._email_subject+"</p><p>{}</p</p>"
        self._email_password = "Embibe@333"

    @property
    def repository(self):
        return self._repository

    @property
    def filename(self):
        return self._filename

    @property
    def directory(self):
        return self._directory

    @property
    def command(self):
        return self._command

    @property
    def to_address(self):
        return self._to_address

    @property
    def from_address(self):
        return self._from_address

    @property
    def email_body(self):
        return self._email_body

    @property
    def email_subject(self):
        return self._email_subject

    @property
    def email_password(self):
        return self._email_password


class Email(object):
    def __init__(self):
        super(Email, self).__init__()
        self._to_address = None
        self._directory = None

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, directory):
        self._directory = directory

    @property
    def to_address(self):
        return self._to_address

    @to_address.setter
    def to_address(self, email):
        self._to_address = email

    def checkSize(self, r):
        size = 0
        try:
            for file in r:
                size += os.stat(file).st_size
            print (size)
        except Exception as e:
            print (e)
            return False
        if size > 25000000:
            return False
        return True

    def sendemail(self, from_address, email_password, email_subject, email_body, attachment_filename):
        to_address = self._to_address

        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = ", ".join(to_address)
        msg['Subject'] = email_subject

        if self.checkSize(attachment_filename):
            for file in attachment_filename:
                attachment = None
                try:
                    attachment = open(file, "rb")
                except Exception as e:
                    print(e)
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % file)
                msg.attach(p)
        else:
            print('size exceeded 25MB.')

        msg.attach(MIMEText(email_body, 'html'))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_address, email_password)
        text = msg.as_string()
        s.sendmail(from_address, to_address, text)
        s.quit()
        print("Email sent to " + str(to_address))


class Server(object):
    def __init__(self):
        super(Server, self).__init__()

    def run(self, command):
        os.system(command)


class Project(object):
    def __init__(self):
        super(Project, self).__init__()
        self._server = Server()
        self._constants = Constants()
        self._email = Email()

    @property
    def server(self):
        return self._server

    @property
    def constants(self):
        return self._constants

    @property
    def email(self):
        return self._email


class Main(object):
    def __init__(self):
        super(Main, self).__init__()
        self._project = Project()

    def readFile(self, file):
        data = None
        with open(file, 'r') as f:
            data = f.read()
        return data

    def getDescription(self, dir):
        try:
            data = open(dir+'description.html','r').read()
            return data
        except Exception as e:
            print(e)
            return None

    def runServer(self):
        project = self._project
        project.server.run('cd ' + project.constants.directory + ' && ' + project.constants.command)
        time.sleep(5)
        project.email.to_address = project.constants.to_address
        e_from = project.constants.from_address
        e_pass = project.constants.email_password
        UTC = pytz.utc
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        e_sub = project.constants.email_subject  # .format(str(datetime_ist).split('.')[0])
        e_body = project.constants.email_body.format(self.getDescription(project.constants.directory))
        e_file = glob.glob(project.constants.directory+'Results/*.csv')
        print(e_file)
        project.email.directory = project.constants.directory
        time.sleep(5)
        project.email.sendemail(e_from, e_pass, e_sub, e_body, e_file)

    def schedule(self): #, sch):
        project = self._project
        while True:
            try:
                # now = datetime.now()
                # if now.hour == int(sch.split(':')[0]) and now.minute == int(sch.split(':')[1]):
                print('Starting process...')
                project.server.run(project.constants.repository)
                time.sleep(3)
                self.runServer()
                time.sleep(3)
                project.server.run('sudo rm -r ' + project.constants.directory)
                print('Exiting process...')
                time.sleep(43200)
            except Exception as e:
                print(e)
                time.sleep(100)


if __name__ == '__main__':
    main = Main()
    main.schedule() #sys.argv[1])
