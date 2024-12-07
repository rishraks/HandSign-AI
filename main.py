import cv2
import mediapipe as mp
import numpy as np
import os
import datetime
import time


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


video_dir = "Videos"
os.makedirs(video_dir, exist_ok=True)
image_dir = "ScreenShots"
os.makedirs(image_dir, exist_ok=True)

fist_sign_detected_time = None
v_sign_detected_time = None
recording = False
out = None


def is_finger_extended(landmarks, tip_idx, pip_idx):
    return landmarks[tip_idx].y < landmarks[pip_idx].y


def is_finger_bent(landmarks, tip_idx, pip_idx):
    return landmarks[tip_idx].y > landmarks[pip_idx].y


def is_thumb_bent(landmarks, handedness):
    if handedness == "Left":
        return landmarks[4].x < landmarks[3].x and landmarks[4].x < landmarks[2].x
    else:
        return (
            landmarks[4].x > landmarks[3].x
            and landmarks[4].x > landmarks[2].x
            or landmarks[4].y > landmarks[3].y
        )


def is_thumb_extended(landmarks, handedness):
    if handedness == "Left":
        return landmarks[4].x > landmarks[3].x
    else:
        return landmarks[4].x < landmarks[3].x


cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (800, 700))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand, handedness in zip(
                results.multi_hand_landmarks, results.multi_handedness
            ):
                mp_drawing.draw_landmarks(
                    image,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(
                        color=(90, 22, 76), thickness=2, circle_radius=4
                    ),
                    mp_drawing.DrawingSpec(
                        color=(200, 122, 76), thickness=2, circle_radius=4
                    ),
                )

            hand_type = handedness.classification[0].label

            if is_finger_extended(hand.landmark, 8, 6) and is_finger_extended(
                hand.landmark, 12, 10
            ):
                if is_finger_bent(hand.landmark, 16, 14) and is_finger_bent(
                    hand.landmark, 20, 18
                ):
                    if is_thumb_bent(hand.landmark, hand_type):
                        cv2.putText(
                            image,
                            "Recording in 3 secs...",
                            (50, 50),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1,
                            (0, 0, 255),
                            2,
                        )
                        if v_sign_detected_time is None:
                            v_sign_detected_time = time.time()

            if (
                is_finger_extended(hand.landmark, 8, 6)
                and is_finger_extended(hand.landmark, 12, 10)
                and is_finger_extended(hand.landmark, 16, 14)
                and is_finger_extended(hand.landmark, 20, 18)
            ):
                if is_thumb_extended(hand.landmark, hand_type):
                    cv2.putText(
                        image,
                        "Recording Stop...",
                        (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    recording = False

            if (
                is_finger_bent(hand.landmark, 8, 6)
                and is_finger_bent(hand.landmark, 12, 10)
                and is_finger_bent(hand.landmark, 16, 14)
                and is_finger_bent(hand.landmark, 20, 18)
            ):
                if is_thumb_bent(hand.landmark, hand_type):
                    cv2.putText(
                        image,
                        "Picture in 3secs!!",
                        (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    if fist_sign_detected_time is None:
                        fist_sign_detected_time = time.time()

        if recording:
            cv2.putText(
                image,
                "Recording Started!!",
                (50, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 0, 255),
                2,
            )

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1)

        if v_sign_detected_time is not None:
            elapsed_time = time.time() - v_sign_detected_time
            if elapsed_time >= 3 and not recording:
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                video_file = os.path.join(video_dir, f"VID_{timestamp}.avi")
                out = cv2.VideoWriter(video_file, fourcc, 30, (640, 480))
                recording = True
                v_sign_detected_time = None

        if recording and out is not None:
            out.write(image)

        if fist_sign_detected_time is not None:
            elapsed_time = time.time() - fist_sign_detected_time
            if elapsed_time >= 3:
                img_time = datetime.datetime.now()
                formatted_time = img_time.strftime("%Y%m%d_%H%M%S")
                file_name = f"{image_dir}/IMG_{formatted_time}.png"
                cv2.imwrite(file_name, image)
                fist_sign_detected_time = None

        if key == ord("q"):
            break

cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
