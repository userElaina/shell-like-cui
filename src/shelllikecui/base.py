import sys
import shlex
import subprocess

from .cui import Cui, make_command, _CNF


def make_cui0() -> Cui:
    return Cui()


def _command_not_found(arg: str) -> int:
    f, arg = arg.split(' ', 1)
    print('Command Not Found:', f)


def _exec(arg: str):
    f, arg = arg.split(' ', 1)
    try:
        exec(arg)
    except Exception as e:
        print(repr(e))


def _eval(arg: str):
    f, arg = arg.split(' ', 1)
    try:
        print(eval(arg))
    except Exception as e:
        print(repr(e))

def _exit(arg: str):
    sys.exit(0)


def make_cui1() -> Cui:
    a = Cui()

    a.register(make_command(_CNF, _command_not_found, 'cnf',
               'Command Not Found Exception default function'))

    def _cui(arg: str):
        f, arg = arg.split(' ', 1)
        return a.exec(arg)
    a.register(make_command('cui', _cui, list(), 'exec by its Interpreter'))

    a.register(make_command('exec', _exec, list(), 'exec by Python'))
    a.register(make_command('eval', _eval, list(), 'eval by Python'))
    a.register(make_command('exit', _exit, list(), 'exit by Python'))

    def _sh(arg: str):
        f, arg = arg.split(' ', 1)
        p = subprocess.Popen(
            shlex.split(arg),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        while p.poll() is None:
            a.slp()
        print(p.stdout.read().decode('utf8'))
    a.register(make_command('sh', _sh, 'shell', 'exec by Shell'))

    return a
