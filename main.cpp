#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <omp.h>
#include <cstdlib>
#include <algorithm>
#include <string>

#include "Jacobi.h"
#include "CommonsParaLib.h"

void swap(Grid<2,double> & a, Grid<2,double> & b)
{
    double * tmp = a.gridArray;
    a = b;
    b.gridArray = tmp;
}

void printMessage(std::string message, ParaHelper& parahelper) {
    if (parahelper.getCurrentProccesNumber(MPI_COMM_WORLD) == 0) {
        std::cout << message << std::endl;
    }
	MPI_Barrier(MPI_COMM_WORLD);
}

void printProgress(int iteration, double delta, ParaHelper& parahelper) {
    if (parahelper.getCurrentProccesNumber(MPI_COMM_WORLD) == 0) {
        std::cout << "\r" << "iteration number: " << iteration << " delta: " << delta;

        std::cout.flush();
    }
}

std::initializer_list<bool> getDecList(int dec) {
    switch (dec) {
        case 0:
            return {true,false};
        case 1:
            return {false,true};
        case 2: 
            return {true,true};
        default:
            return {true,false};
    };
}

bool getXDecParam(int dec) {
    if (dec == 0) { return true; }
    return false;
}
bool getYDecParam(int dec) {
    if (dec == 0) { return false; }
    return true;
}
 
