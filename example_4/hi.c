#include <stdio.h>
#include <unistd.h>

// 对应 stringhook.py qjs 变量里面，
// NativeFunction(ptr("%s"), 'int', ['pointer'])
int f (const char * s){
  printf ("String: %s\n", s);
  return 0;
}

int main (int argc, char * argv[]){
  const char * s = "测试字符串";

  printf ("f() is at %p\n", f);
  printf ("s is at %p\n", s);

  while (1){
    f (s);
    sleep (1);
  }
}