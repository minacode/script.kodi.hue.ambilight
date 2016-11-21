from HSVRatio import HSVRatio
from Constants import HUE_INTERVAL_COUNT


class Screenshot:

    def __init__(self, pixels, width, height):

        self.pixels = pixels
        self.width  = width
        self.height = height

    # broken
    def most_used_spectrum(self, spectrum, saturation, value, size, overall_value):

        # color bias/groups 6 - 36 in steps of 3
        color_groups = settings.color_bias
        if  color_groups < 1:
            color_groups = 1
        color_hue_ratio = HUE_INTERVAL_COUNT / color_groups

        hsv_ratios = {}

        for i in range(HUE_INTERVAL_COUNT):
            if spectrum.has_key(i):
                # shift index to the right so that groups are centered on primary and secondary colors
                color_hue_index = int(
                    (
                      (i + color_hue_ratio / 2) % HUE_INTERVAL_COUNT
                    ) / color_hue_ratio
                )
                pixel_count = spectrum[i]

                if hsv_ratios.has_key(color_hue_index):
                    hsvr = hsv_ratios[color_hue_index]
                    hsvr.average( i / HUE_INTERVAL_COUNT, saturation[i], value[i])
                    hsvr.ratio = hsvr.ratio + pixel_count / size

                else:
                    hsvr = HSVRatio( i / HUE_INTERVAL_COUNT, saturation[i], value[i], pixel_count / size)
                    hsv_ratios[color_hue_index] = hsvr

        hsv_ratios = hsv_ratios.keys()
        # sort colors by popularity
        hsv_ratios.sort(key = lambda hsvratio: hsvratio.ratio, reverse = True)
        # logger.debuglog('hsv_ratios %s' % hsv_ratios)

        return [ratio.average_value(overall_value) for ratio in hsv_ratios.keys()]


    def spectrum_hsv(self, pixels, width, height):

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
