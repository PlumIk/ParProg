from Examples.launching.datalauchexample import DataLaunchExample
import itertools
import subprocess
import timeit
import other.GlobalFunction as GFunction


def LaunchSome(data_launch: DataLaunchExample) -> DataLaunchExample:
    data = GFunction.to_string(data_launch.get_data_in())

    commands_run = list(itertools.product(*data))
    for pars in commands_run:
        pars_list = list()
        res = list()
        for one_par in pars:
            pars_list.append(one_par)

        """ out_dat = 0
        for one in pars_list:
            if one.isdigit():
                out_dat += int(one)

        for_test = 'time:'+str(out_dat)
        some = GFunction.pars_out(for_test, data_launch.get_searching_word())
        if some is not None:
            res.append([pars, out_dat])"""
        for _ in range(data_launch.get_trails()):
            program_list = list()
            for _ in range(data_launch.get_at_same_time()):
                print(['./' + data_launch.get_program_path()] + pars_list)
                program_list.append(subprocess.Popen(['./' + data_launch.get_program_path()] + pars_list,
                                                     stdout=subprocess.PIPE,
                                                     text=True))
            for one_subproc in program_list:
                one_subproc.wait()
                some = GFunction.pars_out(one_subproc.stdout.read(), data_launch.get_searching_word())
                print(one_subproc.stdout.read())
                print('some ', some)
                if some is not None:
                    res.append([pars, float(some)])
                print(res)
        data_launch.update_data_out(res)
    return data_launch
