#include <stdio.h>
#include <cs50.h>

void print_blocks(int a);
void print_spaces(int b);
void print_left_side(int c, int d);
void print_right_side(int e, int f);

int main(void){
    // Prompt user for positive integer
    int n;
    do{
        n = get_int("Give me an integer. ");
    } while (n <= 0 || 8 < n);

    string center_blocks = "#  #";

    if (n > 1){
        for (int j = 1; j <= n; j++){
            print_left_side(j, n);
            printf("%s", center_blocks);
            print_right_side(j, n);
            printf("\n");
        }
    } else {
        printf("%s", center_blocks);
        printf("\n");
    }
}


void print_blocks(int a){
    for (int i = 0; i < a; i++){
        printf("%s", "#");
    }
}

void print_spaces(int b){
    for (int i = 0; i < b; i++){
        printf(" ");
    }
}

void print_left_side(int c, int d){
    if (c == d){
        print_blocks(d-1);
    }else if (c ==1){
        print_spaces(d-1);
    }else if (c < d){
        print_spaces(d-c);
        print_blocks(c-1);
    }
}

void print_right_side(int e, int f){
    if (e == f){
        print_blocks(f-1);
    }else if (e < f){
        print_blocks(e-1);
        print_spaces(f-e);
    }
}
