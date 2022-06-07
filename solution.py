import numpy as np

class Polymino:
	def __init__(self, h, w):
		self.arr = np.ones((h, w), dtype=int)
		self.s = h*w

	def rotate(self):
		self.arr = np.rot90(self.arr)


class L_Polymino(Polymino):
	def __init__(self, h, w):
		super().__init__(h, w)
		self.arr = np.array([1 if x < w or x % w == 0 else 0 for x in range(h * w)]).reshape(h, w)
		self.s = h+w-1

class Table:
	def __init__(self, H, W):
		self.M = H
		self.N = W
		self.arr = np.zeros((self.M, self.N), dtype=int)
		self.filled_poly_coord = []


	def push_polymino(self, poly, cord):

		# poly - object type of Polymino(L_Polymin0)
		# cord - tuple (x, y) size of 2

		self.arr[cord[0]:cord[0]+poly.arr.shape[0], cord[1]:cord[1]+poly.arr.shape[1]] += poly.arr

	def pop_polymino(self, poly, cord):
		self.arr[cord[0]:cord[0]+poly.arr.shape[0], cord[1]:cord[1]+poly.arr.shape[1]] -= poly.arr

	def position_free(self, poly, cord):
		return np.all(np.add(self.arr[cord[0]:cord[0]+poly.arr.shape[0], cord[1]:cord[1]+poly.arr.shape[1]], poly.arr) < 2)

	def place_generation(self, poly):
		rot_num = 4 if isinstance(poly, L_Polymino) else 2
		for _ in range(rot_num):
			for i in range(self.M - poly.arr.shape[0] + 1):
				for j in range(self.N - poly.arr.shape[1] + 1):
					cord = (i,j)
					if self.position_free(poly, cord):
						self.push_polymino(poly, cord)
						self.filled_poly_coord.append(cord)
						yield True
			poly.rotate()
		yield False			
		
	def filling(self, polyminos):
		#initial check of the filling condition
		S = 0
		for poly in polyminos:
			if np.max(poly.arr.shape) > max(self.M, self.N) or np.min(poly.arr.shape) > min(self.M, self.N):
				return False
			S += poly.s
		if S > self.M * self.N:
			return False

		#solver
		cond = [self.place_generation(poly) for poly in polyminos]
		d = 0
		while 0 <= d < len(polyminos):
			#print(self.arr)
			if next(cond[d]):
				d += 1
			else:
				if d == 0:
					break
				self.pop_polymino(polyminos[d-1], self.filled_poly_coord[-1])
				self.filled_poly_coord.pop()
				cond[d] = self.place_generation(polyminos[d])
				d -= 1

		if d == len(polyminos):
			return True
		else:
			return False


if __name__ == '__main__':
	polyminos = []
	with open('input.txt') as f:
		M1, M2 = f.readline().split()					#Table size
		n1 = int(f.readline())							#number of unique rectangle-polymino shape
		for i in range(n1):
			n_pwr = int(f.readline())					#number of polymino with equal shape
			c1, c2 = f.readline().split()				#rectangle-polymino shape
			for j in range(n_pwr):
				p = Polymino(int(c1), int(c2))
				polyminos.append(p)

		n2 = int(f.readline())							#number of unique L-polymino shape
		for i in range(n2):
			n_pwr = int(f.readline())					#number of polymino with equal shape
			c1, c2 = f.readline().split()				#L-polymino shape
			for j in range(n_pwr):
				p = L_Polymino(int(c1), int(c2))
				polyminos.append(p)


	t = Table(int(M1), int(M2))
	print(t.filling(polyminos))