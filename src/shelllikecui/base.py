import shlex
import subprocess
from .cui import Cui, make_command


def make_cui0() -> Cui:
    return Cui()


def _exec(arg: str):
    f, arg = arg.split(' ', 1)
    try:
        exec(arg)
    except Exception as e:
        print(repr(e))
    return None


def _eval(arg: str):
    f, arg = arg.split(' ', 1)
    try:
        print(eval(arg))
    except Exception as e:
        print(repr(e))
    return None


def make_cui1() -> Cui:
    a = make_cui0()
    a.register(make_command('exec', _exec, list(), 'exec by Python'))
    a.register(make_command('eval', _eval, list(), 'eval by Python'))

    def _cui(arg: str):
        f, arg = arg.split(' ', 1)
        return a.exec(arg)
    a.register(make_command('cui', _cui, list(), 'exec by its Interpreter'))

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
        return None
    a.register(make_command('sh', _sh, 'shell', 'exec by Shell'))

    return a
