class a:
    a = str
    def __init__(self, z,x) -> None:
        self.z = z
        self.x = x
    
    def vip(self, a, b):
        self.x = a+b
        self.z = a-b

    @classmethod
    def xyz(cls, a):
        return cls(
        a,
       a+1
        )

A = a(1,2)

A.vip(12,12)
A=a.xyz(233)
print(A.x, A.z)