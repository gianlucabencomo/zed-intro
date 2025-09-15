import argparse
import pyzed.sl as sl

def main(args):
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.sdk_verbose = 0

    # Open camera
    e = zed.open(init_params)
    if e != sl.ERROR_CODE.SUCCESS:
        raise ValueError(f"ZED SDK raise the following error while attempting to open the camera: {e}")
        
    zed_serial = zed.get_camera_information().serial_number
    print(f"ZED Mini Serial Number: {zed_serial}")

    zed.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to demo some of the Zed Mini features.")
    args = parser.parse_args()