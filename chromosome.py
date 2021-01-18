class Chromosome:

    def __init__(self, genes:list):
        self.genes = genes

    def getGenes(self):
        geneNames = []
        for i in range(len(self.genes)):
            geneNames.append(self.genes[i].name)
        return geneNames
    
    def sumCost(self):
        sum = 0
        for i in range(len(self.genes)):
            sum += self.genes[i].cost
        return sum
    
    def sumDuration(self):
        sum = 0
        for i in range(len(self.genes)):
            sum += self.genes[i].duration
        return sum

    def avgNoPeople(self):
        avg = 0
        for i in range(len(self.genes)):
            avg += self.genes[i].npeople
        return avg/(len(self.genes))

    def haveDuplicates(self):
        dupes = len(self.genes) - len(set(self.genes))
        if dupes == 0:
            return 0
        else:
            return dupes