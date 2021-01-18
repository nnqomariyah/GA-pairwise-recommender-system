class Destination:
    
    def __init__(self, name, cost, category, duration, tags=[]):
        self.name = name.replace(',', '')
        self.cost = int(cost)
        self.category = category
        self.duration = float(duration)
        self.tags = tags
        # self.npeople = int(npeople)

