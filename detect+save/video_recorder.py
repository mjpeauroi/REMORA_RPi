import cv2
import threading
import time

class Video_Recorder:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        if not self.cam.isOpened():
            raise Exception("Could not open video device")
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = None
        self.filename = None
        self.recording = False
        self.lock = threading.Lock()

    def start_recording(self, filename, video_length):
        with self.lock:
            if self.recording:
                print("Recording is already in progress.")
                return
            self.filename = filename
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            self.out = cv2.VideoWriter(self.filename, fourcc, 15.0, (self.frame_width, self.frame_height))
            self.recording = True
        threading.Thread(target=self.record, args=(video_length,)).start()

    def record(self, video_length):
        start_time = time.time()
        while True:
            with self.lock:
                if not self.recording:
                    break
                ret, frame = self.cam.read()
            if ret:
                self.out.write(frame)
            else:
                print("Failed to capture video frame")
                break
            if (time.time() - start_time) >= video_length:
                break
        self.stop_recording()

    def get_frame(self):
        with self.lock:
            ret, frame = self.cam.read()
        if ret:
            return ret, frame
        else:
            print("Failed to read frame")
            return None

    def stop_recording(self):
        with self.lock:
            if self.recording:
                self.recording = False
                if self.out:
                    self.out.release()
                    self.out = None
                print(f"Recording stopped. Video saved as: {self.filename}")

    def stop_immediately(self):
        with self.lock:
            if self.recording:
                self.recording = False
                if self.out:
                    self.out.release()
                    self.out = None
                print("Recording stopped immediately.")

    def release_resources(self):
        with self.lock:
            if self.cam:
                self.cam.release()
            if self.out:
                self.out.release()

