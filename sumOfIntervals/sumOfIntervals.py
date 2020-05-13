class Span:

    def __init__(self, range, generation = 0):
        self.min, self.max = range
        self.generation = generation
        self.length = self.max - self.min

    def isOverlap(self, otherSpan):
        if self.min <= otherSpan.min <= self.max:
            return True
        if self.min <= otherSpan.max <= self.max:
            return True
        if otherSpan.min <= self.min <= otherSpan.max:
            return True
        if otherSpan.min <= self.max <= otherSpan.max:
            return True

        return False

    def getOverlappedSpan(self, other):
        return Span([min(self.min, other.min), max(self.max, other.max)], max(self.generation, other.generation) + 1)

    def __eq__(self, other) :
        return self.min == other.min and self.max == other.max

    def __lt__(self, other):
        if self.min < other.min:
            return True
        return False
            

def sum_of_intervals(intervals):
    
    spans = [Span(x) for x in intervals]
    result = sorted(spans)
    g = input("hello")
    


sum_of_intervals([[1,5],[10, 20],[1, 6],[16, 19],[5, 11]])
