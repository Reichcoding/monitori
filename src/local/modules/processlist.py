import subprocess

def get_programs():
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    lines = []
    for line in proc.stdout:
        if not line.decode().isspace():
            lines.append(line.decode().rstrip())

    lines2 = []
    for i in lines[2:]:
        lines2.append(i)

    return lines2