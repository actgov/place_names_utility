# Place Names

### place_names.return_centroid(in_table, out_csv)

This method calculates and returns the centre most point in a cluster
of points. This is required to find the centremost node of a polyline
which represents a road centreline. 

        in_table = r'<drive>:/<path>/intermediate.gdb/roads_to_find_centremost_point'
        out_csv  = r'<drive>:/<path>/centroids.csv'

        place_names.return_centroid(in_table, out_csv)

