from Examples.launching.datalauchexample import DataLaunchExample
import itertools
import subprocess
import timeit
import other.GlobalFunction as GFunction


def LaunchSome(data_launch: DataLaunchExample) -> DataLaunchExample:
    data = GFunction.to_string(data_launch.get_data_in())

    commands_run = list(itertools.product(*data))

    for one in data_launch.get_compilers():
        res = list()
        for two in data_launch.get_keys().get(one):

            key = ''
            for key_one in two:
                key += key_one + ' '
            key = key[:len(key) - 1]
            res = list()

            print(one + ' ' + data_launch.get_program_path() + ' '+key+' ' + data_launch.get_compiler() + ' ' +
                  data_launch.get_compiler_name())

            subprocess.run([one, data_launch.get_program_path(), key, data_launch.get_compiler(),
                            data_launch.get_compiler_name()])

            for pars in commands_run:

                one_command = 'subprocess.Popen([\'./\' +\'' + data_launch.get_compiler_name() + '\','
                for one_par in pars:
                    one_command += '\'' + str(one_par) + '\','
                one_command = one_command[:len(one_command) - 1]
                one_command += '])'
                print(one_command)

                all_command = 'programs_list = list()\n'
                for i in range(data_launch.get_at_same_time()):
                    all_command += 'programs_list.append(' + one_command + ')\n'
                all_command += 'for i in programs_list:\n\twhile i.poll() is None:\n\t\tpass'
                print(all_command)

                for i in range(data_launch.get_trails()):
                    time = timeit.timeit(setup='import subprocess', stmt=all_command, number=1)
                    res.append([two, pars, time])

        data_launch.update_data_out({one: res})
    return data_launch
