import subprocess

programs_list = list()


programs_list.append(subprocess.Popen())

for i in programs_list:
    while i.poll() is None:
        pass
