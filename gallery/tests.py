from django.test import TestCase
from django.urls import reverse
from .models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class GalleryViewTests(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='Nature')
        self.category2 = Category.objects.create(name='Animals')

        self.image1 = Image.objects.create(
            title='Sunset',
            image=SimpleUploadedFile('sunset.jpg', b'\x00\x00\x00', content_type='image/jpeg'),
            created_date=date.today(),
            age_limit=0,
        )
        self.image2 = Image.objects.create(
            title='Tiger',
            image=SimpleUploadedFile('tiger.jpg', b'\x00\x00\x00', content_type='image/jpeg'),
            created_date=date.today(),
            age_limit=12,
        )

        self.image1.categories.add(self.category1)
        self.image2.categories.add(self.category2)

    def test_gallery_view_status_code(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_gallery_view_context_contains_categories(self):
        response = self.client.get(reverse('main'))
        self.assertContains(response, self.category1.name)
        self.assertContains(response, self.image1.title)
        self.assertContains(response, self.category2.name)
        self.assertContains(response, self.image2.title)