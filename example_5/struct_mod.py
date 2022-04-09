from __future__ import print_function
import frida
import sys

session = frida.attach("client.exe")
script = session.create_script("""
// 首先，让我们给自己一点内存来放入我们的结构体：
send('分配内存和写入字节...');
var st = Memory.alloc(16);
// 现在我们需要填充它 - 这有点生硬，但有效...
st.writeByteArray([0x02, 0x00, 0x13, 0x89, 0x7F, 0x00, 0x00, 0x01, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30]);
// Module.getExportByName() 不知道来源也能找到函数
// 模块，但速度较慢，尤其是在大型二进制文件上！ YMMV...
Interceptor.attach(Module.getExportByName(null, 'connect'), {
    onEnter: function(args) {
        send('注入恶意字节数组:');
        args[1] = st;
    }
    //, onLeave: function(retval) {
    //   retval.replace(0); // 使用它来操作返回值
    //}
});
""")


# 这是一些消息处理..
# [ 作为输出读取更有意义 :-D 错误得到 [!] 并且消息得到 [i] 前缀. ]
def on_message(message, data):
    if message['type'] == 'error':
        print("[!] " + message['stack'])
    elif message['type'] == 'send':
        print("[i] " + message['payload'])
    else:
        print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()
