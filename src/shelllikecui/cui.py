import time
import shlex
import threading
from typing import Union, Callable, Iterable

CNF = 'command_not_found'


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

    def update_func(self, func: Callable) -> None:
        self.func = func

    def func(s: str):
        return None


def make_command(name: str, func: Callable, alias: Union[Iterable[str], str] = (), desc: str = '') -> CommandBase:
    a = CommandBase(name, alias, desc)
    a.update_func(func)
    return a


mkcmd = make_command


class Cui:
    def __init__(self) -> None:
        # self.pth = './'
        # self.ps1 = 'user@Cui%s%s# '
        # self.ps1_full: bool = False
        self.ps1 = '> '
        self.clk = 0.1
        self.all_cmd = dict()
        self.alias = dict()
        self.lk = threading.Lock()
        self.lock = self.lk.acquire
        self.unlock = self.lk.release
        self.exit_flag = False

        self.mkcmd = self.make_command

        self.mkcmd(CNF, lambda arg: print('Command Not Found:', shlex.split(arg)[0]),
                   list(), 'Command Not Found Exception default function')
        self.mkcmd('exit', self.exit, list(), 'Python sys.exit')
        self.mkcmd('help', self.helps, list(), 'print this message')

    def slp(self, i: int = 1) -> None:
        time.sleep(self.clk * i)

    def register(self, a: CommandBase, rewrite: bool = False) -> dict:
        res = dict()
        if a.name in self.all_cmd:
            res[a.name] = a.name
            if not rewrite:
                return res
        self.all_cmd[a.name] = a

        for i in a.alias:
            if i in self.alias:
                res['%s %s' % (a.name, i)] = '%s %s' % (self.alias[i], i)
                if not rewrite:
                    continue
            self.alias[i] = a.name
        return res

    def make_command(self, name: str, func: Callable, alias: Union[Iterable[str], str] = (), desc: str = '', rewrite: bool = False) -> dict:
        self.register(make_command(name, func, alias, desc), rewrite)

    def help(self, name: str) -> str:
        s = name
        if len(self.all_cmd[name].alias) > 1:
            s += '['
            for i in self.all_cmd[name].alias:
                if i == name:
                    continue
                s += ',' + i
            s += ']'
        s += ': ' + self.all_cmd[name].desc
        return s

    def helps(self, arg: str = ''):
        arg = shlex.split(arg)[1:]
        if not arg:
            arg = self.all_cmd.keys()
        for i in arg:
            if i == CNF:
                continue
            print(self.help(i))
        return None

    def exit(self, arg: str):
        self.lock()
        self.exit_flag = True
        self.unlock()

    def __get_func(self, name: str) -> Callable:
        return self.all_cmd[self.alias.get(name, CNF)].func

    def exec(self, s: str):
        s = s.strip()
        if not s:
            return None
        name = s.split(' ', 1)[0]
        return self.__get_func(name)(s)

    def cmd(self, s: str):
        code = self.exec(s)
        print(self.ps1, end='', flush=True)
        return code

    def always_input(self) -> None:
        print(self.ps1, end='', flush=True)

        self.lock()
        while not self.exit_flag:
            self.unlock()
            self.cmd(input())
            self.lock()
