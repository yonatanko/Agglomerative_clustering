from cluster import Cluster
from link import SingleLink, CompleteLink


class AgglomerativeClustering:
    def __init__(self, link, samples, dist_dictionary):
        """
        initializing the algorithm
        :param link: current method of computing distance of two clusters
        :param samples: list of all samples in dataset
        :param dist_dictionary: distances dictionary
        """
        self.link = link
        self.clusters = []
        self.list_of_samples = samples
        self.dist_dictionary = dist_dictionary
        for sample in samples:
            self.clusters.append(Cluster(sample.s_id,[sample]))

    def compute_silhoeutte(self):
        """
        building dictionary of the silhoeutte value for each point
        :return: dictionary, with samples ids as keys and the sample's silhoeutte as value
        """
        dictionary_of_samples = {}
        for cluster in self.clusters:
            for sample in cluster.samples:
                if len(cluster.samples) > 1:
                    in_sample = in_of_sample(cluster, sample, self.dist_dictionary)
                    out_sample = out_of_sample(self.clusters, cluster, sample, self.dist_dictionary)
                    dictionary_of_samples[sample.s_id] = (out_sample-in_sample)/(max(in_sample, out_sample))
                else:
                    dictionary_of_samples[sample.s_id] = 0
        return dictionary_of_samples

    def compute_summery_silhoeutte(self,dictionary_of_samples):
        """
        building dictionary of the silhoeutte value for each cluster
        :param dictionary_of_samples: dictionary, with samples ids as keys and the sample's silhoeutte as value
        :return: dictionary, with clusters ids as keys and their silhoeutte as value
        """
        dictionary_of_clusters = {}
        for cluster in self.clusters:
            dictionary_of_clusters[cluster.c_id] = s_of_cluster(cluster, dictionary_of_samples)
        s_dataset = sum(dictionary_of_samples.values()) / len(dictionary_of_samples.keys())
        dictionary_of_clusters["0"] = s_dataset
        return dictionary_of_clusters

    def compute_rand_index(self):
        """
        computation of the rand index for the whole dataset by the algorithm
        a measure of how well the algorithm worked
        :return: rand index of the whole dataset
        """
        tp = 0
        tn = 0
        length = len(self.list_of_samples)
        ncr_of_length_and_couples = length*(length-1)/2
        for i in range(length):
            for j in range(i+1,length,1):
                sample = self.list_of_samples[i]
                other_sample = self.list_of_samples[j]
                clusters = find_clusters(sample,other_sample,self.clusters)
                if sample.label == other_sample.label and clusters[0].c_id == clusters[1].c_id:
                    tp += 1
                if sample.label != other_sample.label and clusters[0].c_id != clusters[1].c_id:
                    tn += 1
        return (tp + tn)/ncr_of_length_and_couples

    def run(self, max_clusters):
        """
        the function that runs the whole algorithm
        each itteration, the algorithm merges the two most near clusters
        it runs until we have the wanted number of cluster, which is the max_clusters
        :param max_clusters: number of clusters we want to have at the end of the clustring
        """
        while len(self.clusters) > max_clusters:
            nearest = find_nearest_clusters(self.clusters, self.link, self.dist_dictionary)
            first_id = nearest[0]
            second_id = nearest[1]
            first_index = find_index_in_list(first_id, self.clusters)
            second_index = find_index_in_list(second_id, self.clusters)
            self.clusters[first_index].merge(self.clusters[second_index], self.clusters)

        dictionary_of_samples = self.compute_silhoeutte()
        dictionary_of_clusters = self.compute_summery_silhoeutte(dictionary_of_samples)

        for cluster in self.clusters:
            cluster.print_details(dictionary_of_clusters[cluster.c_id])
        print_details_of_dataset(dictionary_of_clusters["0"], self.compute_rand_index())


