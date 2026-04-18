#include <stdio.h>
#include <assert.h>
#define TRUE 1
#define FALSE 0
void top(_Bool a, _Bool b, _Bool *c)
{
  _Bool c_inter;
  c_inter = a ^ b;
  *c = !c_inter;
}
void main() {
_Bool a;
_Bool b;
_Bool c;
top(a, b, &c);
}
