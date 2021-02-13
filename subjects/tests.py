from django.test import TestCase
from subjects import models, views

class SubjectTestCase(TestCase):
    def setUp(self):
        self.subject = models.Subject(name="Philosophy", exam_type="WAEC")

    def testSubect(self):
        self.assertEqual(self.subject.name, "Philosophy")
        self.assertEqual(self.subject.exam_type, "WAEC")

    def testPaper(self):
        paper = models.Paper(subject=self.subject, exam_year="2005")
        self.assertEqual(paper.subject, self.subject)
        self.assertEqual(paper.exam_year, "2005")
