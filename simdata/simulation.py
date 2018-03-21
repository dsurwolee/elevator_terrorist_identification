import numpy as np
import itertools
import csv

class ElevatorSim:
	"""
	"""

	def __init__(self, levels, capacity):
		self.levels = levels + 1
		self.capacity = capacity

	@staticmethod
	def timestamp_generator(M, D, Y, h, m, s):
		"""
		"""
		date = '/'.join(str(i) for i in [M, D, Y])
		time = ':'.join(str(i) for i in [h, m, s])
		return date + ' ' + time

	def passenger(self, id, day, work_hours=range(4,20)):
		"""
		""" 
		ptrip_list = []

		trip_count = np.random.randint(2,6)
		for c in range(trip_count):
			# Generate elevator id
			e_id = np.random.randint(1,5)
			# Generate time
			h = np.random.choice(work_hours)
			m, s = np.random.randint(0, 58, 2)
			# Generate floor in and floor out
			fin, fout = np.random.choice(list(range(1,self.levels)), 2, replace=False)
			diff_floor = abs(fin - fout)
			# Seconds per floor
			spf = round(np.random.normal(7,1.5))
			# Trip Duration
			d = diff_floor * spf 
			# Get Entered Time and Exit Time
			e = d + s
			m_out, s_out = (m + e // 60, e % 60) if e >= 60 \
											else (m, e)

			tin = self.timestamp_generator(5,day,2017,h,m,s)
			tout = self.timestamp_generator(5,day,2017,h,m_out,s_out)
			ptrip_list.append([id, e_id, tin, tout, fin, fout])

		return ptrip_list

	def simulate(self):
		"""
		"""
		id_list = list(range(300))
		day = []
		for i in range(1,32):
			count = int(np.random.normal(self.capacity-100,30))
			sample = np.random.choice(id_list, count).tolist()
			day += [self.passenger(v, i) for v in sample] 
		return list(itertools.chain.from_iterable(day))


if __name__ == '__main__':

	# Parameters
	FLOORS = 10
	PASSENGERS = 300 

	# Generate data
	sim = ElevatorSim(FLOORS, PASSENGERS)
	data = sim.simulate()

	# Output simulated date to csv file
	with open ('simdata.csv', 'w') as csvfile:
		record = csv.writer(csvfile, delimiter=',')
		record.writerow(['id','elevator','timein','timeout','floorin','floorout'])
		for d in data:
			record.writerow(d)