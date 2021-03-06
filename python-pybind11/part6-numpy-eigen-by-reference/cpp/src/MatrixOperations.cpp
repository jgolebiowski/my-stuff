//
// Created by Golebiowski, Jacek on 6/16/18.
//
#include <vector>
#include <MatrixOperations.h>
#include <iostream>


/**
 * @brief Generate a new vector of zeros
 * @param size size of the vector
 * @return the created vector
 */
EigenDynamicRowMajor &getMatrix(int size)
{
    auto mat = new EigenDynamicRowMajor;
    mat->setZero(size, size);
    return *mat;
}

/**
 * @brief Set matrix elements to random values
 * @param mat the matrix in question
 */
void setRandom(EigenRefDynamicRowMajor mat)
{
    mat.setRandom();
}

/**
 * @brief Print a given matrix
 * @param mat vector in question
 */
void printMatrix(EigenRefDynamicRowMajor mat)
{
    std::cout << "CPP Matrix:"
              << std::endl
              << mat
              << std::endl;
}


/**
 * @brief Get a vector of matrixes of given size
 * @param size Matrix size
 * @param length Vector length
 * @return Created vector
 */
std::vector<EigenRefDynamicRowMajor> &getVectorMatrix(
        int size, int length)
{
    auto vectorMatrix = new std::vector<EigenRefDynamicRowMajor>;
    for (int i = 0; i < length; i++)
    {
        auto mat = new EigenDynamicRowMajor;
        mat->setZero(size, size);
        vectorMatrix->push_back(*mat);
    }
    return *vectorMatrix;
}

/**
 * @brief For every matrix in a vector, matrix elements to random values
 * @param vectorMatrix the vector of matrices in question
 */
void setRandomVectorMatrix(
        std::vector<EigenRefDynamicRowMajor> &vectorMatrix)
{
    for (EigenRefDynamicRowMajor &mat : vectorMatrix)
    {
        mat.setRandom();
    }
}

/**
 * @brief Print the vector of matrices
 * @param vectorMatrix the vector of matrices in question
 */
void printVectorMatrix(
        std::vector<EigenRefDynamicRowMajor> &vectorMatrix)
{
    std::cout << "Vector of Eigen Matrices:" << std::endl;
    for (EigenRefDynamicRowMajor &mat : vectorMatrix)
    {
        std::cout << "Matrix:"
                  << std::endl
                  << mat
                  << std::endl;
    }
}