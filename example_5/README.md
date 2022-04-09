<div align="center"><h1>注入恶意字节数组</h1></div>



### 目录

[1.client.c 目标代码](./client.c)

[2.struct_mod.py 版拦截代码](./struct_mod.py)


### 使用说明

#### 一. 编译 C 代码
```
gcc -Wall client.c -o client 
```
#### 二. 打开终端输入： 
```
nc -lp 5000
```
#### 三. 打开新的终端： 
```
./client 127.0.0.1
```
#### 四. 打开新的终端：
#### windows 平台
```
    # 要以管理员身份启动 cmd
    python3 struct_mod.py
```
#### linux 平台
```
    sudo sysctl kernel.yama.ptrace_scope=0
    python3 struct_mod.py
```

#### 五. 您将会看到的类似的效果（在输入 client 终端按下 ENTER 键 观察）
```
$ ./client 127.0.0.1
connect() is at: 0x1004013e0

这是 serv_addr 缓冲区:
02 00 13 88 7f 00 00 01 00 00 00 00 00 00 00 00

按 ENTER 键继续

无法连接: Connection refused

```

### 讲解
#### 注入恶意内存对象 - 示例：sockaddr_in struct

任何做过网络编程的人都知道， C 语言中最常用的数据类型之一是struct。
下面是一个简单的程序示例， 它创建一个网络套接字，并通过端口 5000 连接到服务器，
并通过回车键发送字符串"你好呀!" 到服务器。

创建文件 client.c 如下：
```gcc
#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

int main (int argc, char * argv[]){
  int sock_fd, i, n;
  struct sockaddr_in serv_addr;
  unsigned char * b;
  const char * message;
  char recv_buf[1024];

  if (argc != 2){
    fprintf (stderr, "用法: %s <服务器的ip>\n", argv[0]);
    return 1;
  }

  printf ("connect() is at: %p\n", connect);

  if ((sock_fd = socket (AF_INET, SOCK_STREAM, 0)) < 0){
    perror ("无法创建套接字");
    return 1;
  }

  bzero (&serv_addr, sizeof (serv_addr));

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons (5000);

  if (inet_pton (AF_INET, argv[1], &serv_addr.sin_addr) <= 0){
    fprintf (stderr, "无法解析 IP 地址\n");
    return 1;
  }
  printf ("\n这是 serv_addr 缓冲区:\n");
  b = (unsigned char *) &serv_addr;
  for (i = 0; i != sizeof (serv_addr); i++)
    printf ("%s%02x", (i != 0) ? " " : "", b[i]);

  printf ("\n\n按 ENTER 键继续\n");
  while (getchar () == EOF && ferror (stdin) && errno == EINTR);

  if (connect (sock_fd, (struct sockaddr *) &serv_addr, sizeof (serv_addr)) < 0){
    perror ("无法连接");
    return 1;
  }

  message = "你好呀!";
  if (send (sock_fd, message, strlen (message), 0) < 0){
    perror ("无法发送");
    return 1;
  }

  while (1){
    n = recv (sock_fd, recv_buf, sizeof (recv_buf) - 1, 0);
    if (n == -1 && errno == EINTR)
      continue;
    else if (n <= 0)
      break;
    recv_buf[n] = 0;

    fputs (recv_buf, stdout);
  }

  if (n < 0){
    perror ("无法阅读");
  }
```
这是相当标准的代码，并调用作为第一个参数给出的任何 IP 地址。如果您运行nc -lp 5000并在另一个终端窗口中运行 ./client 127.0.0.1，您应该会看到消息出现在 netcat 中，并且还能够将消息发送回作为client回报。
现在，我们可以开始找点乐子了——正如我们在上面看到的，我们可以将字符串和指针注入到进程中。我们可以通过操作程序 sockaddr_in作为其操作的一部分吐出的结构来做同样的事情：
```shell
$ ./client 127.0.0.1
connect() is at: 0x1004013e0

这是 serv_addr 缓冲区:
02 00 13 88 7f 00 00 01 00 00 00 00 00 00 00 00

按 ENTER 键继续
```
如果您不完全熟悉 struct 的结构，网上有很多资源会告诉您什么是什么。这里的重要位是 bytes 0x1388，或 5000 in dec。这是我们的端口号（后面的 4 个字节是十六进制的 IP 地址）。如果我们将其更改为，0x1389那么我们可以将我们的客户重定向到不同的点。如果我们改变接下来的 4 个字节，我们可以完全改变客户端指向的 IP 地址！

这是一个将恶意结构注入内存的脚本，然后劫持该 connect()函数libc.so以将我们的新结构作为其参数。

创建文件struct_mod.py 如下：
```python
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

```
请注意，此脚本演示了如何使用Module.getExportByName()API 在我们的目标中按名称查找任何导出的函数。如果我们可以提供一个模块，那么它在较大的二进制文件上会更快，但这在这里不那么重要。

现在，运行./client 127.0.0.1，在另一个终端运行nc -lp 5001，并在第三个终端运行./struct_mod.py。一旦我们的脚本运行，在终端窗口中按 ENTER client，netcat 现在应该显示客户端发送的字符串。

我们通过将我们自己的数据对象注入内存并将我们的进程与 Frida 挂钩，并使用Interceptor 它来完成我们在操作函数中的脏活，成功地劫持了原始网络。

这显示了 Frida 的真正威力——无需修补、复杂的倒车，也无需费时费力地盯着没完没了的拆解。

这是一个演示上述内容的快速视频：

https://www.youtube.com/watch?v=cTcM7R872Ls