int main(int argc, char** argv)
{
    ParaHelper parahelper(argc, argv);

    int nx = parahelper.getParametr("-nx", 5000);
    int ny = parahelper.getParametr("-ny", 120);
    int decompositionParam = parahelper.getParametr("-dec", 0);
    double HX = ((double)(X1-(X0))/(nx-1));
    double HY = ((double)(Y1-(Y0))/(ny-1));
    int isCyclReverse = parahelper.getParametr("-reverse", 0);
    int threadsNum = parahelper.getParametr("-threadnum", 1);
    int visualParamInt = parahelper.getParametr("-visual", 0);
    int progressParamInt = parahelper.getParametr("-progress", 0);
    bool visualParam = visualParamInt == 0 ? false : true;
    bool progressParam = progressParamInt == 0 ? false : true;

    ThreadPool pool{std::size_t(threadsNum)};

    bool xdec = getXDecParam(decompositionParam);
    bool ydec = getYDecParam(decompositionParam);
    
    DecompositionType ddd(MPI_COMM_WORLD, {xdec,ydec}, { 0,0 });
    Grid<2, double> v1({ nx,ny }, ddd), v2({ nx,ny }, ddd), v3({ nx,ny }, ddd), v4({nx,ny}, ddd);

    Grid<2, double>& u1 = v1, & u2 = v2, & u3 = v3, & u4 = v4;

    Range<2> r({ nx , ny });

    Range<2> r_in({ 1,1 }, { nx-1, ny-1 });

    bool x_startPoint_addition = ddd.getDimParam(X_DIMENTION); 
    bool y_startPoint_addition = ddd.getDimParam(Y_DIMENTION);
    std::string x_str = x_startPoint_addition ? "x : true" : "x : false";
    std::string y_str = y_startPoint_addition ? "y : true" : "y : false";
    int x_add = x_startPoint_addition ? -1 : 0;
    int y_add = y_startPoint_addition ? -1 : 0;
    printMessage(x_str,parahelper);
    printMessage(y_str,parahelper);
    /*printMessage(std::to_string(u3.getSize(X_DIMENTION)),parahelper);
    printMessage(std::to_string(u3.getSize(Y_DIMENTION)),parahelper);
    printMessage(std::to_string(u3.length()),parahelper);*/
    if (x_startPoint_addition) {
        if (nx % parahelper.getNumberOfProcceses(MPI_COMM_WORLD) != 0)
        {
            printMessage("X Grid size should be multiple of number of processes\n", parahelper);
            return 0;
        }
    } else {
        if (ny % parahelper.getNumberOfProcceses(MPI_COMM_WORLD) != 0)
        {
            printMessage("Y Grid size should be multiple of number of processes\n", parahelper);
            return 0;
        }
    }


    double * counter = new double[1];
    counter[0] = 1;

    r.for_each(&u4, [&u4,&counter](const int indexes[2]) {
        u4(indexes[0],indexes[1]) = counter[0]; 
        counter[0]++;
    });

    r.for_each(&u1, [&u3, &u2, &u1,nx,ny](const int indexes[2]) {
        u3(indexes) = phi(indexes[0] + u3.getShift().X, 
                          indexes[1] + u3.getShift().Y,nx,ny);
        u2(indexes) = phi(indexes[0] + u2.getShift().X, 
                          indexes[1] + u2.getShift().Y,nx,ny);
        u1(indexes) = phi(indexes[0] + u1.getShift().X, 
                          indexes[1] + u1.getShift().Y,nx,ny);
    });

    r_in.for_each(&u1, [&u2, &u1](const int indexes[2]) {
        u1(indexes) = PHI0;
        u2(indexes) = PHI0;
    });

    printMessage("Data inited...", parahelper);

    std::function<double(const int[2])> diff_function = [&u1, &u2](const int indexes[2]) -> double {
         return std::abs(u1(indexes) - u2(indexes));
    };

    std::function<void(const int[2])> main_function = [&u1, &u2,nx,ny,HX,HY](const int indexes[2]) -> void {
        int i = indexes[0];
        int j = indexes[1];
        int r1 = i + u2.getShift().X;
        int r2 = j + u2.getShift().Y;

        u2(i, j) = (1.0 / (2.0 / (HX * HX) + 2.0 / (HY * HY) + A)) *
            ((u1(i + 1, j) + u1(i - 1, j)) / (HX * HX) +
                (u1(i, j + 1) + u1(i, j - 1)) / (HY * HY) -
                ro(r1, r2, nx, ny));
    };

    double diff = 0;
    int iterations = 0;
    double t_start = MPI_Wtime();

    std::stringstream visualStream;

    do {
        u1.send_grid_bound();

        if (!isCyclReverse) {
            r_in.for_each(&u1, &pool,main_function);
        }
        else {
            r_in.for_each_reverse(&u1, &pool,main_function);
        }

        diff = Reduce::reduce<2, double, Operation::MAX>(r, &u2, diff_function);

        swap(u1, u2);
        if (progressParam) {
            if (iterations % 100 == 0) {
                printProgress(iterations, diff, parahelper);
            }
        }

        if (visualParam) {
            visualStream << u2.visualPrint(iterations).rdbuf();
        }

        iterations++;
    } while (diff >= E);

    double t_end = MPI_Wtime();

    if (visualParam) {
        std::string dirName = "visual";
        parahelper.writeVisualization(visualStream.rdbuf(), dirName);
    }

    std::function<double(const int[2])> f2 = [&u3, &u2](const int indexes[2]) -> double {

        return std::abs(u2(indexes) - u3(indexes));
    };

    Range<2> r3({ nx, ny });

    double error = Reduce::reduce<2, double, Operation::MAX>(r3, &u2, f2);

    if (parahelper.getCurrentProccesNumber() == 0) {
        std::cout << std::endl;
        std::cout <<  "Delta: " << diff << std::endl;
        std::cout << "Error: " << error << std::endl;
        std::cout <<  "Iterations: " << iterations << std::endl;
        printf("Time: %f\n", t_end - t_start);
    }
    /*
    double sum = Reduce::reduce<double, MPI_SUM>(range2d,
        [&v1, &v2](const int i, const int j) -> double
    { return std::abs(v1.at(i, j) - v2.at(i, j)); }
    );*/


    /*
    Grid<2, double> grid(MPI_COMM_WORLD, { 4,4 });
    
    Range<2> allRange({4,4});

    allRange.for_each([&grid](int i, int j) -> void {
        grid(i, j) = 5;
    });

    grid.print();

    Range<2> range({ 1,1 }, { 3,3 });

    range.for_each([&grid](int i, int j) -> void {
        grid(i, j) = 0;
    });

    grid.print();

    range.for_each([&grid](int i, int j) -> void {
        grid(i, j) = 4;
    });

    grid.print();*/
    
    /*DecompositionType dddd(MPI_COMM_WORLD,{ true,false }, { 0,0 });
    
    Grid<2, double> grid({ NX,NY }, dddd);
    Grid<2, double> prev_grid({ NX,NY }, dddd);

    t_start = MPI_Wtime();
    int iteration_count = jacobi_method(grid, prev_grid);
    t_end = MPI_Wtime();
    
    double delta = get_observational_error(grid);

    if (parahelper.getCurrentProccesNumber(MPI_COMM_WORLD) == 0)
    {
        printf("Iteration count: %d\n", iteration_count);
        printf("Time: %f\n", t_end - t_start);
        printf("Delta: %lf\n", delta);
    }*/
    
    return 0;
}