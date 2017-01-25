#include <iostream>
#include <iomanip>
#include <string>
#include <armadillo>

// Include the nodebug macro to atop the asserts
#define NDEBUG
#include <assert.h>

void hello_world(){
    std::cout<< "Hello world!" << std::endl;
    const char * day = "day!";
    std::cout << "What a beautiful " << day << std::endl;
    }

void print_dataArray(double * data, int nrows, int ncols)
{
	for (int i = 0; i < nrows; i++)
	{
		for	(int j = 0; j < ncols; j++)
			{
				std::cout << std::setw(6) << data[i * ncols + j] << "	";
			}
		std::cout << std::endl;
	}
}

void square_array(double * data_array, int nrows, int ncols)
{
	for (int i = 0; i < nrows; i++)
	for	(int j = 0; j < ncols; j++)
	{
		data_array[i * ncols + j] = data_array[i * ncols + j] * data_array[i * ncols + j];
	}
}

// void square_eMatrix(double * data_array, const int nrows, const int ncols)
// {
// 	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
// 														eMat(data_array, nrows, ncols);
// 	eMat.array() = eMat.array().square();
// 	print_dataArray(data_array, nrows, ncols);
// 	std::cout << eMat << std::endl;

// }


// void multiply_eMatrix(double * inputArr1, double * inputArr2, double * retArr, 
// 															int nrows, int ncols)
// {
// 	assert(nrows == ncols);
// 	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
// 														inputMat1(inputArr1, nrows, ncols);
// 	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
// 														inputMat2(inputArr2, nrows, ncols);
// 	Eigen::Map<Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor>> 
// 														retMat(retArr, nrows, ncols);
// 	retMat = inputMat1 * inputMat2;													

// }

int main()
{
	const int rowsN = 2;
	const int colsN = 2;
	int elemN = colsN * rowsN;
	double data_array[elemN];

	for (int i = 0; i < rowsN; i++)
	for	(int j = 0; j < colsN; j++)
	{
		data_array[i * colsN + j] = i * colsN + j;
	}
	print_dataArray(data_array, rowsN, colsN);

	arma::mat A = arma::randu<arma::mat>(1200, 1200);
	for (int i = 0; i< 100; i++)
	{
		A = A * A;
	}
	return 0;
}