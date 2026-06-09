import datetime
import os
import platform

import psutil

from tools import colors as col


def mutfetch():
    fetch_name = os.getlogin()
    cpu_load = psutil.cpu_percent(interval=1)
    hostname = platform.node()
    shell_name = "MutSH 0.0.1"
    kernel = "Mutruntime 0.1"
    os_name = "MutOS 0.1"
    arch = platform.machine()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(
        psutil.boot_time()
    )
    d = psutil.disk_usage("/")
    disk = f"{d.used / 1024**3:.1f} GB >> {d.total / 1024**3:.1f} GB ({d.percent}%)"
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    mutfetch = (
        col.MAGENTA
        + f"""
                       ██████               USER -> {fetch_name}
                     ███   ██               HOST -> {hostname}
                   ███   █████              OS -> {os_name}
                   █    ██   ███            KERNEL -> {kernel}
                 ████  ██████  █████        SHELL -> {shell_name}
             ████████████   ████   ██       MACHINE -> {arch}
           ███ ███████  ████     ███        CPU -> {cpu_load}%
         ██   ██     █████████████          UPTIME -> {uptime}
         █   █████   ██  █                  TIME -> {time_now}
    ███████  █    ████   █                  DISK -> {disk}
  ███     ███████████   ██
 ██  ████████        ████
██  ██  ██  ██████████
█████     ███  █
    ████  ███  █
       ███    ██
       ██   ███
       ██████
    """
        + col.RESET
    )

    print(mutfetch)


mutfetch()
