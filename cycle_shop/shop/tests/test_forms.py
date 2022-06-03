from django.test import TestCase

# Создайте ваши тесты здесь

from shop.form import PostForm


class PostFormTest(TestCase):
    def test_post_form_title_field_label(self):
        form = PostForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Наименование велосипеда')

    def test_post_form_category_field_label(self):
        form = PostForm()
        self.assertTrue(form.fields['category'].empty_label is None or form.fields[
            'category'].empty_label == 'Категория не выбрана')

    def test_post_form_description_field_label(self):
        form = PostForm()
        self.assertTrue(form.fields['description'].label is None or form.fields['description'].label == 'Описание')

    def test_post_form_price_field_label(self):
        form = PostForm()
        self.assertTrue(form.fields['price'].label is None or form.fields['price'].label == 'Цена велосипеда')

    def test_post_form_image_field_label(self):
        form = PostForm()
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'Картинка')

    def test_post_form_title_field_widget_placeholder(self):
        form = PostForm()
        self.assertEqual(form._meta.widgets['title'].attrs['placeholder'], 'Наименование велосипеда')

    def test_post_form_category_field_widget_placeholder(self):
        form = PostForm()
        self.assertEqual(form._meta.widgets['category'].attrs['placeholder'], 'Категория')

    def test_post_form_description_field_widget_placeholder(self):
        form = PostForm()
        self.assertEqual(form._meta.widgets['description'].attrs['placeholder'], 'Описание')

    def test_post_form_price_field_widget_placeholder(self):
        form = PostForm()
        self.assertEqual(form._meta.widgets['price'].attrs['placeholder'], 'Цена')

    def test_post_form_image_field_widget_no_placeholder(self):
        form = PostForm()
        self.assertFalse('placeholder' in form._meta.widgets['image'].attrs)
