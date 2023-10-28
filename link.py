import sys
class Link:
    def compute(self, cluster, other, dist_dict):
        """
        abstract method
        :param cluster: cluster object
        :param other: cluster object
        :param dist_dict: distances dictionary
        """
        raise NotImplementedError("Implement this method!")


class SingleLink(Link):
    def compute(self, cluster, other, dist_dict):
        """
        computing distance of two clusters by Single Link measure
        :param cluster: cluster object
        :param other: cluster object
        :param dist_dict: distances dictionary
        :return: distance between two most close points in the two inputted clusters
        """
        minimum = sys.maxsize
        for sample in cluster.samples:
            for other_sample in other.samples:
                key_tuple = tuple(sorted((sample.s_id, other_sample.s_id)))
                current_dist = dist_dict[key_tuple]
                if current_dist < minimum:
                    minimum = current_dist
        return minimum


class CompleteLink(Link):
    def compute(self, cluster, other, dist_dict):
        """
        computing distance of two clusters by Complete Link measure
        :param cluster: cluster object
        :param other: cluster object
        :param dist_dict: distances dictionary
        :return: distance between two most far points in the two inputted clusters
        """
        maximum = 0
        for sample in cluster.samples:
            for other_sample in other.samples:
                key_tuple = tuple(sorted((sample.s_id, other_sample.s_id)))
                current_dist = dist_dict[key_tuple]
                if current_dist > maximum:
                    maximum = current_dist
        return maximum


