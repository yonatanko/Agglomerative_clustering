import pandas
from sample import Sample


class Data:
    def __init__(self, path):
        """
        building the class
        :param path: path of the csv file
        """
        df = pandas.read_csv(path, header=0)  # reading the csv file
        self.data = df.to_dict(orient="list")  # making dictionary out of csv data

    def create_sample(self):
        """
        creating a sample type of each id and it's related values
        :return: list of Sample objects
        """
        list_of_samples = []
        for i in range(len(self.data["samples"])):
            current_sample = Sample(self.data["samples"][i],access_list_of_genes(self.data, i), self.data["type"][i])
            list_of_samples.append(current_sample)
        return list_of_samples


def access_list_of_genes(dictionary, index):
    """
    creating the list of genes for each Sample
    :param dictionary: dictionary of the whole data
    :param index: index of the current sample in the samples id's list of the "samples" key in the dictionary
    :return: list of genes that belong to the sample
    """
    genes_list = []
    for key in dictionary.keys():
        if key != "samples" and key != "type":
            genes_list.append(dictionary[key][index])
    return genes_list
