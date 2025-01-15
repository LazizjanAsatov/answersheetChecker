import pytesseract
import cv2


def preprocess_roi(roi):
    """
    Preprocess a region of interest (ROI) for OCR.
    - Converts to grayscale.
    - Applies thresholding for better text recognition.
    """
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def extract_text_from_image(image_path, rois):
    """
    Extract text from defined ROIs in an image.
    - First 3 ROIs are treated as personal information.
    - Remaining ROIs are treated as answers.
    """
    # Read and resize the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (700, 700))

    # Separate personal info and answers
    personal_info = []
    answers = []

    # Loop through ROIs
    for idx, (x, y, w, h) in enumerate(rois):
        roi = img[y : y + h, x : x + w]
        processed_roi = preprocess_roi(roi)
        text = pytesseract.image_to_string(
            processed_roi, lang="eng", config="--psm 7"
        ).strip()
        nums = pytesseract.image_to_string(
            processed_roi,
            lang="eng",
            config="--psm 11 -c tessedit_char_whitelist=0123456789,./",
        ).strip()

        # Append text to the appropriate list
        if idx < 3:
            personal_info.append(text)
        else:
            answers.append(nums)

    return personal_info, answers


