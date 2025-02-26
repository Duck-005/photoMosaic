from PIL import Image
import math
import numpy as np
import json
import sys

def assembler(mosaicPhotos, size):   
    output = []
    width, height = size
    
    for row in mosaicPhotos:
        outputRow = []
        try:
            for image in row:
                with Image.open(f"./assets/src/{image}") as file:
                    block = np.asarray(file)
                    block = np.asarray(Image.fromarray(block).resize((10, 10)))
                    outputRow.append(block)
            output.append(np.hstack(outputRow))
        except(ValueError): continue
        # there may be some higher dimension rows if the image is not standardized so ignore them #_#.
        
    finOutput = np.vstack(output)
    Image.fromarray(finOutput).resize((width, height)).save("./finalOutput.jpg") 
    
def mosaic(pixelated_array):
    with open("./cache.json") as file:
        mapping = json.load(file)
        
    mosaicPhotos = []
    for row in range(len(pixelated_array)):
        mosaicRow = []
        for block in range(len(pixelated_array[0])):
            blockMean = pixelated_array[row][block]
            current_dist = float('inf')
            fileNameMatch = None
            for fileName, mean in mapping.items():
                
                # formula for calculating the least distance from the mean and the cache entry
                dist = math.sqrt(
                    (mean[0] - blockMean[0])**2 + 
                    (mean[1] - blockMean[1])**2 + 
                    (mean[2] - blockMean[2])**2
                )
                if dist < current_dist:
                    current_dist = dist
                    fileNameMatch = fileName
            mosaicRow.append(fileNameMatch)
        mosaicPhotos.append(mosaicRow)
    return mosaicPhotos
        
def avg(image, block_size=10):
    height = image.height
    width = image.width
    pixels = image.load()
    
    cropped_height = (height // block_size) * block_size
    cropped_width = (width // block_size) * block_size

    image_array = np.array([[pixels[x, y] for x in range(cropped_width)] for y in range(cropped_height)], dtype=np.uint8)
    
    # Reshape the image into blocks
    reshaped_array = image_array.reshape(
        cropped_height // block_size, block_size,
        cropped_width // block_size, block_size, 3
    )
    
    # Average the blocks across the height and width axes
    pixelated_array = reshaped_array.mean(axis=(1, 3)).astype(np.uint8)

    return pixelated_array
            
            
def main():
    image = Image.open("marvin.jpeg").convert("RGB")
    
    assembler(mosaic(avg(image)), image.size)
    
if __name__ == "__main__":
    main()
          