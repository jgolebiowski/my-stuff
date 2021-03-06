import os

import numpy as np
import scipy.sparse
import sklearn.datasets
import gzip


def write_partition_multiple(data, labels, partition_size, dataset_path, basefile="partition", writer=None):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_size : int
        Number of examples in a partition
    dataset_path : str
        Path to the dataset directory
    basefile : int
        Base of the partition names, should be uniqie or it will be overwritten
    partition_loder : function(data : ndarray, labels : ndarray, partition_name : str, dataset_path : str)
        Function used to write a partition
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"
    dataset_path = create_directory(dataset_path)
    size = len(labels)

    for idx in range(0, size, partition_size):
        partition_name = "{}-{}".format(basefile, idx)
        writer(data[idx: idx + partition_size],
               labels[idx: idx + partition_size],
               partition_name,
               dataset_path)


def numpy_write_partition(data, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"

    if type(data) == list:
        data = np.array(data)
    if type(labels) == list:
        labels = np.array(labels)

    partition = os.path.join(dataset_path, partition_name)
    np.savez(partition, data=data, labels=labels)


def numpy_load_partition(partition, input_path):
    """
    Load a partition and return the data and labels

    Parameters
    ----------
    partition : str
        Name of the dataset chunks
    input_path : str
        path to the dataset directory

    Returns
    -------
    ndarray
        Data record
    ndarray
        Labels
    """
    assert partition.endswith(".npz"), "File must be a .npz one"
    partition = os.path.join(input_path, partition)
    with np.load(partition) as part:
        data = part["data"]
        labels = part["labels"]
    return data, labels


def libsvm_write_partition_sparse_fromdense(data, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset, wrapper around libsvm_write_partition_sparse to be compatible with tests

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"
    datashape = data[0].shape
    dat = [scipy.sparse.csr_matrix(item.reshape((1, -1))) for item in data]
    lab = np.array(labels)
    libsvm_write_partition_sparse(dat, datashape, lab, partition_name, dataset_path)


def libsvm_write_partition_sparse(data, datashape, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : list[scipy.sparse.csr_matrix]
        List of sparse representations of the array as a (1, example_size) matrix
    datashape : tuple
        Shape of each example
    labels : ndarray or list
        The labels for this data. Shape: (n_examples, )
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    partition_dir = create_directory(os.path.join(dataset_path, partition_name))

    data = scipy.sparse.vstack(data)
    data_file = os.path.join(partition_dir, "data.libsvm.gz")
    with gzip.open(data_file, "w") as dfile:
        sklearn.datasets.dump_svmlight_file(data, labels, dfile, zero_based=True)

    header = "datashape${}\n".format(datashape)
    header_file = os.path.join(partition_dir, "header.libsvm.gz")
    with gzip.open(header_file, "w") as hfile:
        hfile.write(header.encode())


def libsvm_write_partition_dense(data, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"

    if type(data) == list:
        data = np.array(data)
    if type(labels) == list:
        labels = np.array(labels)

    partition_dir = create_directory(os.path.join(dataset_path, partition_name))
    data_file = os.path.join(partition_dir, "data.libsvm.gz")

    datashape = data.shape[1:]
    n_examples = data.shape[0]

    with gzip.open(data_file, "w") as dfile:
        sklearn.datasets.dump_svmlight_file(data.reshape((n_examples, -1)), labels, dfile, zero_based=True)

    header = "datashape${}\n".format(datashape)
    header_file = os.path.join(partition_dir, "header.libsvm.gz")
    with gzip.open(header_file, "w") as hfile:
        hfile.write(header.encode())


def libsvm_load_partition(partition, input_path):
    """
    Load a partition and return the data and labels

    Parameters
    ----------
    partition : str
        Name of the dataset chunks
    input_path : str
        path to the dataset directory

    Returns
    -------
    ndarray
        Data record
    ndarray
        Labels
    """
    partition = os.path.join(input_path, partition)
    data_file = os.path.join(partition, "data.libsvm.gz")
    header_file = os.path.join(partition, "header.libsvm.gz")

    assert os.path.isfile(data_file), "Partition must contain data.libsvm.gz"
    assert os.path.isfile(header_file), "Partition must contain header.libsvm.gz"

    with gzip.open(header_file, "r") as hfile:
        header_str = hfile.readlines()

    header = {}
    for elm in header_str:
        single = elm.decode().split("$")
        header[single[0]] = eval(single[1])

    datasize = 1
    for elm in header["datashape"]:
        datasize *= elm

    with gzip.open(data_file) as dfile:
        data, labels = sklearn.datasets.load_svmlight_file(dfile, n_features=datasize, dtype=np.float32,
                                                           zero_based=True)
    data = data.toarray()
    data = data.reshape((-1,) + header["datashape"])
    return data, labels


# def _dump_svmlight(X, f, one_based=False):
#     X_is_sp = int(hasattr(X, "tocsr"))
#
#     if X.dtype.kind == 'i':
#         value_pattern = "%d:%d"
#     else:
#         value_pattern = "%d:%.16g"
#
#     line_pattern = "%s\n"
#
#     for i in range(X.shape[0]):
#         if X_is_sp:
#             span = slice(X.indptr[i], X.indptr[i + 1])
#             row = zip(X.indices[span], X.data[span])
#         else:
#             nz = X[i] != 0
#             row = zip(np.where(nz)[0], X[i, nz])
#
#         s = " ".join(value_pattern % (j + one_based, x) for j, x in row)
#         f.write((line_pattern % s).encode('ascii'))


def create_directory(name):
    """
    Create a directory

    Parameters
    ----------
    name : str
        Directory name

    Returns
    -------
    str
        Path to the newly created direcotry
    """
    try:
        os.mkdir(name)
    except OSError:
        pass
    return name
