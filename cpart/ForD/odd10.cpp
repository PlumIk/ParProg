#include <stdio.h>
#include <stdlib.h>
#include<cstdio>
#include <unistd.h> // для Unix систем


int main(int argc, char* argv[]) { 
    if(argc==2){
        int tmp1= atoi(argv[1]);
        //printf("Input %d\n", tmp1);
        printf("Time:%f\n",tmp1%10+1.1);
    }else{
        printf("Bad input\n");
    }
     return 0;

 }
