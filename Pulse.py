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
    def SetHost(self):
        self.host = newhost
    def SetUsername(self):
        self.username = newusername
    def SetURL(self):
        self.url = newurl
    def SetRealm(self):
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
            self.connected=True
            return 1
        #print 'NOT CONNECTED!'
        self.connected=False
        return 0
    def Disconnect(self):
        print 'Disconnecting...'
        os.system('%s -K'%(self.GetScript()))
        self.connected=False

client = pulse()

def Connect(username=''):
    global client
    if len(username) != 0:
        client.SetUsername(username)
    client.Connect()

def Disconnect():
    client.Disconnect()

def Check(showDate=1,verbose=0):
    if showDate and verbose:
        os.system('date')
    return bool(client.CheckConnection(verbose))

def PersistConnect(username=''):
    sleepTime = '20'#in seconds
    connected = False
    global client
    proc = subprocess.Popen(['python','-c','import Pulse; Pulse.Connect(\"%s\")'%(username)])#,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print 'Attempting a connection...'
    time.sleep(int(sleepTime))
    connected = bool(Check(1,1))
    while 1:
        if not connected:
            print 'Connection NOT established! Retry...'
            proc.communicate() #end the previous process
            proc = subprocess.Popen(['python','-c','import Pulse; Pulse.Connect(\"%s\")'%(username)])#,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print 'Next update will occur in %s seconds '%(sleepTime)
        time.sleep(int(sleepTime))
        connected = bool(Check(1,1))

#CTRL-C action
def signal_handler(signal,frame):
    print 'Exiting and disconnecting...'
    Disconnect()
    time.sleep(5)
    sys.exit(1)
signal.signal(signal.SIGINT, signal_handler)
