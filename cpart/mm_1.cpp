#include<algorithm> // for std::min()
#include<cstdio>    // for printf
#include<chrono>    // for time measurement
#include <stdio.h>
#include <stdlib.h>


void init_matrices(int m,int n,int k,double *c,double *a,double *b) {
    for (int i=0;i<m*n;i++) c[i] = 0.0;
    for (int i=0;i<m*k;i++) a[i] = 1.0;
    for (int i=0;i<k*n;i++) a[i] = 2.0;
}

// blocked matrix multiplication: c[m][n] += a[m][k]*b[k][n]
void multiply_matrices_blocked(int m,int n,int k,double *c,const double *a,const double *b,int bm,int bn,int bk) {
    for (int ibm=0;ibm<m;ibm+=bm)
        for (int ibn=0;ibn<n;ibn+=bn)
            for (int ibk=0;ibk<k;ibk+=bk)
                for (int im=ibm;im<std::min(m,ibm+bm);im++)
                    for (int in=ibn;in<std::min(n,ibn+bn);in++)
                        for (int ik=ibk;ik<std::min(k,ibk+bk);ik++)
                            c[im*n+in] += a[im*k+ik] * b[ik*n+in];
}

int main(int argc, char* argv[]) {
    int m, n, k;

    int bm, bn, bk;

    if(argc==2){
        int tmp1= atoi(argv[1]);
        m=300;
        n=300;
        k=300;
        bm=tmp1;
        bn=tmp1;
        bk=tmp1;
        if (m%bm!=0){
            printf("%lf %lf \n",(float)10000,(float)10000);
            return 0;
        }
    }else{
        printf("Bad input\n");
        return 0;

    }
    double *c = new double [m*n];
    double *a = new double [m*k];
    double *b = new double [k*n];

    init_matrices(m,n,k,c,a,b);
    auto t2 = std::chrono::high_resolution_clock::now();
    multiply_matrices_blocked(m,n,k,c,a,b,bm,bn,bk);
    auto t3 = std::chrono::high_resolution_clock::now();

    double dt_blocked = 1.0e-3 * std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();

    printf("%lf %lf \n",dt_blocked,dt_blocked);

    delete[] c;
    delete[] a;
    delete[] b;

 }