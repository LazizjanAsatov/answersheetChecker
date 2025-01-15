import cv2
from bubble import AnswerSheetGrader

if __name__ == "__main__":
    # Configuration
    path = "./answers.jpg"
    widthimg = 700
    heightimg = 700

    # Initialize grader
    grader = AnswerSheetGrader(widthimg, heightimg)

    # Read and grade the test
    img = cv2.imread(path)
    score, total, answers = grader.grade_test(img)

    # Print results
    print(f"Score: {score}/{total}")
    print("Student answers:", answers)
    print("Correct answers:", grader.correct_answers)
    print("Student answers detail:", grader.student_answers)
cv2.imshow("Image", img)
cv2.waitKey(0)