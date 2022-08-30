import random
class Random:
    MBIG = 2147483647
    MSEED = 161803398
    Int32_min = -2147483648
    Int32_max = 2147483647
    def rand(self):
        self.times+=1
        return self.InternalSample() * (1.0 / self.MBIG)
    def InternalSample(self):
        locINext = self.inext
        locINextp = self.inextp
        locINext+=1
        if locINext >= 56 :locINext = 1
        locINextp+=1
        if locINextp >= 56: locINextp = 1
        retVal = ( self.SeedArray[locINext] - self.SeedArray[locINextp] ) | 0
        if retVal == self.MBIG: retVal-=1
        if retVal < 0: retVal = ( retVal + self.MBIG ) | 0
        self.SeedArray[locINext] = retVal
        self.inext = locINext
        self.inextp = locINextp
        return retVal
    def _init(self):
        subtraction =self.Int32_max if self.seed == self.Int32_min else abs(self.seed)
        mj = ( self.MSEED - subtraction ) | 0
        self.SeedArray = [0 for i in range(56)]
        self.SeedArray[55] = mj
        mk=1
        for i in range(1,55):
            ii=(21*i)%55
            self.SeedArray[ii] = mk
            mk = ( mj - mk ) | 0
            if mk < 0: mk = ( mk + self.MBIG ) | 0
            mj = self.SeedArray[ii]
        for k in range(1,5):
            for i in range(1,56):
                self.SeedArray[i] = ( self.SeedArray[i] - self.SeedArray[1 + (i + 30) % 55] ) | 0
                if (self.SeedArray[i] < 0): self.SeedArray[i] = ( self.SeedArray[i] + self.MBIG ) | 0
        self.inext=0
        self.inextp=21
    def __init__(self,seed):
        self.seed=seed
        self.times=0
        self._init()
seed=random.randint(-2**31,2**31-1)
r=Random(seed)
print(seed,r.rand())