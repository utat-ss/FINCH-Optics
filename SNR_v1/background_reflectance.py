from PIL import Image
import numpy as np
import os

def background_reflectance(season):
    print("Gathering Background Reflectance...")
    if season == "winter":
        img = "reflectance_landsat\\january_2021.TIF"
    elif season == "spring":
        img = "reflectance_landsat\\april_2021.TIF"
    elif season == "summer":
        img = "reflectance_landsat\\july_2020.TIF"
    elif season == "fall":
        img = "reflectance_landsat\\october_2020.TIF"

    img = np.asarray(Image.open(img))
    img = np.reshape(img, (img.shape[0]*img.shape[1]))
    reflectance = np.mean(img.astype(float))/65535

    # 65535 here is the maximum size of the surface reflectance values (they are stored as uint_16)
    # Documentation: https://prd-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/atoms/files/LSDS-1619_Landsat8-C2-L2-ScienceProductGuide-v2.pdf

    # print("Reflectance in %s: %.3f\n" % (season, reflectance))
    return reflectance