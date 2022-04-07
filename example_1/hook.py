from __future__ import print_function
import frida
import sys

# 附加进程
session = frida.attach("hello")

# 定义被注入JS代码
qjs = """
Interceptor.attach(ptr("%s"), {
    onEnter: function(args) {
        send(args[0].toInt32());
    }
});
""" % int(sys.argv[1], 16)

# 创建JS脚本
script = session.create_script(qjs)


# 定义JS脚本数据接收函数
def on_message(message, data):
    print(message)


# 监听JS脚本数据接收函数
script.on('message', on_message)
# 注入并等待
script.load()
sys.stdin.read()
