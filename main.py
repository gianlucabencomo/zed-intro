import argparse
import pyzed.sl as sl
import sys
from signal import signal, SIGINT
import os

def main(args):
    zed = sl.Camera()

    #Handler to deal with CTRL+C properly
    def handler(signal_received, frame):
        zed.disable_recording()
        zed.close()
        sys.exit(0)

    signal(SIGINT, handler)

    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080
    init_params.camera_fps = 30
    init_params.sdk_verbose = 0
    init.depth_mode = sl.DEPTH_MODE.NONE

    # Open camera
    e = zed.open(init_params)
    if e != sl.ERROR_CODE.SUCCESS:
        raise ValueError(f"ZED SDK raise the following error while attempting to open the camera: {e}")

    # Enable recording
    recording_params = sl.RecordingParameters(os.path.join(os.getcwd(), "output.svo"), sl.SVO_COMPRESSION_MODE.H264)
    e = zed.enable_recording(recording_params)
    if e != sl.ERROR_CODE.SUCCESS:
        raise ValueError(f"ZED SDK raise the following error while attempting to enable recording: {e}")

    
    
    # Serial Number
    zed_serial = zed.get_camera_information().serial_number
    print(f"ZED Mini Serial Number: {zed_serial}")

    # Calibration Parameters
    calibration_params = zed.get_camera_information().camera_configuration.calibration_parameters

    i = 0
    runtime_parameters = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.")
    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            print("Frame count: " + str(i), end="\r")
            i += 1

    zed.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to demo some of the Zed Mini features.")
    args = parser.parse_args()
    main(args)