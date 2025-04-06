from app.log_inspector.abc_inspector import AbstractLogInspector
from app.models.log import Log


class StandartLibraryInspector(AbstractLogInspector):
    expertises = [
        ["find", "-exec"],
        ["vim", "-c", "!sh"],
        ["nmap", "--interactive"],
        ["awk", "BEGIN", '{system("/bin/sh")}'],
        ["less", "/etc/passwd", "!/bin/sh"],
        ["bash", "-i", ">&", "/dev/tcp/"],
        ["python", "-c", "import socket,subprocess,os"],
        ["python", "-c", "import", "socket"],
        ["python", "-c", "pty.spawn"],
        ["python", "-c", "eval("],
        ["perl", "-e", "use Socket"],
        ["php", "-r", "$sock=fsockopen"],
        ["ruby", "-rsocket", "-e"],
        ["nc", "-e", "/bin/sh"],
        ["socat", "TCP:", "EXEC:bash"],
        ["sudo", "-u#-1"],  # CVE-2019-14287
        ["pkexec", "--user", "root"],
        ["docker", "run", "-v", "/:/mnt", "alpine"],
        ["ansible-playbook", "--become-user=root"],
        ["chroot", "/", "bash"],
        ["cp", "/bin/sh"],
        ["mv", "/tmp/exploit", "/usr/bin"],
        ["ln", "-s", "/etc/shadow"],
        ["dd", "if=/dev/zero", "of=/etc/passwd"],
        ["env", "LD_PRELOAD"],
        ["export", "PATH=/tmp:$PATH"],
        ["echo", "* * * * *", "root", "/tmp/exploit"],
        ["crontab", "-l", ">/tmp/cron"],
        ["tcpdump", "-i", "any", "-w"],
        ["wireshark", "-k"],
        ["nmap", "-sS", "-sV", "-p-"],
        ["ncat", "--udp", "-e", "/bin/bash"],
        ["sudo", "nc"],
        ["grep", "-r", "password", "/etc"],
        ["strings", "/usr/bin/login"],
        ["unshadow", "/etc/passwd", "/etc/shadow"],
        ["gdb", "-p"],
        ["strace", "-f", "-e"],
        ["apt-get", "install", "--allow-unauthenticated"],
        ["yum", "--downloadonly", "--downloaddir=/tmp"],
        ["python", "-m", "http.server", "8000"],
        ["php", "-S", "0.0.0.0:8080"],
        ["nsenter", "--target", "1", "--mount"],
        ["crictl", "exec", "-it"],
    ]
    suspicious_patterns = [
        ">/dev/null 2>&1 &",
        "| bash",
        "$(",
        "`",
        "|| true",
        "wget http://",
        "curl -o- http://",
        "base64 -d",
        "openssl enc -d",
    ]

    def check_for_dangerous(self, log: Log) -> bool:
        cmd_lower = log.cmd.lower()
        for expertise in self.expertises:
            if all(marker.lower() in cmd_lower for marker in expertise):
                return True
        return any(pattern in cmd_lower for pattern in self.suspicious_patterns)
