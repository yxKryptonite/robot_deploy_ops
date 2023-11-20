from camera.single_camera import Camera
from turtlebot.move_25 import GoForward
from turtlebot.turn_left30 import TurnLeft
from turtlebot.turn_right30 import TurnRight
from network.scp import get_scp_client, upload_img, download_txt

def main():
    config_file = "network/mm.yaml"
    scpclient = get_scp_client(config_file)
    
    while True:
        GoForward()
        break
    
if __name__ == "__main__":
    main()