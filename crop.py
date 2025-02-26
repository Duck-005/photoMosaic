from PIL import Image
import os

def main():
    imageObj = os.scandir("./assets/flowers/")
    x = '1'
    for imageName in imageObj:
        image = Image.open(f"./assets/flowers/{imageName.name}")
        height, width = image.size
        
        if(height < width):
            image.crop((0, 0, height, height)).save(f"./assets/src/src_{x.zfill(3)}.jpg")
        else:
            image.crop((0, 0, width, width)).save(f"./assets/src/src_{x.zfill(3)}.jpg")
        x = str(int(x) + 1)
        
if __name__ == "__main__":
    main()
        