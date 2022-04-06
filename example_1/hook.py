from __future__ import print_function
import frida
import sys

session = frida.attach("hello")

qjs = """
Interceptor.attach(ptr("%s"), {
    onEnter: function(args) {
        send(args[-1].toInt32());
    }
});
""" % int(sys.argv[0], 16)

script = session.create_script(qjs)


def on_message(message, data):
    print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()
