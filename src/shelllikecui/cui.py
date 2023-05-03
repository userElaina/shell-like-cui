import sys
import time
from typing import Union, Callable, Iterable

_CNF = 'command_not_found'


class CommandBase:
    def __init__(self, name: str, alias: Union[Iterable[str], str] = (), desc: str = '') -> None:
        self.name = name
        if isinstance(alias, str):
            self.alias = {alias, }
        else:
            self.alias = set(alias)
        self.alias.add(name)
        self.desc = desc

    def add_alias(self,  alias: Union[Iterable[str], str] = ()) -> None:
        if isinstance(alias, str):
            self.alias.add(alias)
        else:
            self.alias += set(alias)

    def func(s: str):
        return None


def make_command(name: str, func: Callable, alias: Union[Iterable[str], str] = (), desc: str = '') -> CommandBase:
    a = CommandBase(name, alias, desc)
    a.func = func
    return a


def _command_not_found(arg: str) -> int:
    f, arg = arg.split(' ', 1)
    print('Command Not Found:', f)
    return None


def _exit(arg: str):
    sys.exit(0)
    return None

def _none(arg: str):
    return None


class Cui:
    def __init__(self) -> None:
        # self.pth = './'
        # self.ps1 = 'user@Cui%s%s# '
        # self.ps1_full: bool = False
        self.ps1 = '> '
        self.clk = 0.1
        self.all_cmd = dict()
        self.alias = dict()

        self.register(make_command(_CNF, _command_not_found, 'cnf',
                                   'Command Not Found Exception default function'))
        self.register(make_command('exit', _exit, list(), 'exit by Python'))
        self.register(make_command('', _none, list(), 'nothing'))

    def slp(self, i: int = 1) -> None:
        time.sleep(self.clk * i)

    def register(self, a: CommandBase, rewrite: bool = False) -> dict:
        res = dict()
        if a.name in self.all_cmd:
            res[a.name] = a.name
            if not rewrite:
                return res

        self.all_cmd[a.name] = a.func
        for i in a.alias:
            if i in self.alias:
                res['%s %s' % (a.name, i)] = '%s %s' % (self.alias[i], i)
                if not rewrite:
                    continue
            self.alias[i] = a.name
        return res

    def _get_func(self, name: str) -> Callable:
        return self.all_cmd[self.alias.get(name, _CNF)]

    def exec(self, s: str):
        s = s.strip() + ' '
        name = s.split(' ', 1)[0]
        return self._get_func(name)(s)

    def cmd(self, s: str):
        code = self.exec(s)
        print(self.ps1, end='', flush=True)
        return code

    def always_input(self) -> None:
        print(self.ps1, end='', flush=True)
        while True:
            self.cmd(input())
