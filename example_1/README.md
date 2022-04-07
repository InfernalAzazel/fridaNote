<div align="center"><h1>HOOK hello.c 并监听该函数输出</h1></div>



### 目录

[1.目标代码](./hello.c)

[2.hook代码 py版](./hook.py)

[3.hook代码 ipynb 版](./hook.ipynb)


### 使用说明

### 编译 C 代码
```
gcc -Wall hello.c -o hello  
```
#### 启动程序并记下 f() ( 0x400544 在里面 以下示例）： 
```
f() is at 0x5588fa7f8169
Number: 0
Number: 1
Number: 2
…
```
### 使用您从上面选择的地址运行此脚本（ 0x400544在我们的 例子）：
#### windows 平台
``` python
    # 要以管理员身份启动 cmd
    python hook.py 0x5588fa7f8169
```
#### linux 平台
```
    sudo sysctl kernel.yama.ptrace_scope=0
    python hook.py 0x5588fa7f8169
```