from sys import argv
from data import Data
from link import CompleteLink, SingleLink
from agglomerative_clustering import AgglomerativeClustering


def main(argv):
    """
    main function
    :param argv: path of file
    """
    dataset = Data(argv[1])
    list_of_samples = dataset.create_sample()
    dist_dictionary = build_distance_dictionary(list_of_samples)
    print("single link:")
    runner = AgglomerativeClustering(SingleLink, list_of_samples, dist_dictionary)
    runner.run(7)
    print()
    print("complete link:")
    runner_2 = AgglomerativeClustering(CompleteLink, list_of_samples, dist_dictionary)
    runner_2.run(7)


def build_distance_dictionary(list_of_samples):
    """
    building the distance dictionary
    each key is a tuple of 2 samples ids, and it's value is the euclidean distance between them
    :param list_of_samples: all the samples in the dataset
    :return: distances dictionary
    """
    dist_dictionary = {}
    #by running like that, we dont run over the same couple twice
    for i in range(len(list_of_samples)):
        for j in range(i+1,len(list_of_samples)):
            if list_of_samples[i].s_id != list_of_samples[j].s_id:
                distance = list_of_samples[i].compute_euclidean_distance(list_of_samples[j])
                key_tuple = tuple(sorted((list_of_samples[i].s_id, list_of_samples[j].s_id)))
                dist_dictionary[key_tuple] = distance
    return dist_dictionary


if __name__ == '__main__':
    main(argv)