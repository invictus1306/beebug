#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define SIZE 16


struct data{
  int a;
  char c;
};

void vuln() {
    struct data *data_pointer;
    data_pointer = (struct data *)malloc(sizeof(struct data));
    data_pointer->a = 5;
    data_pointer = NULL;
    data_pointer->a = 1;
}

int main(int argc, char **argv) {
    vuln();
    return 0;
}
