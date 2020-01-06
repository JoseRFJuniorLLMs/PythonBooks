class Region:
    def __init__(self, coords, ref):
        self.coords = coords
        self.ref    = ref

    def inside(self, x, y):
        isSide = 0
        if self.coords[0][0] <= x <= self.coords[1][0] and \
           self.coords[0][1] <= y <= self.coords[1][1]:
            isSide = 1

        return isSide

class ImageMap:
    def __init__(self):
        self.regions = []
        self.cache   = {}

    def addRegion(self, coords, ref):
        self.regions.append(Region(coords, ref))

    def getRegion(self, x, y):
        try:
            return self.cache[(x,y)]
        except KeyError:
            for region in self.regions:
                if region.inside(x, y) == 1:
                    self.cache[(x,y)] = region
                    return region.ref
            return None

