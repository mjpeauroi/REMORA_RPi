import cv2
import os

setthreshold = 20

# Set environment variable for the current process and any subprocesses it spawns
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Use the first camera as video source
cap = cv2.VideoCapture(0)

frame_width = 640
frame_height = 480

# Define the codec and create VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*"avc1")
out = cv2.VideoWriter("out_vid.mp4", fourcc, 30.0, (frame_width, frame_height))

try:
    # Initial frame read
    done, CurrentFrame = cap.read()
    done, NextFrame = cap.read()

    while done:
        # Calculate the absolute difference between current frame and next frame
        diff = cv2.absdiff(CurrentFrame, NextFrame)

        # Convert to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur
        blured_img = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply threshold
        threshold, binary_img = cv2.threshold(blured_img, setthreshold, 255, cv2.THRESH_BINARY)

        # Dilate the image
        dilated = cv2.dilate(binary_img, None, iterations=12)

        # Find contours
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        motion_detected = False  # Flag to check if motion is detected

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue

            # Draw rectangle around the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(CurrentFrame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            motion_detected = True
            print("detected")

        if not motion_detected:
            # If no motion is detected
            print("still")

        # Show the frame
        cv2.imshow("frame", CurrentFrame)

        # Save the current frame to output file
        out.write(CurrentFrame)

        # Prepare for next iteration
        CurrentFrame = NextFrame
        done, NextFrame = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    cv2.destroyAllWindows()
    cap.release()
    out.release()
