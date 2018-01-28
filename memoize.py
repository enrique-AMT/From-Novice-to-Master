def Memoize(fn , *args=None, **kwargs=None):
    di = dict()

    def wrapper():
        
        if fn not in di:
            di[fn]= fn(args,kwargs)
        else:
            return di[fn]

    return wrapper()
