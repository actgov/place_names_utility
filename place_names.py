import arcpy
from collections import defaultdict

# Author: Aaron O'Hehir - ACTmapi Administrator
# Date: 17/09/2018

"""
This method calculates and returns the centre most point in a cluster
of points. This is required to find the centremost node of a polyline
which represents a road centreline. 

        in_table = r'<drive>:/<path>/intermediate.gdb/roads_to_find_centremost_point'
        out_csv  = r'<drive>:/<path>/centroids.csv'

        place_names.return_centroid(in_table, out_csv)

"""

def return_centroid(in_table,out_csv):
    field_names = ['FN_ID', 'SHAPE']

    # Create Cursor object to iterate over point features using the 'FN_ID' 
    # fields as cursor. 
    cursor = arcpy.da.SearchCursor(in_table, field_names)

    # Create a dict and append co-ordinate values of a 
    # cluster against FN_ID number.
    points_dict = defaultdict(list)
    for row in cursor:
        # Feature name ID
        FN_ID = str(int(row[0]))
        # Co-orindate tuple i.e. (680845.2802999998, 6042263.1732)
        points_dict[FN_ID].append(row[1])

    # Add header to output csv
    output = 'FN_ID,X,Y,_xmin,_ymin,_xmax,_ymax\n'

    # Code works by calculating the centroid of the cluster,
    # then finds the point with X/Y values closest to the centroid. 
    for item in points_dict:
        # Check for cluster i.e. 2 or more points.
        if (len(points_dict[item]) > 2 or len(points_dict[item]) == 2):
            number_of_coords = len(points_dict[item])
            print("Number of coords: " + str(number_of_coords))
            # Variables to use in calculation.
            _xmin = 10000000000000
            _ymin = 10000000000000
            _xmax = 0
            _ymax = 0
            x = 0
            y = 0
            x_dist = 10000000000000
            y_dist = 10000000000000
            # Calculate the centroid and the bounding extent of the cluster. 
            for coord_pair in points_dict[item]:
                if coord_pair != None:
                    x_src = float(coord_pair[0])
                    y_src = float(coord_pair[1])
                    x += x_src
                    y += y_src
                if x_src < _xmin:
                    _xmin = x_src
                if y_src < _ymin:
                    _ymin = y_src
                if x_src > _xmax:
                    _xmax = x_src
                if y_src > _ymax:
                    _ymax = y_src
            print("sum of x: "+str(x))
            print("sum of y: "+str(y))
            x_centroid = x/number_of_coords
            y_centroid = y/number_of_coords
            print("x_centroid: "+str(x_centroid))
            print("y_centroid: "+str(y_centroid))
            x = 0
            y = 0
            # Calculate the point with the clostest distance to the cluster. 
            for coord_pair in points_dict[item]:
                if coord_pair != None:
                    x = float(coord_pair[0])
                    y = float(coord_pair[1])
                    x_dist_to_centroid = abs(x - x_centroid)
                    y_dist_to_centroid = abs(y - y_centroid)
                    if x_dist_to_centroid < x_dist and y_dist_to_centroid < y_dist:
                        x_dist = x_dist_to_centroid
                        y_dist = y_dist_to_centroid
                        result_coord_pair = coord_pair
            # Output centremost point and cluster extent. 
            output += item + ',' + str(result_coord_pair[0])   + \
                             ',' + str(result_coord_pair[1])   + \
                             ',' + str(_xmin) +','+ str(_ymin) + \
                             ',' + str(_xmax) +','+ str(_ymax) + '\n'
    # Write output to csv
    try:
        f = open(out_csv, 'r+')
    except IOError:
        f = open(out_csv, 'w')
    f.seek(0)
    f.write(output)
    f.truncate()
    f.close()

if __name__ == "__main__":
    try:
        return_centroid(in_table, out_csv)
    except Exception as e:
        sys.exit(1)
