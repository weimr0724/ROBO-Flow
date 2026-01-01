from typing import Optional, Tuple

try:
    import cv2
    import numpy as np
except Exception:
    cv2 = None
    np = None

DxDy = Tuple[float, float]

class VisionInput:
    """
    Teaching-grade OpenCV pipeline:
    - Capture frame
    - Detect red object (HSV)
    - Output normalized offset (dx, dy) in [-1, 1]
    """

    def __init__(self, cam_index: int = 0, width: int = 640, height: int = 480, show: bool = True):
        if cv2 is None or np is None:
            raise RuntimeError("OpenCV or numpy not installed. Run: pip install opencv-python numpy")
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.show = show
        self.width = width
        self.height = height
        self.running = True

    def next(self) -> Optional[DxDy]:
        if not self.running:
            return None

        ok, frame = self.cap.read()
        if not ok or frame is None:
            return None

        h, w = frame.shape[:2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Red can wrap around hue=0, so we use two masks.
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([170, 120, 70])
        upper2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower1, upper1)
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)

        # Reduce noise
        mask = cv2.medianBlur(mask, 5)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cx, cy = None, None
        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > 300:  # ignore small noise
                x, y, ww, hh = cv2.boundingRect(c)
                cx = x + ww // 2
                cy = y + hh // 2

                if self.show:
                    cv2.rectangle(frame, (x, y), (x+ww, y+hh), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

        # draw center crosshair
        if self.show:
            cv2.line(frame, (w//2, 0), (w//2, h), (255, 255, 255), 1)
            cv2.line(frame, (0, h//2), (w, h//2), (255, 255, 255), 1)
            cv2.imshow("Vision Input (Teaching)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False
                return None

        # If no target found, return (0,0) to hold near base.
        if cx is None or cy is None:
            return (0.0, 0.0)

        dx = (cx - w/2) / (w/2)   # normalize to [-1,1]
        dy = (cy - h/2) / (h/2)
        dx = max(-1.0, min(1.0, float(dx)))
        dy = max(-1.0, min(1.0, float(dy)))
        return (dx, dy)

    def close(self):
        try:
            self.cap.release()
        except Exception:
            pass
        if cv2 is not None:
            try:
                cv2.destroyAllWindows()
            except Exception:
                pass
