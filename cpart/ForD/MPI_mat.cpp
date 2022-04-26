#include<stdio.h>
#include<stdlib.h>
#include<mpi.h>
#include<chrono> 	
#include<time.h>
 
int main(int argc,char *argv[])
{
	if(argc<3){
		return 0;
	}
    double start, stop;
    int maxa = atoi(argv[1]);
    int maxb = atoi(argv[1]);
    int i, j, k, l;
    int *a, *b, *c, *buffer, *ans;
    int size = 2000;
    int rank, numprocs, line;
 	auto t0 = std::chrono::high_resolution_clock::now();	
    MPI_Init(NULL,NULL);//MPI Initialize
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);// Получить текущий номер процесса
    MPI_Comm_size(MPI_COMM_WORLD,&numprocs);// Получить количество процессов
 
    line = size/numprocs;// Делим данные на блоки (количество процессов), и основной процесс также должен обрабатывать данные
    a = (int*)malloc(sizeof(int)*size*size);
    b = (int*)malloc(sizeof(int)*size*size);
    c = (int*)malloc(sizeof(int)*size*size);
    // Размер кеша больше или равен размеру обрабатываемых данных, когда он больше, чем фактическая часть данных
    buffer = (int*)malloc(sizeof(int)*size*line);// Размер пакета данных
    ans = (int*)malloc(sizeof(int)*size*line);// Сохраняем результат расчета блока данных
 
    // Основной процесс присваивает матрице начальное значение и передает матрицу N каждому процессу, а матрицу M передает каждому процессу в группах.
    if (rank==0)
    {
        for(i=0;i<size;i++) // Чтение данных
            for(j=0;j<size;j++)
                a[i*size+j]=(i+j)%maxa;  
 
        for(i=0;i<size;i++) 
            for(j=0;j<size;j++)
                b[i*size+j]=(i+j)%maxb;  

        // Отправить матрицу N другим подчиненным процессам
        for (i=1;i<numprocs;i++)
        {
                MPI_Send(b,size*size,MPI_INT,i,0,MPI_COMM_WORLD);
        }
        // Отправляем каждую строку a каждому подчиненному процессу по очереди
        for (l=1; l<numprocs; l++)
        {
            MPI_Send(a+(l-1)*line*size,size*line,MPI_INT,l,1,MPI_COMM_WORLD);
        }
        // Получаем результат, рассчитанный по процессу
        for (k=1;k<numprocs;k++)
        {
            MPI_Recv(ans,line*size,MPI_INT,k,3,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
            // Передаем результат в массив c
            for (i=0;i<line;i++)
            {
                for (j=0;j<size;j++)
                {
                    c[((k-1)*line+i)*size+j] = ans[i*size+j];
                }
 
            }
        }
        // Рассчитать оставшиеся данные
        for (i=(numprocs-1)*line;i<size;i++)
        {
            for (j=0;j<size;j++)
            {
                int temp=0;
                for (k=0;k<size;k++)
                    temp += a[i*size+k]*b[k*size+j];
                c[i*size+j] = temp;
            }
        }
        // Результат теста
        // Статистика по времени
 
        auto t1 = std::chrono::high_resolution_clock::now();
    	double dt_normal = 1.0e-3 * std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
    	printf("Time:%lf\n",dt_normal);
 
        free(a);
        free(b);
        free(c);
        free(buffer);
        free(ans);
    }
 
    // Другие процессы получают данные и после вычисления результата отправляют их в основной процесс
    else
    {
    	//printf("Here	\n");
        // Получаем широковещательные данные (матрица b)
        MPI_Recv(b,size*size,MPI_INT,0,0,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
 
        MPI_Recv(buffer,size*line,MPI_INT,0,1,MPI_COMM_WORLD,MPI_STATUS_IGNORE);
        // Рассчитать результат продукта и отправить результат в основной процесс
        for (i=0;i<line;i++)
        {
            for (j=0;j<size;j++)
            {
                int temp=0;
                for(k=0;k<size;k++)
                    temp += buffer[i*size+k]*b[k*size+j];
                ans[i*size+j]=temp;
            }
        }
        // Отправить результат расчета в основной процесс
        MPI_Send(ans,line*size,MPI_INT,0,3,MPI_COMM_WORLD);
    }
 
    MPI_Finalize();//Конец
    
 
    return 0;
}
