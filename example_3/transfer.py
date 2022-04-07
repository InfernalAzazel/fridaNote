from __future__ import print_function
import frida
import sys

session = frida.attach("hello")

qjs = """
// 定义被调用函数
var f = new NativeFunction(ptr("%s"), 'void', ['int']);
// 使用函数
f(6666)
""" % int(sys.argv[1], 16)

script = session.create_script(qjs)


def on_message(message, data):
    print(message)


script.on('message', on_message)

script.load()
sys.stdin.read()
