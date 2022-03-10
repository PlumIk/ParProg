from Examples.launching.datalauchexample import DataLaunchExample
import itertools
import subprocess
import other.GlobalFunction as GFunction


def LaunchSome(data_launch: DataLaunchExample) -> DataLaunchExample:
    data = GFunction.any_list_to_string_list(data_launch.get_data_in())

    commands_run = list(itertools.product(*data))
    for pars in commands_run:
        pars_list = list()
        res = list()
        for one_par in pars:
            pars_list.append(one_par)

        for _ in range(data_launch.get_trails()):
            program_list = list()
            for _ in range(data_launch.get_at_same_time()):
                program_list.append(subprocess.Popen([data_launch.get_program_path()] + pars_list,
                                                     stdout=subprocess.PIPE,
                                                     text=True))
            for one_subproc in program_list:
                one_subproc.wait()
                some = GFunction.pars_out(one_subproc.stdout.read(), data_launch.get_searching_word())
                if some is not None:
                    res.append([pars, float(some)])
        data_launch.update_data_out(res)
    return data_launch
