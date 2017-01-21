'''
This program takes a person standing in front of a green screen
and then removes the background and inserts a new one
'''
print __doc__

from SimpleCV import Camera, VirtualCamera,Color, Display, Image, pg

sleep_time = 2 #the amount of time to show each image for


cam = Camera(1)

vid = VirtualCamera('NuclearExplosion.mp4', 'video')
#vid = VirtualCamera('640x360_hurricane.mp4', 'video')
#vid = VirtualCamera('volcano.mp4', 'video')
#vid = VirtualCamera('Volcano2.mp4', 'video')
#vid = VirtualCamera('volcano_erupting.mp4', 'video')

#disp = Display(flags = pg.FULLSCREEN)
disp = Display()

while not disp.isDone():
    img = cam.getImage()
    img.flipHorizontal()
    sz = img.size()

    vid.getImage()
    vid.getImage()
    background = vid.getImage()
    #if vid.getFrameNumber() == 717:
    if not background:
        vid.rewind()
        background = vid.getImage()

    background = background.resize(sz[0], sz[1])

    bgcolor = img.getPixel(10,10)
    #print bgcolor
    #bgcolor = (10, 200, 120)
    #bgcolor = (230, 230, 230)

    dist = img.colorDistance(bgcolor)
    mask = dist.binarize()

    foreground = img - mask

    background = background - mask.invert()
    combined = background + foreground
    combined.save(disp)


