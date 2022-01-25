import itertools
import subprocess
import timeit
import other.GlobalFunction as GFunction
from typing import Type


class ProgramLauncherOLD:
    _data = dict()

    def run(self, compiles: list, prog_path: str, keys: dict, data: list, compiler: str, name: str,
            trails: int, at_same_time: int):

        data = GFunction.to_string(data)

        commands_run = list(itertools.product(*data))

        for one in compiles:
            res = list()
            for two in keys.get(one):

                key = ''
                for key_one in two:
                    key += key_one + ' '
                key = key[:len(key) - 1]
                res = list()

                # print(one + ' ' + prog_path + ' '+key+' ' + compiler + ' ' + name)

                subprocess.run([one, prog_path, key, compiler, name])

                for pars in commands_run:

                    one_command = 'subprocess.Popen([\'./\' +\'' + name + '\','
                    for one_par in pars:
                        one_command += '\'' + str(one_par) + '\','
                    one_command = one_command[:len(one_command) - 1]
                    one_command += '])'
                    print(one_command)

                    all_command = 'programs_list = list()\n'
                    for i in range(at_same_time):
                        all_command += 'programs_list.append(' + one_command + ')\n'
                    all_command += 'for i in programs_list:\n\twhile i.poll() is None:\n\t\tpass'
                    print(all_command)

                    pres = list()
                    for i in range(trails):
                        time = timeit.timeit(setup='import subprocess', stmt=all_command, number=1)
                        pres.append([two, pars, time])
                    res.append(pres)

                    '''pars = list()
                    for i in parsi:
                        pars.append(i)

                    one_command = 'subprocess.run([\'./\' +\'' + name + '\','
                    for one_par in pars:
                        one_command += '\''+str(one_par) + '\','
                    one_command = one_command[:len(one_command) - 1]
                    one_command += '])'
                    print(one_command)

                    print(timeit.timeit(setup='import subprocess', stmt=one_command+'\n'+one_command, number=trails))

                    for one_try in range(trails):
                        programs_list = list()
                        for same in range(at_same_time):
                            programs_list.append(subprocess.run(['./' + name] + pars))
                            print('add')
                        pres = list()
                        for end in programs_list:
                            print('end')
                            pres.append([two, pars, end.stdout])
                        res.append(pres)'''

            self._data.update({one: res})

        return self

    def get_data(self):
        return self._data
