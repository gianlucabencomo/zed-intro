import argparse
import pyzed.sl as sl

import cv2
import numpy as np

def main(args):
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30
    init_params.sdk_verbose = 0

    # Open camera
    e = zed.open(init_params)
    if e != sl.ERROR_CODE.SUCCESS:
        raise ValueError(f"ZED SDK raise the following error while attempting to open the camera: {e}")
    
    # Serial Number
    zed_serial = zed.get_camera_information().serial_number
    print(f"ZED Mini Serial Number: {zed_serial}")

    # Calibration Parameters
    calibration_params = zed.get_camera_information().camera_configuration.calibration_parameters

    runtime_parameters = sl.RuntimeParameters()
    image = sl.Mat()
    print("Press 'q' to quit")
    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.SIDE_BY_SIDE)
            frame = image.get_data()
            h, w = frame.shape[:2]
            cv2.imshow("ZED Live Stream", cv2.resize(frame, (720, int(h * (720 / w)))))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()
    zed.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to demo some of the Zed Mini features.")
    args = parser.parse_args()
    main(args)