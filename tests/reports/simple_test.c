#include<stdio.h>

int main() {
    int choice;
    do {
        printf("Menu\n\n");
        printf("Add Movie\n");
        printf("Search Movie\n");
        printf("Exit\n");
        scanf("%d", &choice);
 
        switch (choice) {
            case 1:
                printf("add\n");
                break;
            case 2:
                printf("nSearch\n");
                break;
            case 3:
                printf("goodbye\n");
                break;
            default:
                printf("wrong choice.Enter Again");
                break;
        }
    } while(choice !=3);
}
