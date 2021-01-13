import numpy as np
import json
from bresenham import bresenham
import requests
import cv2
import os

#def drawPNG (vector_images, side=256, time=10):
def drawPNG (vector_images, side=(720,1280), time=15):
        # raster_image = np.ones((side, side), dtype=np.uint8) * 255
        raster_image = np.ones(side, dtype=np.uint8) * 255
        #print(raster_image.shape)
        prevX, prevY = None, None
        start_time = vector_images[0]['timestamp']
        # print (start_time)
        # print (vector_images[-1]['timestamp'] - vector_images[0]['timestamp'])
        for points in vector_images:
                if (points['timestamp'] - start_time)/1000 > time:
                    break
                x, y = map(float, points['coordinates'])
                x = int(x * side[1])
                y = int(y * side[0])
                #print('x: ', x,' y: ',y)

                pen_state = list(map(int, points['pen_state']))
                if not (prevX is None or prevY is None):
                        cordList = list(bresenham(prevX, prevY, x, y))
                        #print('cordList: ', cordList)
                        for cord in cordList:
                                #print('cord: ', cord)
                                if (cord[0] > 0 and  cord[1] > 0) and (cord[0] < side[0] and  cord[1] < side[1]):
                                        raster_image[cord[1], cord[0]] = 0
                                        #raster_image[cord[0], cord[1]] = 0
                        if pen_state == [0, 1, 0]:
                                prevX = x; prevY = y
                        elif pen_state == [1, 0, 0]:
                                prevX = None 
                                prevY = None
                        else:
                                raise ValueError("pen_state not accounted for")
                else:
                        prevX = x 
                        prevY = y

        return raster_image


if __name__ == "__main__":
        output_dir = "output/size1280"
        #os.makedir(output_dir, exists_ok=True)
        all_data = json.load(open("all_data.json", "r"))
        user_list = all_data['users']
        #user_list = ["17"]
        for usr_id, user in enumerate(user_list):
                usr_id = user
                count = 0
                urls_list = all_data[user].keys()
                for url_id, url in enumerate(urls_list):
                        count += 1
                        data = all_data[user][url]
                        sketch = data['sketch']
                        #sketch_caption = data['sketch_caption']
                        # for time in [20, 40, 60]:
                        for time in [15]:
                            raster_sketch = drawPNG(sketch, time=time)
                            cv2.imwrite(os.path.join(
                                    output_dir, str(usr_id)+
                                    "_"+str(url_id)+"_"+str(time)+"_sketch.png"),
                                    raster_sketch)
                        # img_data = requests.get(url).content
                        # with open(os.path.join(output_dir, 
                        #         str(usr_id)+"_"+str(url_id)+"_img.png"), "wb") as handler:
                        #         handler.write(img_data)

                        # with open(os.path.join(output_dir,
                        #         str(usr_id)+"_"+str(url_id)+"_sketch_caption.txt"), "w") as fp:
                        #         fp.write(sketch_caption)
                print ("User: ", user, " has submitted ", count, " annotation.")