def in_of_sample(cluster, original_sample, dist_dict):
    """
    computing the in measure of the sample in the cluster
    :param cluster: cluster object
    :param original_sample: the sample we compute her in measure
    :param dist_dict: distances dictionary
    :return: in value of the sample
    """
    cluster_size = len(cluster.samples)
    sum_distances = 0
    for current_sample in cluster.samples:
        if current_sample.s_id != original_sample.s_id:
            key_tuple = tuple(sorted((original_sample.s_id, current_sample.s_id)))
            sum_distances += dist_dict[key_tuple]
    return sum_distances/(cluster_size-1)


def out_of_sample(list_of_clusters, current_cluster, original_sample, dist_dict):
    """
    computing the out measure of the sample in the cluster
    :param list_of_clusters: list of all clusters in current itteration
    :param current_cluster: cluster object, the cluster of the current check sample
    :param original_sample: sample object, the one we compute it's out measure
    :param dist_dict: distances dictionary
    :return: out value of the sample
    """
    list_of_all_distances = []
    for cluster in list_of_clusters:
        sum_distances = 0
        if cluster.c_id != current_cluster.c_id:
            for outer_sample in cluster.samples:
                key_tuple = tuple(sorted((original_sample.s_id, outer_sample.s_id)))
                sum_distances += dist_dict[key_tuple]
            list_of_all_distances.append(sum_distances/len(cluster.samples))
    return min(list_of_all_distances)


def s_of_cluster(cluster, dictionary_of_samples):
    """
    computing the silhoeutte value of the cluster
    :param cluster: cluster object, the one we compute for
    :param dictionary_of_samples: dictionary, with sample ids as keys and their silhoeutte as value
    :return: silhoeutte of the cluster
    """
    sum_s_of_samples_in_cluster = 0
    cluster_size = len(cluster.samples)
    for sample in cluster.samples:
        sum_s_of_samples_in_cluster += dictionary_of_samples[sample.s_id]
    return sum_s_of_samples_in_cluster/cluster_size


def print_details_of_dataset(silhouette, rand_index):
    """
    printing details of the dataset
    :param silhouette: silhoeutte of the dataset
    :param rand_index: the rand index of the dataset
    """
    print("whole data:", end=" ")
    print("silhouette = " + str(round(silhouette,3)), end=", ")
    print("RI = " + str(round(rand_index,3)), end="")


def find_clusters(sample,other_sample, list_of_clusters):
    """
    finding the clusters of two given samples
    :param sample: sample object
    :param other_sample: sample object
    :param list_of_clusters: list of all clusters in current iteration
    :return: list of two clusters
    """
    clusters = [0,0]
    for cluster in list_of_clusters:
        if sample in cluster.samples:
            clusters[0] = cluster
        if other_sample in cluster.samples:
            clusters[1] = cluster
    return clusters


def find_nearest_clusters(list_of_all_clusters, method, dist_dict):
    """
    finding two nearest clusters
    :param list_of_all_clusters: list of all clusters in the current iteration
    :param method: method of clusters distance computation
    :param dist_dict: distances dictionary
    :return: list with two nearest clusters ids
    """
    if method.__name__ == "CompleteLink":
        method = CompleteLink()
    else:
        method = SingleLink()
    cluster_1_id = list_of_all_clusters[0].c_id
    cluster_2_id = list_of_all_clusters[1].c_id
    min_dist = method.compute(list_of_all_clusters[0], list_of_all_clusters[1], dist_dict)
    for cluster in list_of_all_clusters:
        for other_cluster in list_of_all_clusters:
            if cluster.c_id != other_cluster.c_id:
                dist = method.compute(cluster, other_cluster, dist_dict)
                if dist < min_dist:
                    cluster_1_id = cluster.c_id
                    cluster_2_id = other_cluster.c_id
                    min_dist = dist
    return [cluster_1_id, cluster_2_id]


def find_index_in_list(id, list_of_clusters):
    """
    finding the index of the cluster in the list of all clusters, by it's id
    :param id: clustr id
    :param list_of_clusters: list of all clusters in the current iteration
    :return: index of the cluster in the list of clusters
    """
    for i in range(len(list_of_clusters)):
        if list_of_clusters[i].c_id == id:
            return i