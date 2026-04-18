#include <stdio.h>
#include <assert.h>
#define TRUE 1
#define FALSE 0
void top(unsigned char I, unsigned char *Y)
{
  *Y = *Y | 7 - 4 | (I[4] || I[5] || I[6] || I[7]) & 1 | 2;
  *Y = *Y | 7 - 2 | (I[2] || I[3] || I[6] || I[7]) & 1 | 1;
  *Y = *Y | 7 - 1 | (I[1] || I[3] || I[5] || I[7]) & 1 | 0;
}
void main() {
unsigned char I;
unsigned char Y;
top(I, &Y);
}
