#include <stdio.h>
#include <unistd.h>

void f (int n){
    printf ("Number: %d\n", n);
}

int main (int argc,char * argv[]){
    int i = 0;
    // 打印 f 方法函数地址
    printf ("f() is at %p\n", f);

    while (1){
        f (i++);
        sleep (1);
    }
}