import shlex
import subprocess
from .cui import Cui


def make_cui0() -> Cui:
    return Cui()


def __exec(arg: str):
    name, arg = arg.split(' ', 1)
    try:
        exec(arg)
    except Exception as e:
        print(repr(e))
    return None


def __eval(arg: str):
    name, arg = arg.split(' ', 1)
    try:
        print(repr(eval(arg)))
    except Exception as e:
        print(repr(e))
    return None


def make_cui1() -> Cui:
    a = make_cui0()
    a.mkcmd('exec', __exec, list(), 'exec by Python')
    a.mkcmd('eval', __eval, list(), 'eval by Python')

    def __cui(arg: str):
        name, arg = arg.split(' ', 1)
        return a.exec(arg)
    a.mkcmd('cui', __cui, list(), 'exec by its Interpreter')

    def __sh(arg: str):
        name, arg = arg.split(' ', 1)
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
    a.mkcmd('sh', __sh, 'shell', 'exec by Shell')

    return a


mkcui0 = make_cui0
mkcui1 = make_cui1
