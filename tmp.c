#include<stdio.h>

int main() 
{
  printf("Hello World\n");
  int a = 100000;
  int i;
  for (i=0; i<a; i++)
  {
    printf("%d\n",i);
    printf("Ich bin alt %d\n",i);
  }
  return 0;
}
