import cv2
import numpy as np


def extract_id(thresh, roi, num_digits=7, num_options=10, min_fill_threshold=20):

    id_x, id_y, id_w, id_h = roi
    id_roi = thresh[id_y : id_y + id_h, id_x : id_x + id_w]
    bubble_height = id_h // num_options
    digit_width = id_w // num_digits
    student_id = []

    for i in range(num_digits):
        x_start = i * digit_width
        x_end = (i + 1) * digit_width
        digit_roi = id_roi[:, x_start:x_end]

        max_pixels = 0
        selected_number = -1

        for j in range(num_options):
            y_start = j * bubble_height
            y_end = (j + 1) * bubble_height
            bubble = digit_roi[y_start:y_end, :]

            # Count white pixels in the bubble
            filled_pixels = np.sum(bubble == 255)

            # Update the selected bubble if it has the most pixels
            if filled_pixels > max_pixels:
                max_pixels = filled_pixels
                selected_number = j

        # Validate the selected bubble against the threshold
        if max_pixels > min_fill_threshold:
            # Adjust for custom numbering: 1-9 -> 1-9, 0 -> 0
            adjusted_number = (selected_number + 1) % 10
            student_id.append(adjusted_number)
        else:
            student_id.append("X")  # Mark as unfilled

    return student_id


def visualize_rois(img, rois, roi_type=None):
    """
    Visualize the defined ROIs on the image with different colors for different ROI types.
    Returns the annotated image.

    Colors:
    - Multiple choice (bubble): Blue
    - Student ID: Red
    - Personal info: Green
    - Open questions: Purple
    """
    img_copy = img.copy()

    # Define colors for different ROI types (BGR format)
    colors = {
        "bubble_sections": (255, 0, 0),  # Blue
        "student_id": (0, 0, 255),  # Red
        "personal_info": (0, 255, 0),  # Green
        "open_questions": (255, 0, 255),  # Purple
        "default": (0, 255, 0),  # Default green
    }

    # If rois is a dictionary, process each type separately
    if isinstance(rois, dict):
        for roi_type, roi_data in rois.items():
            color = colors.get(roi_type, colors["default"])

            # Handle bubble sections differently as they're in a different format
            if roi_type == "bubble_sections":
                for section in roi_data:
                    x, y, w, h = section["roi"]
                    cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 2)
            # Handle student_id which is a single tuple
            elif roi_type == "student_id":
                x, y, w, h = roi_data
                cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 2)
            # Handle other ROI types that are lists of tuples
            else:
                for x, y, w, h in roi_data:
                    cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 2)
    # If rois is a list, use single color based on roi_type
    else:
        color = colors.get(roi_type, colors["default"])
        for x, y, w, h in rois:
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 2)

    return img_copy
