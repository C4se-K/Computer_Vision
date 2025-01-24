import cv2
import time
import os


video_file = 'test_video1.mp4'
cap = cv2.VideoCapture(video_file)

if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
frame_time_real = 1 / fps

control_speed = 1
target_frame_time = frame_time_real / control_speed


remaining_times = []
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
processed_frames = 0


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or cannot fetch frame.")
        break

    start_time = time.time()

    frame_resized = cv2.resize(frame, (160, 90))

    edges = cv2.Canny(frame_resized, 100, 200)

    processing_time = time.time() - start_time

    remaining_time = target_frame_time - processing_time
    remaining_times.append(max(0, remaining_time))


    if remaining_time > 0:
        time.sleep(remaining_time)

    cv2.imshow('Processed Frame', edges)

    processed_frames += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


total_remaining_time = sum(remaining_times)
average_remaining_time = total_remaining_time / len(remaining_times) if remaining_times else 0

print(f"Processed {processed_frames} frames out of {total_frames}.")
print(f"Control Speed (1:x): {control_speed}.")
print(f"Total Remaining Time: {total_remaining_time:.2f} seconds.")
print(f"Average Remaining Time per Frame: {average_remaining_time:.4f} seconds.")
