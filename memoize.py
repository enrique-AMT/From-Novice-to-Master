def Memoize(fn):
    di = dict()

    def wrapper(x):
        
        if fn not in di:
            di[x]= fn(x)
            
        return di[fn]

    return wrapper
