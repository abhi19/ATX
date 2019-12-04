import socket
import time
import ftplib
import sys
import os
import getopt

#ip = "192.168.144.141"
from pip._vendor.distlib.compat import raw_input

port = [21,25,80,445,99]
open_ports = []
retry = 1
delay = 1
timeout = 3

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                open_ports.append(port)
                return True

        except:
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup

def anoncheck(ip):
	try:
		ftp=ftplib.FTP(ip)
		ftp.login('anonymous','anonymous')
		print('\n[+] '+str(ip)+' : FTP Anonymous login Successful')
		ftp.quit()
		return True
	except Exception as e:
		print("\n[-] Failed login.\n"+str(e))
		return False

def http(ip):
    print('\nRunning Dirb on the target')
    print('\n-----------------DIRB v2.22----------------\n By The Dark Raver')
    os.system('dirb http://'+ip+' >> '+ip+'.txt')
    os.system('cat '+ip+'.txt | grep CODE:200')

def smb(ip):
    print('\nChecking SMB')
    os.system('smbmap -H '+ip+' | tee '+ip+'_smb.txt')



if __name__ == '__main__':
    print('\n------------Welcome to ATX---------------')
    ip = raw_input('\nEnter target IP adddress: ')
    print('\nChecking for open ports:')
    for num in port:
        if checkHost(ip, num):
            print(repr(num) + " is UP")
        else:
            print(repr(num) + " is Down")
    print('\nOpen Ports:')
    print(open_ports)

    print('\nChecking for FTP login:')
    anoncheck(ip)
    http(ip)
    smb(ip)