from __future__ import print_function
import frida
import sys

session = frida.attach("hello")

qjs = """
Interceptor.attach(ptr("%s"), {
    onEnter: function(args) {
        // 每次 hook 都修改函数参数 改为 1337 数值
        args[0] = ptr("1337");
    }
});
""" % int(sys.argv[1], 16)

script = session.create_script(qjs)


def on_message(message, data):
    print(message)


script.on('message', on_message)

script.load()
sys.stdin.read()
