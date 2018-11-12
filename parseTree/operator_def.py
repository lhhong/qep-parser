class Operator(object):
	def __init__(op_name, cost_estimate, description):
		# op_name in ['HashAggregate', 'Hash Join', 'Nested Loop', 'Index Scan', 'Hash', 'Seq Scan']
		# cost_estimate is a string, eg cost=2936.20..2937.73 rows=41 width=16
		# description is just a description for now
		self.op_name = op_name
		self.description = description
		parseCost(cost_estimate)

	def parseCost(cost_estimate):
		parts = cost_estimate.split(' ')
		costs = parseHeader(parts[0], header='cost=')
		min_cost, max_cost = costs.split('..')
		rows = parseHeader(parts[1], header='rows=')

		self.est_min_cost = float(min_cost)
		self.est_max_cost = float(max_cost)
		self.rows = int(rows)

	def parseHeader(line, header):
		n = len(header)
		if line[:n] == header:
			return line[n:]
		return line

