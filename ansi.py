STR = '123abc'


def p(i: int) -> None:
    print('%03d: \x1b[%dm%s\x1b[0m%s' % (i, i, STR, STR))


def pp(i: int, j: int) -> None:
    print('%03d, %03d: \x1b[%dm\x1b[%dm%s\x1b[0m%s' % (i, j, i, j, STR, STR))


def t(i: int):
    for i in range(i, i+8):
        p(i)


p(0)  # Origin
p(1)  # vsc: Bold; Terminal: Bright
p(2)  # weak (n: vsc) (Not widely supported)
p(3)  # Italic (Not widely supported)
p(4)  # Underline
p(5)  # blink (n: vsc)
p(6)  # blink (n: vsc)
p(7)  # text_bg_color_swap
p(8)  # hide (Not widely supported)
p(9)  # del (Not widely supported)

p(53)  # Overlined (n: vsc)

t(30)
t(40)
t(90)  # Not in standard
t(100)  # Not in standard

# x0~x7: black red green yellow blue magenta cyan white
# x8: rgb24 or x256
# 3x 4x 9x 10x: text bg text-bright bg-bright

# vsc: (1, 3x) = (1, 9x);
# Terminal: (1, 3x) = (9x) = (1, 9x)

for x in range(8):
    s = '(%02d, %02d), (%02d), (%02d, %02d): '
    s %= (1, 30 + x, 90 + x, 1, 90 + x)
    s += '\x1b[%dm\x1b[%dm%s\x1b[0m\x1b[%dm%s\x1b[%dm%s\x1b[0m%s'
    s %= (1, 30 + x, STR, 90 + x, STR, 1, STR, STR)
    print(s)

# t(10)  # (n: vsc, Terminal)
# p(18)  # (n: vsc, Terminal)
# p(19)  # (n: vsc, Terminal)
# p(20)  # (n: vsc, Terminal)
# t(50)  # (n: vsc, Terminal)
# t(60)  # (n: vsc, Terminal)
