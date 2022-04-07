<div align="center"><h1>HOOK hello.c 修改函数的参数值</h1></div>



### 目录

[1.hello.c 目标代码](./hello.c)

[2.modify.py 版拦截代码](./modify.py)

[3.modify.ipynb 版拦截代码](./modify.ipynb)


### 使用说明

#### 一. 编译 C 代码
```
gcc -Wall hello.c -o hello  
```
#### 二. 启动程序并记下 f() ( 0x555f78c29169 在里面 以下示例）： 
```
f() is at 0x555f78c29169
Number: 0
Number: 1
Number: 2
…
```
#### 三. 使用您从上面选择的地址运行此脚本（ 0x555f78c29169 在我们的 例子）：
#### windows 平台
```
    # 要以管理员身份启动 cmd
    python3 modify.py 0x555f78c29169
```
#### linux 平台
```
    sudo sysctl kernel.yama.ptrace_scope=0
    python3 modify.py 0x555f78c29169
```

#### 四. 您将会看到的效果（在输入 hello 终端观察）
```
...
Number: 1337
Number: 1337
Number: 1337
Number: 1337
...
```