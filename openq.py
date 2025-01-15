import pytesseract
import cv2

# Define ROIs
rois = [
    (189, 493, 142, 25), #Famila
    (189, 530, 142, 25), #ism
    (189, 570, 142, 25), #otasini ismi

    (392, 135, 110, 35),  # 36a
    (515, 135, 110, 37),  # 36b
    (392, 187, 110, 37),  # 37a
    (515, 187, 110, 37),  # 37b
    (392, 240, 110, 37),  # 38a
    (515, 240, 110, 37),  # 38b
    (392, 292, 110, 37),  # 39a
    (515, 292, 110, 37),  # 39b
    (392, 344, 110, 37),  # 40a
    (515, 344, 110, 37),  # 40b
    (392, 395, 110, 37),  # 41a
    (515, 395, 110, 37),  # 41b
    (392, 450, 110, 37),  # 42a
    (515, 450, 110, 37),  # 42b
    (392, 502, 110, 37),  # 43a
    (515, 502, 110, 37),  # 43b
    (392, 555, 110, 37),  # 44a
    (515, 555, 110, 37),  # 44b
    (392, 605, 110, 37),  # 45a
    (515, 605, 110, 37),  # 45b
]

def preprocess_roi(roi):
    """
    Preprocess a region of interest (ROI) for OCR.
    - Converts to grayscale.
    - Applies thresholding for better text recognition.
    """
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def extract_text_from_image(image_path):
    """
    Extract text from defined ROIs in an image.
    - First 3 ROIs are treated as personal information.
    - Remaining ROIs are treated as answers.
    """
    # Read and resize the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (700, 700))  # Resize to expected dimensions

    # Separate personal info and answers
    personal_info = []
    answers = []

    # Loop through ROIs
    for idx, (x, y, w, h) in enumerate(rois):
        roi = img[y : y + h, x : x + w]
        processed_roi = preprocess_roi(roi)
        text = pytesseract.image_to_string(processed_roi, lang="eng", config="--psm 7").strip()
        nums=pytesseract.image_to_string(processed_roi, lang="eng", config="--psm 11 -c tessedit_char_whitelist=0123456789,./").strip()
        # Append text to the appropriate list
        if idx < 3:
            personal_info.append(text)
        else:
            answers.append(nums)

    # Output results
    print("Personal Info:", personal_info)
    print("Answers:", answers)

    return personal_info, answers

def visualize_rois(image_path):
    """
    Visualize the defined ROIs on the image.
    """
    img = cv2.imread(image_path)
    img = cv2.resize(img, (700, 700))  # Resize to expected dimensions

    # Draw rectangles around ROIs
    for x, y, w, h in rois:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image
    cv2.imshow("ROIs", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = "answers.jpg"
print("Available Languages:", pytesseract.get_languages())
personal_info, answers = extract_text_from_image(image_path)
visualize_rois(image_path)

