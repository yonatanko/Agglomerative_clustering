class Cluster:
    def __init__(self, c_id, samples):
        """
        initializing the Cluster object
        :param c_id: clusters id (minimal id of it's samples)
        :param samples: list of it's samples (list of Sample object)
        """
        self.c_id = c_id
        self.samples = samples
        self.dominant_label = ""

    def merge(self, other, origin_list):
        """
        merging two clusters into one and deleating the other from the list and from the memory
        :param other: other cluster
        :param origin_list: the list of all clusters in the dataset
        """
        self.c_id = min(self.c_id, other.c_id)
        self.samples = self.samples + other.samples
        self.samples.sort(key = lambda x: x.s_id)
        origin_list.remove(other)
        del other

    def print_details(self, silhouette):
        """
        printing cluster's information
        :param silhouette: the silhouette measure of the cluster
        """
        print("Cluster " + str(self.c_id) + ":", end=" ")
        print(sorted([self.samples[i].s_id for i in range(len(self.samples))]), end=", ")
        list_of_lables = create_list_of_labels(self.samples)
        self.dominant_label = calculate_dominant_label(list_of_lables)
        print("dominant label = " + self.dominant_label, end=", ")
        print("silhouette = " + str(round(silhouette,3)), end="")
        print()


def create_list_of_labels(samples):
    """
    creating list of lables of the cluster's Samples
    :param samples: list of the clusters samples
    :return: list of the samples labels
    """
    list_of_lables = []
    for sample in samples:
        list_of_lables.append(sample.label)
    return list_of_lables


def calculate_dominant_label(list_of_lables):
    """
    calculating the dominant lable of the cluster
    :param list_of_lables: list of the clusters lables
    :return: most common label in the cluster
    """
    set_of_lables = set(list_of_lables)
    list_of_appearances = []
    for label in set_of_lables:
        list_of_appearances.append([label, list_of_lables.count(label)])
    sorted_lables = sorted(list_of_appearances, key= lambda x : x[1], reverse= True)
    return find_max_by_lex_and_count(sorted_lables)


def find_max_by_lex_and_count(sorted_list):
    """
    if there are couple lables that are the most common in the cluster, we return the label
    that appears first by lexicographical order
    :param sorted_list: sorted list of lables
    :return: the label that appeared the most and appears first by lexicographical order
    """
    maximum = sorted_list[0][0]
    count = sorted_list[0][1]
    for i in range(len(sorted_list)):
        if sorted_list[i][1] == count and sorted_list[i][0] < maximum:
            print(sorted_list[i][0], maximum)
            maximum = sorted_list[i][0]
            count = sorted_list[i][1]
        if sorted_list[i][1] < count:
            return maximum
    return maximum

