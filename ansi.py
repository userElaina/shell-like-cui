s = '123abc'

def p(i: int):
    print('%03d: \x1b[%dm%s\x1b[0m%s\n' % (i, i, s, s))


def t(i: int):
    for i in range(i, i+8):
        p(i)


'''
p(0) # Origin
p(1) # Bold (or Bright)
p(3) # Italic
p(4) # Underline
p(7) # text_bg_color_swap
p(8) # hide
p(9) # del


t(30)
t(40)
t(90)
t(100)
# *0~*7: black red green yellow blue magenta cyan white
# 3* 4* 9* 10*: text bg text-bright bg-bright

# 1 (when Bright), 3x = 9x = 1, 9x
# 1 (when Bold), 3x = 1, 9x; 
'''

# t(10)
# t(20)
