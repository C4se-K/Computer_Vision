import cv2
import os
import time
import numpy as np
import math

file = "test_video2.mp4"
current_dir = os.path.dirname(os.path.abspath(__file__))
video_file = os.path.join(current_dir, file)

cap = cv2.VideoCapture(video_file)
if not cap.isOpened():
    print("Error: cannot open file")
    exit()


frame_times = []
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
processed_frames = 0


#determine the resolution of the process
# a value below 1, which would result in < (9, 16) which would be suboptimal
multiplier = 1
frame_x = int(16 * multiplier)
frame_y = int(9 * multiplier)
product = frame_x * frame_y


# for monitoring
grad_list = np.zeros((frame_y, frame_x))
prev_frame = np.zeros((frame_y, frame_x))


while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    start_time = time.time()

    #testing
    #display for testing/confirmation
    cv2.imshow('Edges', cv2.resize(frame, (1600, 800)))

    # (frame_x, frame_y) instead of (16, 9) makes the processing around x2 slower.
    # memory access overhead... hardcode...
    frame_resized = cv2.resize(frame, (frame_x, frame_y))
    gray_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    # dont really need this if calculting with integers is fine
    normalized_gray = gray_frame#np.round(gray_frame / 255.0, 4)

    #currently, up to 0 works
    threshold = 0
    difference = np.abs(normalized_gray - prev_frame)
    changes = difference > threshold

    #9n x 16n
    for row in range(changes.shape[0]):
        for col in range(changes.shape[1]):
            grad_list[row, col] = 1 if changes[row, col] else 0

    

    prev_frame = normalized_gray

    frame_times.append(time.time() - start_time)
    processed_frames += 1


    #display and monitoring
    os.system('cls' if os.name == 'nt' else 'clear')
    temp_list = grad_list
    print(np.array(temp_list).reshape(frame_y, frame_x))
    #print(grid.shape)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break





cap.release()
cv2.destroyAllWindows()

total_time = sum(frame_times)
avg_time_per_frame = total_time / processed_frames if processed_frames > 0 else 0
frame_time_std = np.std(frame_times)

print(f"processed {processed_frames} frames out of {total_frames}")
print(f"total processing time: {total_time:.2f} seconds")
print(f"average time per frame: {avg_time_per_frame:.4f} seconds")
print(f"frame time standard deviation: {frame_time_std:.4f} seconds")


"""
    # (image, threshold1 , threshold2[, apertureSize[, L2gradient]])
    # threshold 1 is the lower bound of detction raising it would make the detection more sensitive
    # it would also make it less consistent

    # threshold 2 is the upper bound of detection raising it would make the detection more consistent
    #but also less sensitive. only hard edges will be detected

    # if the two values are the same, eg. 200, 200 the image will only detect the hard edges
    # also becomes dependent on the value itself. 
    # cant make a conclusion yet.
    """
    #edges = cv2.Canny(frame_resized, 100, 200)
    #cv2.imshow('Edges', edges)