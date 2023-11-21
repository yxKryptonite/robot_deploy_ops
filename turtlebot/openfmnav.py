import os
import cv2
from camera.single_camera import Camera
from turtlebot.move_25 import GoForward # 1
from turtlebot.turn_left30 import TurnLeft # 2
from turtlebot.turn_right30 import TurnRight # 3
from network.scp import get_scp_client, upload_file, download_file, wait_for_result, generate_code
import datetime

def main():
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    config_file = "network/mm.yaml"
    scpclient = get_scp_client(config_file)
    code = None
    
    camera = Camera(width=640, height=480)
    c, d = camera.get_image_with_depth()
    print(c.shape, d.shape)
    os.makedirs(f"./{now}", exist_ok=True)
    os.makedirs(f"./{now}/color",exist_ok=True)
    os.makedirs(f"./{now}/depth",exist_ok=True)
    cv2.imwrite(f"./{now}/color/0.png", c)
    cv2.imwrite(f"./{now}/depth/0.png", d)
    
    count = 0
    
    while True:
        count += 1
        c, d = camera.get_image_with_depth()
        cv2.imwrite(f"./{now}/color/{count}.png", c)
        cv2.imwrite(f"./{now}/depth/{count}.png", d)
        code = generate_code()
        with open(f"./{now}/code.txt", "w") as f:
            f.write(code)
        upload_file(scpclient, f"/data/xxx/openfmnav/{now}/color/{count}.png", f"./{now}/color/{count}.png")
        upload_file(scpclient, f"/data/xxx/openfmnav/{now}/depth/{count}.png", f"./{now}/depth/{count}.png")
        upload_file(scpclient, f"/data/xxx/openfmnav/{now}/code.txt", f"./{now}/code.txt")
        
        result = wait_for_result(scpclient, f"/data/xxx/openfmnav/{now}/result.txt", f"./{now}/result.txt")
        if result == 1:
            GoForward()
        elif result == 2:
            TurnLeft()
        elif result == 3:
            TurnRight()
        elif result == 0:
            return # stop
    
        if count >= 500:
            print("count >= 500, stop")
            return
    
if __name__ == "__main__":
    main()