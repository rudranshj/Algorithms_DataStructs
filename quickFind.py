class UnionFind:
	def __init__(self,sz):
		self.root = [i for i in range(sz)]

	def find(self,x):
		return self.root[x]

	def union(self,x,y):
		rootX = self.find(x)
		rootY = self.find(y)
		if rootX != rootY:
			for i in range(len(self.root)):
				if self.root[i]==rootY: self.root[i]=rootX

	def isConnected(self,x,y):
		return self.find(x)==self.find(y)

uf = UnionFind(10)
uf.union(1,2)
uf.union(6,7)
uf.union(3,8)
uf.union(3,2)
uf.union(8,9)
uf.isConnected(1,8)