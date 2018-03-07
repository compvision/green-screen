"""
aaaa
"""
import numpy as np
import cv2


def main():
    """
    aaaa
    """
    # default cam matrix rows and columns
    cap = cv2.VideoCapture(1)  # use external cam
    #cap = cv2.resize(cap, [7680, 4320])
    bg_cap = cv2.VideoCapture("video.avi")
    # get the background and resize it.
    #img_back = cv2.imread('background.jpg')
    background_color = np.uint8([[[0, 255, 0]]])
    hls_background_color = cv2.cvtColor(background_color, cv2.COLOR_BGR2HLS)
    hls_background_color = hls_background_color[0][0]
    frame_count = 0
    while True:
        frame_count += 1
        if frame_count == int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            cap.set(cv2.CAP_PROP_FRAME_COUNT, 2)
            frame_count = 0
            frame_count += 1
        _, frame = cap.read()
        ret, img_back = bg_cap.read()
        back_cols, back_rows = img_back.shape[:2]
        frame = cv2.resize(frame, (back_rows, back_cols))
        cols, rows = frame.shape[:2]
        background = img_back[0:cols, 0:rows]
        frame = cv2.flip(frame, 1, frame)

        hls_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

        hue = hls_image[:, :, 0]

        binary_hue = cv2.inRange(hue, 30, 100)

        mask = np.zeros(img_back.shape, dtype=np.uint8)

        mask[:, :, 0] = binary_hue
        mask[:, :, 1] = binary_hue
        mask[:, :, 2] = binary_hue

        blured = cv2.GaussianBlur(mask, (11, 11), 0)
        blured_inverted = cv2.bitwise_not(blured)
        bg_key = cv2.bitwise_and(background, blured)
        fg_key = cv2.bitwise_and(frame, blured_inverted)
        cv2.imwrite('bg.jpg', bg_key)
        cv2.imwrite('fg.jpg', fg_key)
        keyed = cv2.add(bg_key, fg_key)
        keyed = cv2.resize(keyed, (1366, 768))
        cv2.imshow('frame', keyed)
        k = cv2.waitKey(33)
        if k == 27:  # ESC
            break

if __name__ == "__main__":
    main()
