import cv2
from bubble import AnswerSheetGrader
from openq import extract_text_from_image
from studentid import extract_id, visualize_rois

# Define ROIs
ROIS = {
    # Multiple choice sections (x, y, width, height)
    "bubble_sections": [
        {"questions": 7, "choices": 5, "roi": (20, 255, 55, 200)},  # Questions 1-7
        {"questions": 7, "choices": 5, "roi": (79, 255, 48, 200)},  # Questions 8-14
        {"questions": 7, "choices": 5, "roi": (129, 255, 48, 200)},  # Questions 15-21
        {"questions": 7, "choices": 5, "roi": (184, 255, 48, 200)},  # Questions 22-28
        {"questions": 4, "choices": 5, "roi": (238, 255, 48, 110)},  # Questions 29-32
        {"questions": 3, "choices": 7, "roi": (238, 375, 65, 80)},  # Questions 33-35
    ],
    "student_id": (131, 110, 59, 132),
    "personal_info": [
        (189, 493, 142, 25),  # Family name
        (189, 530, 142, 25),  # First name
        (189, 570, 142, 25),  # Father's name
    ],
    "open_questions": [
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
    ],
}


def process_answer_sheet(image_path, width=700, height=700):
    # Initialize grader
    grader = AnswerSheetGrader(width, height)
    grader.sections = ROIS["bubble_sections"]

    # Read and resize image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (width, height))

    # Process multiple choice
    score, total, answers = grader.grade_test(img)

    # Process student ID
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)
    student_id = extract_id(thresh, ROIS["student_id"])

    # Process personal info and open questions
    all_rois = ROIS["personal_info"] + ROIS["open_questions"]
    personal_info, open_answers = extract_text_from_image(image_path, all_rois)

    return {
        "multiple_choice": {"score": score, "total": total, "answers": answers},
        "student_id": student_id,
        "personal_info": personal_info,
        "open_answers": open_answers,
        "image": img,
    }


if __name__ == "__main__":
    # Process answer sheet
    image_path = "./answers.jpg"
    results = process_answer_sheet(image_path)

    # Print results
    print("\n=== Answer Sheet Results ===")
    print(
        f"Multiple Choice Score: {results['multiple_choice']['score']}/{results['multiple_choice']['total']}"
    )
    print(f"Student ID: {''.join(map(str, results['student_id']))}")
    print("\nPersonal Information:")
    for info in results["personal_info"]:
        print(f"- {info}")
    print("\nOpen Answers:")
    for i, answer in enumerate(results["open_answers"], 1):
        print(f"Q{i}: {answer}")

    # Visualize all ROIs with different colors
    img_with_rois = visualize_rois(results["image"], ROIS)
    cv2.imshow("Answer Sheet with ROIs", img_with_rois)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
