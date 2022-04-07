<div align="center"><h1>注入字符串和调用函数</h1></div>



### 目录

[1.hi.c 目标代码](./hi.c)

[2.stringhook.py 版拦截代码](./stringhook.py)


### 使用说明

#### 一. 编译 C 代码
```
gcc -Wall hi.c -o hi  
```
#### 二. 启动程序并记下 f() ( 0x5617919e9169 在里面 以下示例）： 
```
f() is at 0x5617919e9169
s is at 0x5617919ea010
String: 测试字符串
String: 测试字符串
…
```
#### 三. 使用您从上面选择的地址运行此脚本（ 0x5617919e9169 在我们的 例子）：
#### windows 平台
```
    # 要以管理员身份启动 cmd
    python3 stringhook.py 0x5617919e9169
```
#### linux 平台
```
    sudo sysctl kernel.yama.ptrace_scope=0
    python3 stringhook.py 0x5617919e9169
```

#### 四. 您将会看到的类似的效果（在输入 hi 终端观察）
```
...
String: 测试字符串
String: 我调用了!
String: 测试字符串
String: 测试字符串
...
```