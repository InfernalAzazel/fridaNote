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

  return 0;
}