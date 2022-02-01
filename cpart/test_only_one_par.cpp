#include <stdio.h>
#include <stdlib.h>
#include<cstdio>
#include <unistd.h> // для Unix систем


int main(int argc, char* argv[]) {
    int m, n, k;

    int bm, bn, bk;

    if(argc==2){
        int tmp1= atoi(argv[1]);
        //printf("Input %d\n", tmp1);
        sleep(tmp1%3);
        printf("Time:%f\n",tmp1%3+0.0001);
    }else{
        printf("Bad input\n");
    }
     return 0;

 }