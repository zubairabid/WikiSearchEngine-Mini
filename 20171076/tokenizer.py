import re

#from nltk.tokenize import word_tokenize as custometoken

def custometoke(line):
    line = re.sub(r'(?:(?:https?:\/\/(?:www.)?)|www.)[A-Z0-9a-z_-]+(?:\.[A-Z0-9a-z_\/-]+)+', '', line)
    return re.findall(#r'[\U00010000-\U0010ffff]'\
            #r'|[A-Z0-9a-z]+[A-Z0-9a-z._%+-]*@[A-Z0-9a-z]+(?:\.[A-Z0-9a-z]+)+'\
            #r'|(?<= )[$€£¥₹]?[0-9]+(?:[,.][0-9]+)*[$€£¥₹]?'\
            #r'|(?:(?:https?:\/\/(?:www.)?)|www.)[A-Z0-9a-z_-]+(?:\.[A-Z0-9a-z_\/-]+)+'\
            #r'|(?:(?<=[^A-Za-z0-9])|^)@[A-Z0-9a-z._+]+[A-Za-z0-9_]'\
            #r'|#[A-Za-z0-9]+(?:[\._-][A-Za-z0-9]+)*'\
            #r'|\.{3,}'\
            #r'|[!"#$%\&\'()*+,\-.:;<=>?@\[\\\/\]\^_`{\|}~]'\
            #r'|[A-Z]\.'\
            r'|\w+', line)
