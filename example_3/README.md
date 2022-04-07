<div align="center"><h1>HOOK hello.c 调用它的函数</h1></div>



### 目录

[1.hello.c 目标代码](./hello.c)

[2.transfer.py 版拦截代码](./transfer.py)


### 使用说明

#### 一. 编译 C 代码
```
gcc -Wall hello.c -o hello  
```
#### 二. 启动程序并记下 f() ( 0x564b913e5169 在里面 以下示例）： 
```
f() is at 0x564b913e5169
Number: 0
Number: 1
Number: 2
…
```
#### 三. 使用您从上面选择的地址运行此脚本（ 0x564b913e5169 在我们的 例子）：
#### windows 平台
```
    # 要以管理员身份启动 cmd
    python3 transfer.py 0x564b913e5169
```
#### linux 平台
```
    sudo sysctl kernel.yama.ptrace_scope=0
    python3 transfer.py 0x564b913e5169
```

#### 四. 您将会看到的类似的效果（在输入 hello 终端观察）
```
...
Number: 41
Number: 42
Number: 6666
Number: 43
...
```