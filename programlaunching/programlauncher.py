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

            print(one + ' ' + data_launch.get_program_path() + ' ' + key + ' -o now.out')

            subprocess.run([one, data_launch.get_program_path(), key, '-o', 'now.out'])

            if data_launch.get_initial_key() == "":
                data_launch.set_initial_key('./now.out')
            else:
                data_launch.set_initial_key(data_launch.get_initial_key() + ' ./now.out')

            for pars in commands_run:

                pars_list = list()
                for one_par in pars:
                    pars_list.append(one_par)

                for _ in range(data_launch.get_trails()):
                    program_list = list()
                    for _ in range(data_launch.get_at_same_time()):
                        print([data_launch.get_initial_key()] + pars_list)
                        program_list.append(subprocess.Popen([data_launch.get_initial_key()] + pars_list,
                                                             stdout=subprocess.PIPE,
                                                             text=True))

                    for one_subproc in program_list:
                        one_subproc.wait()
                        res.append([two, pars, float(GFunction.pars_out(one_subproc.stdout.read())[0])])
        data_launch.update_data_out({one: res})
    return data_launch
