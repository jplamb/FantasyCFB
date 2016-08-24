from random import randint
import datetime

print ''
print 'Today is: '
print('{:%b %d, %Y}'.format(datetime.date.today()))
print('{:%H:%M:%S}').format(datetime.datetime.now())
print ''
print ''
print 'Randomly generating draft order... '
print ''

players = {1: 'John L',
			2: 'John B',
			3: 'Jack',
			4: 'Mike',
			5: 'Scott'}

freq = [0,0,0,0,0]
y = 0
limit = 1000

print limit, ' draft orders will be generated. Final draft order is selected '
print 'based on each person''s lowest overall position'
print ''

while y < limit:
	pick_order = []

	while len(pick_order) < len(players):
		numb = randint(1,len(players))
		if numb not in pick_order:
			pick_order.append(numb)

	for x in range(0, len(pick_order)):
		freq[pick_order[x]-1] += x

	y += 1

freq_name = {freq[0]: 'John L'
			, freq[1]: 'John B'
			, freq[2]: 'Jack'
			, freq[3]: 'Mike'
			, freq[4]: 'Scott'}

print 'Raw pick order frequencies (lower number indicates higher pick order): '
print freq_name
print ''
freq.sort()

print 'Offical draft order is: '
print ''

for x in range(0, len(pick_order)):
	print x+1, '. ', freq_name[freq[x]]
	
print ''