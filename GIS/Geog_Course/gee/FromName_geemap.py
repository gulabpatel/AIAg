import ee 

# Display an image given its ID.

image = ee.Image('CGIAR/SRTM90_V4')
# Center the m.
m.setCenter(-110, 40, 5)
# Display the image.
m.addLayer(image, {'min': 0, 'max': 3000}, 'SRTM')
Map