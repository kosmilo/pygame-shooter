import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from settings import *

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode
mp_draw = mp.solutions.drawing_utils


class HandTracking:
    def __init__(self, session):
        self.session = session
        self.model_path = 'resources/gesture_recognizer.task'
        self.vid = cv2.VideoCapture(0)
        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.update_hand_info  # this controls what function to call for the output
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(self.options)

    @staticmethod
    def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        print('timestamp: {}, gesture recognition result: {}'.format(timestamp_ms, result))

    def print_hand_info(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if self.is_hand_visible(result):
            x, y = self.get_hand_location(result)
            screen_x = WIDTH * (1 - x)
            screen_y = HEIGHT * y
            print('timestamp: {}, gesture: {}, x: {} out of {}, y: {} out of {}'.format(
                timestamp_ms, self.get_hand_gesture_name(result), screen_x, WIDTH, screen_y, HEIGHT))
        else:
            print('hand not visible')

    def update_hand_info(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if self.is_hand_visible(result):
            # get hand location, translate it into screen coordinates and set mouse pos
            # the max/min stuff is so the cursor can't go out of boundaries and break everything
            x, y = self.get_hand_location(result)
            screen_x = max(20, min(WIDTH * (1 - x), WIDTH-20))
            screen_y = max(20, min(HEIGHT * y, HEIGHT-20))
            pg.mouse.set_pos(screen_x, screen_y)

            # this is for debugging purposes
            # print('timestamp: {}, gesture: {}, x: {} out of {}, y: {} out of {}'.format(
            #    timestamp_ms, self.get_hand_gesture_name(result), screen_x, WIDTH, screen_y, HEIGHT))

            # if the gesture is a closed fist, simulate mouse click
            if self.get_hand_gesture_name(result) == 'Closed_Fist':
                mouse_click_event = pg.event.Event(pg.MOUSEBUTTONDOWN, {'pos': (screen_x, screen_y), 'button': 1})
                pg.event.post(mouse_click_event)
                print('closed fist/simulated left mouse click at {}, {}'.format(screen_x, screen_y))
        else:
            print('hand not visible')  # this can be replaced with a warning or some such

    @staticmethod
    def is_hand_visible(result: GestureRecognizerResult):
        if len(result.hand_landmarks) > 0:
            return True
        else:
            return False

    @staticmethod
    def get_hand_location(result: GestureRecognizerResult):
        hand_landmarks = result.hand_landmarks[0]
        hand_location = hand_landmarks[0].x, hand_landmarks[0].y
        return hand_location

    @staticmethod
    def get_hand_gesture_name(result: GestureRecognizerResult):
        hand_gesture = result.gestures[0][0].category_name
        return hand_gesture

    def update(self):
        ret, frame = self.vid.read()  # capture video
        mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)  # convert frame to mp image
        self.recognizer.recognize_async(mp_frame, pg.time.get_ticks())  # use gesture recognition on the mp image
        # cv2.imshow('frame', frame)  # display camera feed
