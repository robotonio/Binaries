import cv2
import numpy as np
import os
from fastiecm import fastiecm

class CVTool:
    def __init__(self, folder="useful_images_new"):
        self.folder = folder
        self.forest_level = (230, 255)
        self.crops_level = (200, 229)
        self.forest_counter = 0
        self.crops_counter = 0
        
    def remove_frame(self, img, scale=0.15):
        img = cv2.resize(img, (2592, 1944), interpolation=cv2.INTER_AREA)
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)
        dim = (width, height)
        # resize image
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        mask = np.zeros((img.shape[0], img.shape[1]), np.uint8)
        center = (width//2, height//2)
        radius = (height // 2) - 50
        color = (255, 255, 255)
        cv2.circle(mask, center, radius, color, -1)
        # masked
        clear_image = cv2.bitwise_and(img, img, mask=mask)
        return clear_image

    def contrast_stretch(self, im, per=5):
        # find the top brightness of pixels in the image in 
        # the top 5% and bottom 5% of your image.
        in_min = np.percentile(im, per)
        # print(in_min)
        in_max = np.percentile(im, 100 - per)
        # print(in_max)
        # set the maximum brightness and minimum brightness on the 
        # new image you are going to create. The brightest a pixel’s 
        # colour can be is 255, and the lowest is 0
        out_min = 0.0
        out_max = 255.0

        # change all the pixels in the image, so that the image has the 
        # full range of contrasts from 0 to 255.
        out = im - in_min
        out *= ((out_min - out_max) / (in_min - in_max))
        out += in_min

        return out

    def gray_ndvi(self, image):
        '''
        Now that you have a high contrast image, it’s time to do the 
        NDVI calculations. This will take all the blue pixels and make 
        them brighter, and make all the red pixels darker, leaving an 
        image that will be black and white. The brightest pixels in 
        the image indicate healthy plants, and the darkest pixels 
        ndicate unhealthy plants or an absence of plants.
        '''
        image = self.contrast_stretch(image, per=5)

        # To adjust the pixels in the image and only work with red and blue, 
        # the image needs splitting into its three seperate channels. 
        # r for red, g for green, and b for blue.

        b, g, r = cv2.split(image)
        # Now the red and blue channels need to be added together and stored as bottom
        bottom = (r.astype(float) + b.astype(float))
        # Because we’re doing a division, we also need to make sure 
        # that none of our divisors are 0, or there will be an error
        bottom[bottom==0] = 0.01
        # The blue channel can then have the red channel subtracted 
        # (remember that red would mean unhealthy plants or no plants), 
        # and then divided by the bottom calculation
        ndvi = (b.astype(float) - r) / bottom
        # To once again enhance the image, it can be run 
        # through the contrast_stretch function
        ndvi_contrasted = self.contrast_stretch(ndvi)
        # remove frame
        mask = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        center = (image.shape[1] // 2, image.shape[0] // 2)
        radius = (image.shape[0] // 2) - 50
        color = (255, 255, 255)
        cv2.circle(mask, center, radius, color, -1)
        ndvi_contrasted = cv2.bitwise_and(ndvi_contrasted, ndvi_contrasted, mask=mask)

        return ndvi_contrasted

    def colored_ndvi(self, image):
        gray_ndvi = self.gray_ndvi(image)
        # You can run the image through a colour mapping process that will 
        # turn really bright pixels to the colour red and dark pixels to the colour blue
        color_mapped_prep = gray_ndvi.astype(np.uint8)
        # The current image, that you have saved as ndvi_contrasted is not suitable 
        # for colour mapping. The numbers stored in the numpy array are currently 
        # all floats or what is commonly known as decimal numbers. They all need 
        # converting to whole numbers, or integers between 0 and 255
        color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)

        return color_mapped_image


    def display(self, win_name, image, scale=1, wait=True):    
        image = np.array(image, dtype=float)/float(255)
        shape = image.shape
        height = int(shape[0] * scale)
        width = int(shape[1] * scale)
        image = cv2.resize(image, (width, height))
        cv2.namedWindow(win_name)
        cv2.imshow(win_name, image)
        if wait:
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            cv2.waitKey(10)

    def scan(self, scale=0.5, debug=False, wait=False):
        total = 0
        count = 0
            
        for image in os.listdir(self.folder):
            #img_path = filename
            img = cv2.imread(os.path.join(self.folder, image))
            if img is not None:                
                clear_img = self.remove_frame(img, scale=scale)
                gray_ndvi = self.gray_ndvi(clear_img)
                forest_array = ((self.forest_level[0] < gray_ndvi) & (gray_ndvi < self.forest_level[1]))
                self.forest_counter += forest_array.sum()
                crops_array = ((self.crops_level[0] < gray_ndvi) & (gray_ndvi < self.crops_level[1]))
                self.crops_counter += crops_array.sum()
                print("Forest:", self.forest_counter, ", Crops:", self.crops_counter)

                colored_ndvi = self.colored_ndvi(clear_img)
                if debug:
                    self.display("Gray NDVI", gray_ndvi, scale=1, wait=False)
                    self.display("Clear Image", clear_img, scale=1, wait=False)
                    self.display("Colored NDVI", colored_ndvi, scale=1, wait=wait)

def main():
    cvtool = CVTool()
    cvtool.scan(debug=False, wait=False)
    counter = cvtool.forest_counter + cvtool.crops_counter
    print("Forest %", (cvtool.forest_counter * 100)/counter)
    print("Crops %", (cvtool.crops_counter * 100) / counter)

if __name__ == "__main__":
    main()
