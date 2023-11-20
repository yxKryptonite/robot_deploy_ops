from camera.single_camera import Camera
import os
import cv2

if __name__ == "__main__":
    camera = Camera(width=640, height=480)
    c, d = camera.get_image_with_depth()
    print(c.shape, d.shape)
    c, d = camera.get_image_with_depth() # take a second shot
    os.makedirs("./color",exist_ok=True)
    os.makedirs("./depth",exist_ok=True)
    cv2.imwrite("./color/1.png", c)
    cv2.imwrite("./depth/1.png", d)