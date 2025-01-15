import cv2
import numpy as np


class AnswerSheetGrader:
    def __init__(self, width=700, height=700):
        self.width = width
        self.height = height
        self.student_answers = []
        self.min_threshold = 50  # Adjusted threshold for individual boxes

        # Define sections and their properties
        self.sections = [
            {"questions": 7, "choices": 5, "roi": (20, 255, 55, 200)},  # Questions 1-7
            {"questions": 7, "choices": 5, "roi": (79, 255, 48, 200)},  # Questions 8-14
            {
                "questions": 7,
                "choices": 5,
                "roi": (129, 255, 48, 200),
            },  # Questions 15-21
            {
                "questions": 7,
                "choices": 5,
                "roi": (184, 255, 48, 200),
            },  # Questions 22-28
            {
                "questions": 4,
                "choices": 5,
                "roi": (238, 255, 48, 110),
            },  # Questions 29-32
            {
                "questions": 3,
                "choices": 7,
                "roi": (238, 375, 65, 80),
            },  # Questions 33-35
        ]

        self.correct_answers = [
            [2, 2, 3, 2, 1, 2, 4],  # Questions 1-7
            [3, 2, 3, 2, 1, 2, 4],  # Questions 8-14
            [3, 2, 3, 2, 1, 2, 4],  # Questions 15-21
            [3, 2, 3, 2, 1, 2, 4],  # Questions 22-28
            [3, 2, 3, 2],  # Questions 29-32
            [3, 2, 3],  # Questions 33-35
        ]

    def get_box_answer(self, box):
        """Count non-zero pixels in a box"""
        try:
            pixel_count = cv2.countNonZero(box)
            return pixel_count
        except Exception as e:
            print(f"Error processing box: {e}")
            return 0

    def process_section(self, section, img_gray):
        """Process a single section of questions"""
        try:
            x, y, w, h = section["roi"]
            questions = section["questions"]
            choices = section["choices"]

            # Extract section ROI
            roi = img_gray[y : y + h, x : x + w]

            # Apply threshold to ROI
            _, thresh_roi = cv2.threshold(roi, 170, 255, cv2.THRESH_BINARY_INV)

            # Calculate box dimensions
            box_height = h // questions
            box_width = w // choices

            section_answers = []

            # Process each question
            for q in range(questions):
                question_answers = []
                y_start = q * box_height

                # Process each choice
                for c in range(choices):
                    x_start = c * box_width
                    box = thresh_roi[
                        y_start : y_start + box_height, x_start : x_start + box_width
                    ]
                    pixel_count = self.get_box_answer(box)
                    question_answers.append(pixel_count)

                # Count how many answers are marked (above threshold)
                marked_answers = sum(
                    1 for pixels in question_answers if pixels > self.min_threshold
                )

                # Handle different cases:
                # Case 1: No answer marked
                # Case 2: Multiple answers marked
                # Case 3: Exactly one answer marked (correct case)
                if marked_answers != 1:
                    marked_answer = 0  # Invalid answer (no mark or multiple marks)
                else:
                    # Get the single marked answer
                    marked_answer = question_answers.index(max(question_answers))

                section_answers.append(marked_answer)

            return section_answers

        except Exception as e:
            return [0] * section["questions"]

    def grade_test(self, img):
        try:
            img = cv2.resize(img, (self.width, self.height))
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)

            self.student_answers = []

            # Process each section
            for section in self.sections:
                section_answers = self.process_section(section, img_blur)
                self.student_answers.append(section_answers)

            # Calculate score
            score = 0
            total_questions = sum(len(section) for section in self.correct_answers)

            for student_section, correct_section in zip(
                self.student_answers, self.correct_answers
            ):
                for student_ans, correct_ans in zip(student_section, correct_section):
                    if student_ans == correct_ans:
                        score += 1

            return score, total_questions, self.student_answers

        except Exception as e:
            return 0, 0, []
