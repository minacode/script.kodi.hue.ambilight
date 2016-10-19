from typing import List
from HSVRatio import HSVRatio


class Screenshot:
  
    def __init__(self, pixels, capture_width, capture_height):
          
        self.pixels = pixels
        self.capture_width  = capture_width
        self.capture_height = capture_height


    def most_used_spectrum(
        self, 
        spectrum      : List[int], 
        saturation    : int, 
        value         : int, 
        size          : int, 
        overall_value : int
    ) -> List[HSVRatio]:
      
        # color bias/groups 6 - 36 in steps of 3
        colorGroups = settings.color_bias
        if  colorGroups == 0:
            colorGroups = 1
        colorHueRatio = 360 / colorGroups
    
        hsvRatios = []
        hsvRatiosDict = {}
    
        for i in range(360):
            if spectrum.has_key(i):
                # shift index to the right so that groups are centered on primary and secondary colors
                colorIndex = int( ( (i + colorHueRatio / 2) % 360) / colorHueRatio )
                pixelCount = spectrum[i]
        
                if hsvRatiosDict.has_key(colorIndex):
                    hsvr = hsvRatiosDict[colorIndex]
                    hsvr.average( i / 360.0, saturation[i], value[i])
                    hsvr.ratio = hsvr.ratio + pixelCount / float(size)
        
                else:
                    hsvr = HSVRatio( i / 360.0, saturation[i], value[i], pixelCount / float(size))
                    hsvRatiosDict[colorIndex] = hsvr
                    hsvRatios.append(hsvr)
    
        colorCount = len(hsvRatios)
        if colorCount > 1:
            # sort colors by popularity
            hsvRatios.sort(key = lambda hsvratio: hsvratio.ratio, reverse = True)
            # logger.debuglog('hsvRatios %s' % hsvRatios)
            
            # return at least 3
            if colorCount == 2:
                hsvRatios.insert(0, hsvRatios[0])
            
            for j in range(3):
                hsvRatios[j].averageValue(overall_value)
            return hsvRatios
    
        elif colorCount == 1:
            hsvRatios[0].averageValue(overall_value)
            return [hsvRatios[0]] * 3
    
        else:
            return [HSVRatio()] * 3


    def spectrum_hsv(self, pixels: List[int], width: int, height: int) -> List[HSVRatio]:
            
        spectrum   = {}
        saturation = {}
        value      = {}
        
        size = int( len(pixels) / 4 )
        
        s = 0 
        v = 0
        
        for i in range(0, size, 4):
            if fmtRGBA:
                r = pixels[i]
                g = pixels[i + 1]
                b = pixels[i + 2]
            else: # probably BGRA
                b = pixels[i]
                g = pixels[i + 1]
                r = pixels[i + 2]
      
            tmph, tmps, tmpv = colorsys.rgb_to_hsv(float(r / 255.0), float(g / 255.0), float(b / 255.0))
            s += tmps
            v += tmpv
      
            # skip low value and saturation
            if tmpv > 0.25 and tmps > 0.33:
                h = int(tmph * 360)
        
                # logger.debuglog('%s \t set pixel r %s \tg %s \tb %s' % (i, r, g, b))
                # logger.debuglog('%s \t set pixel h %s \ts %s \tv %s' % (i, tmph*100, tmps*100, tmpv*100))
        
                if spectrum.has_key(h):
                    spectrum[h]  += 1 # tmps * 2 * tmpv
                    saturation[h] = (saturation[h] + tmps) / 2
                    value[h]      = (value[h]      + tmpv) / 2
                else:
                    spectrum[h]   = 1 # tmps * 2 * tmpv
                    saturation[h] = tmps
                    value[h]      = tmpv
    
        overall_value = v / float(size)
        # s_overall = int(s * 100 / i)
        return self.most_used_spectrum(spectrum, saturation, value, size, overall_value)
  
