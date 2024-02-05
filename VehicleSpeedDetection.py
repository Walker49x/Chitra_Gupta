import cv2
import dlib
import time
import math
import tkinter as tk
from PIL import Image, ImageTk


# Classifier File
car_cascade = cv2.CascadeClassifier(r"C:\Users\Priyanshu\PycharmProjects\Chitra_Gupta\assests\vech.xml")

# Video file capture
video = cv2.VideoCapture(r"C:\Users\Priyanshu\PycharmProjects\Chitra_Gupta\assests\Heavy Vehicular Traffic at Mumbai Ahmedabad National Highway 8 moving like Narendra Modi Wave !!!!!!_2.mp4")

# Constant Declaration
WIDTH = 1280
HEIGHT = 720

# Estimate speed function
def estimate_speed(location1, location2):
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
    ppm = 8.8
    d_meters = d_pixels / ppm
    fps = 18
    speed = d_meters * fps * 3.6
    return speed

# Tracking multiple objects
def track_multiple_objects():
    total_vehicle_count = 0
    counting_line_y = 500

    rectangle_color = (0, 255, 255)
    frame_counter = 0
    current_car_id = 0
    fps = 0

    car_tracker = {}
    car_numbers = {}
    car_location1 = {}
    car_location2 = {}
    speed = [None] * 1000

    out = cv2.VideoWriter('outTraffic.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (WIDTH, HEIGHT))

    while True:
        start_time = time.time()
        rc, image = video.read()
        if type(image) == type(None):
            break

        image = cv2.resize(image, (WIDTH, HEIGHT))
        result_image = image.copy()

        frame_counter += 1
        car_id_to_delete = []

        for car_id in car_tracker.keys():
            tracking_quality = car_tracker[car_id].update(image)

            if tracking_quality < 7:
                car_id_to_delete.append(car_id)

        for car_id in car_id_to_delete:
            print(f"Removing carID {car_id} from list of trackers.")
            car_tracker.pop(car_id, None)
            car_location1.pop(car_id, None)
            car_location2.pop(car_id, None)

        if not (frame_counter % 10):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))

            for (x, y, w, h) in cars:
                x_bar, y_bar = x + 0.5 * w, y + 0.5 * h
                match_car_id = None

                for car_id in car_tracker.keys():
                    tracked_position = car_tracker[car_id].get_position()
                    t_x, t_y, t_w, t_h = map(int, [tracked_position.left(), tracked_position.top(),
                                                  tracked_position.width(), tracked_position.height()])
                    t_x_bar, t_y_bar = t_x + 0.5 * t_w, t_y + 0.5 * t_h

                    if (t_x <= x_bar <= t_x + t_w) and (t_y <= y_bar <= t_y + t_h) and \
                            (x <= t_x_bar <= x + w) and (y <= t_y_bar <= y + h):
                        match_car_id = car_id

                if match_car_id is None:
                    print(f'Creating new tracker {current_car_id}')
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    car_tracker[current_car_id] = tracker
                    car_location1[current_car_id] = [x, y, w, h]
                    current_car_id += 1

        for car_id in car_tracker.keys():
            tracked_position = car_tracker[car_id].get_position()
            t_x, t_y, t_w, t_h = map(int, [tracked_position.left(), tracked_position.top(),
                                           tracked_position.width(), tracked_position.height()])

            cv2.rectangle(result_image, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangle_color, 4)
            car_location2[car_id] = [t_x, t_y, t_w, t_h]

        end_time = time.time()

        if not (end_time == start_time):
            fps = 1.0 / (end_time - start_time)

        for i in car_location1.keys():
            if frame_counter % 1 == 0:
                [x1, y1, w1, h1] = car_location1[i]
                [x2, y2, w2, h2] = car_location2[i]

                car_location1[i] = [x2, y2, w2, h2]

                if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
                    if (speed[i] is None or speed[i] == 0) and 275 <= y1 <= 285:
                        speed[i] = estimate_speed([x1, y1, w1, h1], [x1, y2, w2, h2])

                    if speed[i] is not None and y1 >= 180:
                        cv2.putText(result_image, f"{int(speed[i])} km/h",
                                    (int(x1 + w1 / 2), int(y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 100), 2)
                for (_x, _y, _w, _h) in cars:
                    x = int(_x)
                    y = int(_y)
                    w = int(_w)
                    h = int(_h)

                    x_bar = x + 0.5 * w
                    y_bar = y + 0.5 * h

                    # Check if the bottom of the detected object is within the counting region
                    if y_bar >= counting_line_y:
                        cv2.line(result_image, (0, counting_line_y), (WIDTH, counting_line_y), (255, 0, 0), 2)

        cv2.imshow('result', result_image)
        out.write(result_image)

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    out.release()

if __name__ == '__main__':
    track_multiple_objects()
