#include <stdio.h>
#include <string.h>

#define msg_len 5

char msgSecret[] = "This is the secret message";
char msgDefault[] = "This is the default message";

int print_secr() {
  printf("Congrats! %s\n", msgSecret);
  return 0;
}

int print_default(int num) {
  int add;
  add = num + 10;
  printf("Hello! %s, the number is %d\n", msgDefault, add);
  return 0;
}

int main(int argc, char **argv) {
  char message[msg_len];
  
  printf("Please enter a message: \n"); 
  fgets(message, msg_len, stdin);
 
  if (strcmp(message, "test")){
    print_default(12);
  } else {
  	print_secr();
  }
  return 0;
}