import os
import shutil
import subprocess

comp = 'g++'
path = '/home/alex/Prog/ParProg/'
name = 'mm.cpp'
# keys = ['-O3']
keys = ['-O0', '-O1', '-O2', '-O3', '-Ofast']
steps = 10
for_save = '/home/alex/Prog/ParProg/data/'

if not os.path.isdir(for_save):
    os.mkdir(for_save)
for one in keys:
    if os.path.isdir(for_save + name + one):
        shutil.rmtree(for_save + name + one, ignore_errors=True)
    os.mkdir(for_save + name + one)

if os.path.isdir(for_save + name + '_final'):
    shutil.rmtree(for_save + name + '_final', ignore_errors=True)
os.mkdir(for_save + name + '_final')

info_file = open(name + '_final.txt', "w+")

for one in keys:
    cur_name = name + one
    subprocess.run([comp, path + name, one, '-o', cur_name + '.out'])

    res = list()
    for i in range(steps):
        result = subprocess.run('./' + cur_name + '.out', capture_output=True, text=True)
        out_line = result.stdout
        out_line = out_line.split(' ')
        res.append([float(out_line[0]), float(out_line[1])])

    my_file = open(cur_name + '.txt', "w+")
    ap = [0, 0]
    for two in res:
        ap[0] += two[0]
        ap[1] += two[1]
        r = str(two[0]) + ' | ' + str(two[1]) + '\n'
        my_file.write(r)
    my_file.close()
    os.replace(cur_name + '.txt', for_save + cur_name + '/' + cur_name + '.txt')
    os.replace(cur_name + '.out', for_save + cur_name + '/' + cur_name + '.out')
    ap[0] /= steps
    ap[1] /= steps
    r = str(ap[0]) + ' | ' + str(ap[1]) + ' | keys:' + one + '\n'
    info_file.write(r)
os.replace(name + '_final' + '.txt', for_save + name + '_final' + '/' + name + '_final' + '.txt')
info_file.close()

'''
subprocess.run(["g++", "/home/alex/Prog/ParProg/mm.cpp", "-O3"])
result = subprocess.run("./a.out", capture_output=True, text=True)
'''
