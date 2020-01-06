"""
Functions to compute color shadows, light and dark.
"""

__author__='doughellmann@mindspring.com'

def checkRGBRange(value, maxBits=16):
	minval=0
	maxval=pow(2, maxBits) - 1
	#print '\t %d = %04x => ' % (value, value),
	if value < minval:
		newval = minval
	elif value > maxval:
		newval = maxval
	else:
		newval = value
	#print '%04x = %d' % (newval, newval)
	return newval

def computeColorTriplet(widget, baseColor):
	#print 'computing colors for %s' % baseColor
	baseColorRGB = widget.winfo_rgb(baseColor)
	baseColorHex = '#%04x%04x%04x' % baseColorRGB
	lightColorRGB = (checkRGBRange(baseColorRGB[0] * 1.2),
			checkRGBRange(baseColorRGB[1] * 1.2),
			checkRGBRange(baseColorRGB[2] * 1.2))
	lightColor = '#%04x%04x%04x' % lightColorRGB
	darkColorRGB = (checkRGBRange(baseColorRGB[0] * 0.6),
			checkRGBRange(baseColorRGB[1] * 0.6),
			checkRGBRange(baseColorRGB[2] * 0.6))
	darkColor = '#%04x%04x%04x' % darkColorRGB
	triplet = (baseColorHex, lightColor, darkColor)
	#print triplet
	return triplet

