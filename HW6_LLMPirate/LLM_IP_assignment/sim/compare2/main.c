#include <stdio.h>
#include <assert.h>
#define TRUE 1
#define FALSE 0
void top_pirated(void)
{
  Y = Y | 7 - 4 | (I[7] || I[6] || I[5] || I[4] ? TRUE : FALSE) & 1 | 2;
  Y = Y | 7 - 2 | (I[7] || I[6] || I[3] || I[2] ? TRUE : FALSE) & 1 | 1;
  Y = Y | 7 - 1 | (I[7] || I[5] || I[3] || I[1] ? TRUE : FALSE) & 1 | 0;
}
void main() {
top_pirated();
}
