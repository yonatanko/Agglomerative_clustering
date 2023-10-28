class Sample:
    def __init__(self, s_id, genes, label):
        """
        initializing the Sample object
        :param s_id: id of sample
        :param genes: list of genes values
        :param label: label of the sample
        """
        self.s_id = s_id
        self.genes = genes
        self.label = label

    def compute_euclidean_distance(self, other):
        """
        computing distance of 2 points by the euclidian measure
        :param other: other sample
        :return: euclidean distance of 2 points
        """
        sum_squared = 0
        for j in range(len(self.genes)):
            sum_squared += (self.genes[j]-other.genes[j])**2
        return sum_squared**0.5
