#!/usr/bin/python
##### Pulse.py
# Usage: to persist a Pulse VPN connection
# Change the defaults like username and realm in the pulse class for your use
# Begin this program with the following command
# If CTRL-C is initiated, the default action is to disconnect and exit python
#
#example python -c "import Pulse; Pulse.PersisConnect()"
#
#Author Matt Hogan (hoganman@gmail.com)
import os,subprocess,sys,signal,time

class pulse:
    def __init__(self):
        self.script = "/usr/local/pulse/PulseClient.sh"
        self.host = 'secure.colostate.edu'
        self.username = ''
        self.url = 'https://secure.colostate.edu'
        self.realm = '\"CSU eID\"'
    def GetScript(self):
        return self.script
    def GetHost(self):
        return self.host
    def GetUsername(self):
        return self.username
    def GetURL(self):
        return self.url
    def GetRealm(self):
        return self.realm
    def Connect(self):
        if len(self.username) == 0:
            print 'Please put your username in now'
            self.username = str(raw_input('username: '))
        print 'Connecting %s to %s'%(self.GetUsername(),self.GetURL())
        os.system('%s -h %s -u %s -U %s -r %s'%(self.GetScript(),self.GetHost(),self.GetUsername(),self.GetURL(),self.GetRealm()))
        self.CheckConnection()
    def SetUsername(self,newUsername):
        self.username = newUsername
    def SetScript(self,newscript):
        self.script = newscript
    def SetHost(self,newhost):
        self.host = newhost
    def SetURL(self,newurl):
        self.url = newurl
    def SetRealm(self,newrealm):
        self.realm = newrealm
    def CheckConnection(self,verbose=0):
        result = os.popen('%s -S'%(self.GetScript())).read()
        #print 'Is connecting currently?'
        if result.find('Connecting to Server') != -1:
            #print 'YES'
            if verbose:
                print 'Connecting to Server. Please wait 10 seconds'
            numberOfChecks = 0
            while result.find('Connecting to Server') != -1 and numberOfChecks < 10:
                if verbose:
                    print '...'
                numberOfChecks = numberOfChecks + 1
                time.sleep(1)
                result = os.popen('%s -S'%(self.GetScript())).read()
        #print 'Final check for is connected?'
        result = os.popen('%s -S'%(self.GetScript())).read()
        if result.find('connection status : Connected') != -1:
            #print 'CONNECTED!'
            if verbose:
                os.system('%s -S'%(self.GetScript()))
            return 1
        #print 'NOT CONNECTED!'
        return 0
    def Disconnect(self,verbose=1):
        if verbose:
            print 'Disconnecting. Please wait...'
        status = os.popen('%s -K'%(self.GetScript())).read()
        if verbose:
            print status

        #subprocess.Popen([self.GetScript(),'-K'])

client = pulse()
sleepTime = '20'#in seconds
listOfProcesses = []

def Connect(username=''):
    if len(username) == 0:
        print 'Please put your username in now'
        username = str(raw_input('username: '))
    global client
    client.SetUsername(username)
    client.Connect()

def Disconnect():
    global client
    client.Disconnect()
    time.sleep(1)
    connected = Check(0,0)
    if not connected:
        os.system('notify-send -t %s \"Disconnected from %s\"'%(sleepTime,client.GetHost()))
        return
    for times in range(0,5):
        client.Disconnect()
        time.sleep(1)
        connected = Check(0,0)
        if not connected:
            os.system('notify-send -t %s \"Disconnected from %s\"'%(sleepTime,client.GetHost()))
            return
    os.system('notify-send -t %s \"Unable to disconnect from %s\"'%(sleepTime,client.GetHost()))
    

def Check(showDate=1,verbose=0):
    if showDate and verbose:
        os.system('date')
    return bool(client.CheckConnection(verbose))

def PersistConnect(username=''):
    connected = False
    checkedConnection = False
    notifiedConnection = False
    notifiedDisconnection = False
    if len(username) == 0:
        print 'Please put your username in now'
        username = str(raw_input('username: '))
    global client
    proc = subprocess.Popen(['python','-c','import Pulse; Pulse.Connect(\"%s\")'%(username)])
    listOfProcesses.append(proc)
    print 'Attempting a connection...'
    time.sleep(int(sleepTime))
    connected = bool(Check(1,1))
    checkedConnection = True
    while 1:
        if checkedConnection and connected and not notifiedConnection:
            subprocess.Popen(['notify-send','-t',sleepTime,'You have been connected to %s'%(client.GetHost())])
            notifiedConnection = True
            notifiedDisconnection = False
        #if not connected:
        if checkedConnection and not connected:
            proc.communicate() #kill the previous process
            listOfProcesses.remove(proc)
            checkedConnection = False
            if notifiedConnection and not notifiedDisconnection:
                subprocess.Popen(['notify-send','-t',sleepTime,'You have been disconnected from %s'%(client.GetHost())])
                notifiedDisconnection = True
                notifiedConnection = False
            print 'Connection NOT established! Retry...'
            #instantiate a new connection
            proc = subprocess.Popen(['python','-c','import Pulse; Pulse.Connect(\"%s\")'%(username)])
            listOfProcesses.append(proc)
        print 'Next update will occur in %s seconds '%(sleepTime)
        time.sleep(int(sleepTime))
        connected = bool(Check(1,1))
        checkedConnection = True

#CTRL-C action
def signal_handler(signal,frame):
    print '\nExiting...'
    connected = bool(Check(0,0))
    if connected:
        print 'and disconnecting...'
    for process in listOfProcesses:
        process.communicate()
    connected = bool(Check(0,0))
    if connected:
        Disconnect()
    else:
        os.system('notify-send -t %s \"Disconnected from %s\"'%(sleepTime,client.GetHost()))
    sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)
