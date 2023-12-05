import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from main import *

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode
mp_draw = mp.solutions.drawing_utils


def is_hand_visible(result: GestureRecognizerResult):
    if len(result.hand_landmarks) > 0:
        return True
    else:
        return False


def get_hand_location(result: GestureRecognizerResult):
    hand_landmarks = result.hand_landmarks[0]
    hand_location = hand_landmarks[0].x, hand_landmarks[0].y
    return hand_location


def get_hand_gesture_name(result: GestureRecognizerResult):
    hand_gesture = result.gestures[0][0].category_name
    return hand_gesture


class HandTracking:
    def __init__(self, game):
        self.game = game
        self.model_path = 'resources/gesture_recognizer.task'
        self.vid = cv2.VideoCapture(0)
        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.update_hand_info
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)

    @staticmethod
    def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        print('timestamp: {}, gesture recognition result: {}'.format(timestamp_ms, result))

    @staticmethod
    def print_hand_info(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if is_hand_visible(result):
            print('timestamp: {}, gesture: {}, location: {}'.format(
                timestamp_ms, get_hand_gesture_name(result), get_hand_location(result)))

    def update_hand_info(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if is_hand_visible(result):
            x, y = get_hand_location(result)
            screen_x = WIDTH * (1 - x)
            screen_y = HEIGHT * y
            pg.mouse.set_pos(screen_x, screen_y)
            if get_hand_gesture_name(result) == 'Closed_Fist':
                closed_fist_event = pg.event.Event(CLOSED_FIST)
                pg.event.post(closed_fist_event)
            print('hand visible')
        else:
            print('hand not visible')

    def get_pos(self):
        return self.x, self.y

    def update(self):
        ret, frame = self.vid.read()
        latest_frame = frame
        mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=latest_frame)
        self.recognizer.recognize_async(mp_frame, pg.time.get_ticks())
