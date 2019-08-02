import subprocess


def per2eng(dict1):
    mydict = {
            '۰':'0',
            '۱':'1',
            '۲':'2',
            '۳':'3',
            '۴':'4',
            '۵':'5',
            '۶':'6',
            '۷':'7',
            '۸':'8',
            '۹':'9',
            }
    for c in dict1:
        if c.isalpha():
            a = mydict[c]
            dict1  = dict1.replace(c,a)
    return dict1


def sendmessage(title, message):
""" show notify-send for GNU/Linux Users."""
    subprocess.Popen(['notify-send', title, message])
    return
