class ProbMap:
    ''' Represents a probability calculator.
    
    Calculates probability of success using various methods
    '''
    def process(li):
        pass


class MultMap(ProbMap):
    ''' Multiplier probability mapper.
    
    Combines probabilities by computing a product across all probabilities.
    '''
    
    def process(self, li):
        result = 1.0
        for i in li:
            result *= li.get(i)
        return result
        
        
class MinMap(ProbMap):
    ''' Returns the smallest (numerically) number in the list
    
    Returns the smallest possibility
    '''
    
    def process(self, li):
        result = 1.0
        for i in li:
            if i < result:
                result = i
        return result


class MeanMap(ProbMap):
    ''' Uses the mean/average to ascertain probability
    
    Calculates the simple arithmetic mean of the list values.
    '''
    
    def process(self, li):
        result = 0.0
        for i in li:
            result += i
        return result/len(li)
        
        
#unit testing
def main():
    li = [0.5,0.25,0.3]
    print MultMap().process(li)
    print MinMap().process(li)
    print MeanMap().process(li)
    
if __name__ == "__main__":
    main()
