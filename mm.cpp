#include<algorithm> // for std::min()
#include<cstdio>    // for printf
#include<chrono>    // for time measurement

void init_matrices(int m,int n,int k,double *c,double *a,double *b) {
  for (int i=0;i<m*n;i++) c[i] = 0.0;
  for (int i=0;i<m*k;i++) a[i] = 1.0;
  for (int i=0;i<k*n;i++) a[i] = 2.0;
}

// matrix multiplication: c[m][n] += a[m][k]*b[k][n]
void multiply_matrices(int m,int n,int k,double *c,const double *a,const double *b) {
  for (int im=0;im<m;im++)
    for (int in=0;in<n;in++)
      for (int ik=0;ik<k;ik++)
        c[im*n+in] += a[im*k+ik] * b[ik*n+in];
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

int main() {
  const int m = 1500;
  const int n = 1500;
  const int k = 1500;
  double *c = new double [m*n];
  double *a = new double [m*k];
  double *b = new double [k*n];
  int bm = 100;
  int bn = 100;
  int bk = 100;

  init_matrices(m,n,k,c,a,b);
  auto t0 = std::chrono::high_resolution_clock::now();
  multiply_matrices(m,n,k,c,a,b);
  auto t1 = std::chrono::high_resolution_clock::now();

  init_matrices(m,n,k,c,a,b);
  auto t2 = std::chrono::high_resolution_clock::now();
  multiply_matrices_blocked(m,n,k,c,a,b,bm,bn,bk);
  auto t3 = std::chrono::high_resolution_clock::now();

  double dt_normal = 1.0e-3 * std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
  double dt_blocked = 1.0e-3 * std::chrono::duration_cast<std::chrono::milliseconds>(t3 - t2).count();

  printf("%lf %lf\n",dt_normal,dt_blocked);

  delete[] c;
  delete[] a;
  double * ret=new double[2];
  ret[0]=dt_normal;
  ret[1]=dt_blocked;

 }