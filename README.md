
# Rev-Shell 🖥️

This tool generates a reverse shell for a specific network interface, choosing among different subsystems:
```
usage: rev_shell.py [-h] [-p PORT] [-H] [-S] [-s SUBSYSTEM]

Generates a reverse shell command for the specified subsystem

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Specifies the port to open the connection in        
  -H, --hexadecimal     Encode the ip in hexadecimal
  -S, --list-subsystems
                        List available subsystems
  -s SUBSYSTEM, --subsystem SUBSYSTEM
                        What subsystem the reverse shell is going to execute

```

