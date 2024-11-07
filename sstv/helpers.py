from pydub import AudioSegment

# AudioSegment.converter = "C:\\Users\\stani\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffmpeg = "C:\\Users\\stani\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffprobe = "C:\\Users\\stani\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffprobe.exe"

from JotaJoti.sstv.constants import M1


def byte_to_freq(value):
    """Converts byte to frequency"""
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


def normalize(audio, arg):
    """Modify value of the audio file"""
    ext = audio.split('.')[-1]
    sound = AudioSegment.from_file(audio, format=ext)
    while sound.dBFS < -arg:
        sound += 1
    return sound


def combine(audio1, audio2, name):
    """Combine two audio files"""
    sound1 = normalize(audio1, 5)
    sound = normalize(audio2, 10)

    if len(sound1) > len(sound):
        overlay = sound1.overlay(sound, position=0)
    else:
        overlay = sound.overlay(sound1, position=0)

    overlay.export(f"./audio/{name}.wav", format="wav")
