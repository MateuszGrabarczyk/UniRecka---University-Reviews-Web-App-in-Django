from django.test import TestCase
from .utils import check_if_has_cursed_words 
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Review, University, ReviewHistory, Comment, CommentHistory

class CursedWordsTests(TestCase):
    def test_has_curse_words(self):
        self.assertTrue(check_if_has_cursed_words(["chuj", "white", "slowo"]))

    def test_has_no_curse_words(self):
        self.assertFalse(check_if_has_cursed_words(["pierwszy", "recenzja", "opinia"]))

class ReviewModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user and a university instance for use in tests
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.university = University.objects.create(name='Test University', voivodeship='Test Voivodeship', city='Test City', link='http://testuniversity.com')
    
    def test_create_review(self):
        review = Review.objects.create(
            title='Test Review',
            description='This is a test review description.',
            rating=5,
            university=self.university,
            user=self.user
        )
        self.assertEqual(review.title, 'Test Review')
        self.assertEqual(review.description, 'This is a test review description.')
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.active)

    def test_review_update_creates_history(self):
        review = Review.objects.create(
            title='Original Title',
            description='Original description.',
            rating=4,
            university=self.university,
            user=self.user
        )
        review.title = 'Updated Title'
        review.description = 'Updated description.'
        review.save()

        review_history = ReviewHistory.objects.last()
        self.assertIsNotNone(review_history)
        self.assertEqual(review_history.title, 'Original Title')
        self.assertEqual(review_history.description, 'Original description.')
        self.assertEqual(review_history.rating, 4)

    def test_review_deletion_sets_inactive(self):
        review = Review.objects.create(
            title='Review to Delete',
            description='This review will be set inactive.',
            rating=3,
            university=self.university,
            user=self.user
        )
        review_id = review.id
        review.delete()
        
        review = Review.objects.get(id=review_id)
        self.assertFalse(review.active)

    def test_string_representation(self):
        review = Review.objects.create(
            title='String Representation Test',
            description='Testing the string representation.',
            rating=5,
            university=self.university,
            user=self.user
        )
        self.assertEqual(str(review), 'String Representation Test')

class CommentModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user, university and review instance for use in tests
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.university = University.objects.create(name='Test University', voivodeship='Test Voivodeship', city='Test City', link='http://testuniversity.com')
        cls.review = Review.objects.create(
            title='Test Review',
            description='This is a test review description.',
            rating=5,
            university=cls.university,
            user=cls.user
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            description='This is a test comment.',
            review=self.review,
            user=self.user
        )
        self.assertEqual(comment.description, 'This is a test comment.')
        self.assertTrue(comment.active)

    def test_comment_update_creates_history(self):
        comment = Comment.objects.create(
            description='Original comment description.',
            review=self.review,
            user=self.user
        )
        comment.description = 'Updated comment description.'
        comment.save()

        comment_history = CommentHistory.objects.last()
        self.assertIsNotNone(comment_history)
        self.assertEqual(comment_history.description, 'Original comment description.')

    def test_comment_deletion_sets_inactive(self):
        comment = Comment.objects.create(
            description='Comment to be set inactive.',
            review=self.review,
            user=self.user
        )
        comment_id = comment.id
        comment.delete()

        updated_comment = Comment.objects.get(id=comment_id)
        self.assertFalse(updated_comment.active)

    def test_string_representation(self):
        comment = Comment.objects.create(
            description='Testing the string representation.',
            review=self.review,
            user=self.user
        )
        self.assertEqual(str(comment), 'Testing the string representation.')
