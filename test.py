from shelllikecui import mkcui1

a = mkcui1()


def qwq(arg: str) -> None:
    print('QAQ')


a.mkcmd('qwq', qwq, ['qaq', 'quq'], 'QwQ')

print(a.all_cmd)
print(a.alias)

a.always_input()

'''
qwq
help
exec print(1)
eval 1+2
eval 'a'
exit
'''
