class ImageLoader:

    def __init__(self, imagelist, callback):
        self.imagelist = imagelist
        self.callback = callback
        self.images = []
        self.image_toload = len(self.imagelist)
        for image in self.imagelist:
            self.load(image)

    def load(self, imageurl):
        image = __new__(Image())
        self.images.append(image)
        image.addEventListener('load', self.loaded, False)
        image.src = imageurl

    def loaded(self):
        self.image_toload -= 1
        if not self.image_toload:
            self.callback.onImagesLoaded(self.images)


def loadImages(imagelist, callback):
    ImageLoader(imagelist, callback)

