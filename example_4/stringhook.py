from __future__ import print_function
import frida
import sys

session = frida.attach("hi")
script = session.create_script("""
var st = Memory.allocUtf8String("我调用了!");
var f = new NativeFunction(ptr("%s"), 'int', ['pointer']);
    // 在 NativeFunction 中，参数 2 是返回值类型,
    // 参数 3 是输入类型的数组
f(st);
""" % int(sys.argv[1], 16))


def on_message(message, data):
    print(message)


script.on('message', on_message)
script.load()
