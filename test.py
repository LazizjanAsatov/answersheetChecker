# import cv2
# import numpy as np


# def extract_id(thresh, roi, num_digits=7, num_options=10, min_fill_threshold=20):
    
#     id_x, id_y, id_w, id_h = roi
#     id_roi = thresh[id_y : id_y + id_h, id_x : id_x + id_w]
#     bubble_height = id_h // num_options
#     digit_width = id_w // num_digits
#     student_id = []

#     for i in range(num_digits):
#         x_start = i * digit_width
#         x_end = (i + 1) * digit_width
#         digit_roi = id_roi[:, x_start:x_end]

#         max_pixels = 0
#         selected_number = -1

#         for j in range(num_options):
#             y_start = j * bubble_height
#             y_end = (j + 1) * bubble_height
#             bubble = digit_roi[y_start:y_end, :]

#             # Count white pixels in the bubble
#             filled_pixels = np.sum(bubble == 255)

#             # Debugging: Print the filled pixel count
#             print(f"Digit {i}, Option {j}, Pixels: {filled_pixels}")

#             # Update the selected bubble if it has the most pixels
#             if filled_pixels > max_pixels:
#                 max_pixels = filled_pixels
#                 selected_number = j

#         # Validate the selected bubble against the threshold
#         if max_pixels > min_fill_threshold:
#             # Adjust for custom numbering: 1-9 -> 1-9, 0 -> 0
#             adjusted_number = (selected_number + 1) % 10
#             student_id.append(adjusted_number)
#         else:
#             student_id.append("X")  # Mark as unfilled

#     return student_id


# path = "./answers2.jpg"  # Replace with your image path
# img = cv2.imread(path)
# img = cv2.resize(img, (700, 700))  # Resize for consistent processing
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)  # Binary thresholding

# # Define the ROI for the student ID section
# rois = [(131, 110, 59, 132)]  # Replace with your specific ROI coordinates

# # Extract student ID
# student_id = extract_id(thresh, rois[0])
# print("Student ID:", "".join(map(str, student_id)))

# # Visualize the ROI and detected bubbles
# for x, y, w, h in rois:
#     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
# cv2.imshow("Processed Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
