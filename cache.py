from PIL import Image
import os
import numpy as np
import json as js

def main():
    imageObj = os.scandir("./assets/src/")
    json = {}
    for imageName in imageObj:
        image = Image.open(f"./assets/src/{imageName.name}")
        mean = np.asarray(image).mean(axis=(0, 1))
        json[f"{imageName.name}"] = np.floor(mean).tolist() # to convert np array to normal list
        
    with open("./cache.json", "w") as cache:
        cache.write(js.dumps(json, indent=4))
        
if __name__ == "__main__":
    main()
    