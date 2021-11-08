import os
import shutil
import subprocess

import for_input

conf_name = 'conf.txt'

conf_file = open(conf_name, "r")
confData = conf_file.read()
conf_file.close()
confData = confData.split('\n')
confDict = dict()
for one in confData:
    one = one.split(':')
    if one[0] == 'keys' or one[0] == 'data_sets':
        one[1] = one[1].split(',')
    confDict.update({one[0]: one[1]})
print(confDict)
dataSet = for_input.cur_set(confDict.setdefault('data_sets'))
if os.path.isdir(confDict.setdefault('save_path')):
    shutil.rmtree(confDict.setdefault('save_path'), ignore_errors=True)
os.mkdir(confDict.setdefault('save_path'))

info_file = open(confDict.setdefault('save_path') + 'final.txt', "w+")
for one in confDict.setdefault('keys'):
    for two in dataSet:
        subprocess.run([confDict.setdefault('compile'), confDict.setdefault('program_path'), one, '-o', 'now.out'])
        res = list()
        for i in range(int(confDict.setdefault('tres'))):
            programsList = list()
            for j in range(int(confDict.setdefault('in_time'))):
                if type(two) is int:
                    programsList.append(subprocess.run(['./now.out', str(two)], capture_output=True, text=True))
                else:
                    programsList.append(subprocess.run(['./now.out', str(two[0]), str(two[1])],
                                                       capture_output=True, text=True))
                for three in programsList:
                    out_line = three.stdout
                    out_line = out_line.split(' ')
                    res.append([float(out_line[0]), float(out_line[1])])

        ap = [0, 0]
        for tr in res:
            ap[0] += tr[0]
            ap[1] += tr[1]
        ap[0] /= int(confDict.setdefault('tres'))*int(confDict.setdefault('in_time'))
        ap[1] /= int(confDict.setdefault('tres'))*int(confDict.setdefault('in_time'))
        r = str(ap[0]) + ' | ' + str(ap[1]) + ' | keys:' + one + ' | in time ' + confDict.setdefault('in_time')
        if type(two) is int:
            r += ' | input: ' + str(two)
        else:
            r += ' | input: ' + 'n' + str(two[0]) + ' dn' + str(two[1])
        r += '\n'
        info_file.write(r)

'''


if os.path.isdir(for_save + name + '_final'):
    shutil.rmtree(for_save + name + '_final', ignore_errors=True)
os.mkdir(for_save + name + '_final')

info_file = open(name + '_final.txt', "w+")

for one in keys:
    cur_key_name = name + one
    for two in input_data:
        if type(two) is int:
            cur_name = name + one + 'n' + str(two)
        else:
            cur_name = name + one + 'n' + str(two[0]) + 'dn' + str(two[1])

        subprocess.run([comp, path + name, one, '-o', cur_name + '.out'])

        res = list()
        for i in range(steps):
            result = None
            if type(two) is int:
                result = subprocess.run(['./' + cur_name + '.out', str(two)], capture_output=True, text=True)
            else:
                result = subprocess.run(['./' + cur_name + '.out', str(two[0]), str(two[1])],
                                        capture_output=True, text=True)
            out_line = result.stdout
            out_line = out_line.split(' ')
            res.append([float(out_line[0]), float(out_line[1])])

        my_file = open(cur_name + '.txt', "w+")
        ap = [0, 0]
        for tr in res:
            ap[0] += tr[0]
            ap[1] += tr[1]
            r = str(tr[0]) + ' | ' + str(tr[1]) + '\n'
            my_file.write(r)
        my_file.close()
        name_add = ''
        if type(two) is int:
            name_add = 'n' + str(two)
        else:
            name_add = 'n' + str(two[0]) + 'dn' + str(two[1])
        os.replace(cur_name + '.txt', for_save + cur_key_name + '/' + name_add + '/' + cur_name + '.txt')
        os.replace(cur_name + '.out', for_save + cur_key_name + '/' + name_add + '/' + cur_name + '.out')
        ap[0] /= steps
        ap[1] /= steps
        r = str(ap[0]) + ' | ' + str(ap[1]) + ' | keys:' + one
        if type(two) is int:
            r += ' | input: ' + str(two)
        else:
            r += ' | input: ' + 'n' + str(two[0]) + ' dn' + str(two[1])
        r += '\n'
        info_file.write(r)
os.replace(name + '_final' + '.txt', for_save + name + '_final' + '/' + name + '_final' + '.txt')
info_file.close()


subprocess.run(["g++", "/home/alex/Prog/ParProg/mm.cpp", "-O3"])
result = subprocess.run("./a.out", capture_output=True, text=True)
'''
