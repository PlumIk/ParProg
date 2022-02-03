#ifndef MPI_JACOBI_BASELINE_DATA_H
#define MPI_JACOBI_BASELINE_DATA_H

//Область моделирования
#define X0 -1
#define X1 1
#define Y0 -1
#define Y1 1

//Параметр уравнения
#define A (1e5)

//Порог сходимости
#define E (1e-6)

//Начальное приближение
#define PHI0 0

//Размеры сетки
#define NX 120//5000
#define NY 5000//120

//Шаги сетки
#define hx ((double)(X1-(X0))/(NX-1))
#define hy ((double)(Y1-(Y0))/(NY-1))

//Искомая функция (зависимость от i,j)
double phi(double i, double j);

double phi(double i, double j, int x, int y);

//Правая часть уравнения (зависимость от i,j)
double ro(double i, double j);

double ro(double i, double j, int x, int y);

#define I(i, j) ((i)*NY+j)

#endif //MPI_JACOBI_BASELINE_DATA_H
