""" Utilities for naming log directories """
import os
import glob


def kwargs_to_exp_name_strs(kwargs):
    """ given the kwargs to run, produce log dir name postfix """
    ignore = {'num_runs', 'epochs', 'steps_per_epoch', 'num_cpu'}
    shortnames = {'hidden_sizes': 'hid', 'activation': '', 'env_name': '',
                  'algo': ''}
    str_val_funcs = {'hidden_sizes': hidden_sizes_to_str,
                     'activation': tf_activation_to_str}
    return [shortnames.get(name, name)
            + str_val_funcs.get(name, lambda x: str(x).lower())(val)
            for name, val in kwargs.items() if name not in ignore]


def hidden_sizes_to_str(hidden_sizes):
    """ convert hidden sizes tuple (32,64) and similar to str for exp name """
    return '-'.join(map(str, hidden_sizes))


def tf_activation_to_str(activation):
    """ convert tf activation function to string """
    return str(activation).split()[1]


def kwargs_to_exp_name(prefix, kwargs):
    """ produce experiment name from run kwargs """
    exp_name_strs = kwargs_to_exp_name_strs(kwargs)
    after_prefix = '_' if (exp_name_strs and prefix) else ''
    return prefix + after_prefix + '_'.join(exp_name_strs)


def output_dir_from_kwargs(prefix, implementation, kwargs, seed=None):
    """ build name of output directory (as a string) """
    exp_name = kwargs_to_exp_name(prefix, kwargs)
    output_dir = os.path.join('./data/{}'.format(implementation),
                              exp_name, exp_name)
    return output_dir + '_s{}'.format(seed) if (seed is not None) else output_dir


def num_run_epochs(prefix, implementation, seed, kwargs):
    """ returns the number of epochs that have been run with this
    configuration """
    output_dir_base = output_dir_from_kwargs(
        prefix, implementation, kwargs)
    path = os.path.join(output_dir_base + '_s{}'.format(seed), 'progress.txt')
    if not os.path.exists(path):
        return 0
    linecount = -1 # subtract one for header
    with open(path, 'r') as fileobj:
        for _ in fileobj:
            linecount += 1
    return linecount


def seeds(num_runs):
    """ Iterate through seeds (spinup goes through 10's for some reason?) """
    for run_no in range(num_runs):
        yield 10*run_no


def already_run_seeds(prefix, implementation, kwargs):
    """ returns a list of the seeds that have already been run with
    these arguments """
    base_outdir = output_dir_from_kwargs(prefix, implementation, kwargs)
    return [int(outdir.split('s')[-1])
            for outdir in glob.glob(base_outdir + '_s*')]
