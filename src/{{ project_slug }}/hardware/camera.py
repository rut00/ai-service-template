import cv2
import threading
import time


class USBCamera:

    def __init__(self, camera_id=0, width=640, height=480, fps=30):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps

        self.cap = None
        self.running = False
        self.frame = None
        self.lock = threading.Lock()

    def start(self):
        """Start camera stream in background thread."""
        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera {self.camera_id}")

        # Set properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        self.running = True
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        """Continuously read frames."""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            with self.lock:
                self.frame = frame

    def read(self):
        """Return latest frame."""
        with self.lock:
            if self.frame is None:
                return None
            return self.frame.copy()

    def stop(self):
        """Stop camera stream."""
        self.running = False
        time.sleep(0.1)

        if self.cap:
            self.cap.release()
            self.cap = None
