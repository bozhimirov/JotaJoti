from JotaJoti.sstv.constants import M1


def byte_to_freq(value):
    return M1.FREQ_BLACK + M1.FREQ_RANGE * value / 255


def calc_lum(freq):
    """Converts SSTV pixel frequency range into 0-255 luminance byte"""

    lum = int(round((freq - 1500) / 3.1372549))
    return min(max(lum, 0), 255)


def barycentric_peak_interp(bins, x):
    """Interpolate between frequency bins to find x value of peak"""

    # Takes x as the index of the largest bin and interpolates the
    # x value of the peak using neighbours in the bins array

    # Make sure data is in bounds
    y1 = bins[x] if x <= 0 else bins[x - 1]
    y3 = bins[x] if x + 1 >= len(bins) else bins[x + 1]

    denom = y3 + bins[x] + y1
    if denom == 0:
        return 0

    return (y3 - y1) / denom + x
