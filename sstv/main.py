

import PIL.Image

from JotaJoti.sstv.helpers import combine
from encode import MartinM1 as m1
from decode import SSTVDecoder

image0 = PIL.Image.open('./original_images/logo2.png')
image1 = PIL.Image.open('./original_images/1.jpg')

m1(image0, 6900, 16).write_wav('./audio/audio0.wav')
m1(image1, 6900, 16).write_wav('./audio/audio1.wav')
audio0 = './audio/audio0.wav'
# audio = './audio/3.mp3'
audio = './audio/60.wav'
audio1 = './audio/audio1.wav'
combine(audio1, audio, 'combined')
combined = './audio/combined.wav'
img0 = SSTVDecoder(audio0).decode().save('./images/image0.png')
img = SSTVDecoder(combined).decode().save('./images/combined.png')
img1 = SSTVDecoder(audio1).decode().save('./images/image1.png')
print('done')
