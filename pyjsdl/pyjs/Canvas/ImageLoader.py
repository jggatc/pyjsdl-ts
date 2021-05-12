class ImageLoader:

    def __init__(self, imagelist, callback):
        self.imagelist = imagelist
        self.callback = callback
        self.images = []
        self.imgnum = len(self.imagelist)
        for img in self.imagelist:
            self.load(img)

    def load(self, imageurl):
        img = __new__(Image())
        self.images.append(img)
        img.addEventListener('load', self.loaded, False)
        img.src = imageurl

    def loaded(self):
        if len(self.images) == self.imgnum:
            self.callback.onImagesLoaded(self.images)


def loadImages(imagelist,callback):
    ImageLoader(imagelist,callback)

