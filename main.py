import argparse
import pyzed.sl as sl

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

    i = 0
    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()
    while i < 0:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.SIDE_BY_SIDE)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE)
            print(f"Image resolution: {image.get_width()} x {image.get_height()} || Image timestamp: {timestamp.get_milliseconds()}")
            i += 1

    zed.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to demo some of the Zed Mini features.")
    args = parser.parse_args()
    main(args)