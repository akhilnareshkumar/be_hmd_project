# Get the directions from https://maps.googleapis.com/maps/api/directions/json?origin=18.5553705,73.87762109999994&destination=18.5329493,73.87961700000005&key=API_KEY

import urllib
import json
import pyproj
import math
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D



# Fetching JSON directions and storing into a list


source = open('../json/current_location_map.json','r').read()
source = json.loads(source)
destination = open('../json/destination.json','r').read()
destination = json.loads(destination)

print "Source(Current location):", source[0], source[1]
print "Destination:", destination[0], destination[1]

target_url = "https://maps.googleapis.com/maps/api/directions/json?origin="+str(source[0])+","+str(source[1])+"&destination="+str(destination[0])+","+str(destination[1])+"+&key=AIzaSyBpmgg9nlSd1RtvmlGlr-626SGlzVw1UiY"
print "Fetching directions from source to destination..."
json_data = urllib.urlopen(target_url).read()


# json_data = open('json/maps/hometowadia.json').read()
# json_data = open('json/maps/dorabjeetoairport.json').read()

data = json.loads(json_data)

lat = []
lng = []

lat.append(data['routes'][0]['legs'][0]['steps'][0]['start_location']['lat'])
lng.append(data['routes'][0]['legs'][0]['steps'][0]['start_location']['lng'])

for x in data['routes'][0]['legs'][0]['steps']:
	lat.append(x['end_location']['lat']),
	lng.append(x['end_location']['lng'])




# Converting Map coordinates to x and y coordinates

x_coord = lat
y_coord = lng

print 'The map coordinates from source to destination'
for x in range(len(lat)):
	print lat[x], lng[x]
print

p1 = pyproj.Proj(init='epsg:24047')
x_coord,y_coord = p1(lng,lat)

print 'The x and y coordinates from the source to destination'
for i in range(len(lat)):
	print x_coord[i], y_coord[i]
print




# Make source the origin

x_init = x_coord[0]
y_init = y_coord[0]

init_points_file = open('../json/initial.json', 'w')
init_points_file.write("["+str(x_init)+","+str(y_init)+"]")
init_points_file.close()

for i in range(len(x_coord)):
	x_coord[i] -= x_init
	y_coord[i] -= y_init




# Rotate the map according to the first path

theta = math.atan2(x_coord[1]-x_coord[0],y_coord[1]-y_coord[0])
cos = math.cos(theta)
sin = math.sin(theta)

x_coord_new = []
y_coord_new = []

for i in range(len(x_coord)):
	x_coord_new.append(0)
	y_coord_new.append(0)

for i in range(len(x_coord)):
	x_coord_new[i] = (x_coord[i]*cos) - (y_coord[i]*sin)
	y_coord_new[i] = (y_coord[i]*cos) + (x_coord[i]*sin)

print 'New x and y coordinates after rotation'
for i in range(len(lat)):
	print x_coord_new[i], y_coord_new[i]
print


z_coord_new = []
for i in range(len(x_coord_new)):
	z_coord_new.append(0)





# Write the output to overlay file

outputfile = open('../json/overlay.json', 'w')
outputfile.write(json.dumps([x_coord_new,y_coord_new,z_coord_new]))
outputfile.close()




# Print the map

# 3D

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot(x_coord_new, y_coord_new, z_coord_new, label='Source to Destination')
# plt.axis('equal')
# ax.legend()

# plt.show()



# 2D

# plt.plot(x_coord_new,y_coord_new)
# plt.show()
