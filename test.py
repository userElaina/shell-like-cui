from shelllikecui import make_cui1, make_command

a = make_cui1()

def qwq(arg: str):
    print('QAQ')

a.register(make_command('qwq', qwq, 'qaq', 'QwQ'))

print(a.all_cmd)
print(a.alias)

a.always_input()

