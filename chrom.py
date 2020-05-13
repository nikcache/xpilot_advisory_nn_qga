# Chromosome Class

class Chrom:

    def __init__(self, gene, id, port):
        self.gene = gene
        self.fitness = 0
        self.id = id
        self.port = port

    def getGene(self):
        return self.gene

    def getFit(self):
        return self.fitness
    
    def getID(self):
        return self.id

    def getPort(self):
        return self.port

    def getPair(self):
        return [self.id, self.gene, self.fitness]

    def setFit(self, fit):
        self.fitness = fit
    
    def setGene(self, gene):
        self.gene = gene

    def __str__(self):
        return str(self.gene)

def test():
    t = Chrom([0,0,0,0,0,0])
    t.setFit(99)
    print(t.getPair())

if __name__ == '__main__':
    test()