# Generated by Django 3.0.7 on 2021-08-25 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topicblog', '0009_auto_20210214_0725'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicBlogTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_name', models.CharField(max_length=80)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TopicBlogItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(allow_unicode=True, blank=True)),
                ('item_sort_key', models.IntegerField()),
                ('servable', models.BooleanField(default=True)),
                ('published', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('header_image', models.ImageField(blank=True, upload_to='')),
                ('header_title', models.CharField(blank=True, max_length=80)),
                ('header_description', models.CharField(blank=True, max_length=120)),
                ('header_slug', models.CharField(blank=True, max_length=100)),
                ('item_type', models.CharField(choices=[('article', 'article'), ('project', 'project'), ('press_release', 'press_release'), ('newsletter', 'newsletter'), ('newsletter_web', 'newsletter_web'), ('petition', 'petition'), ('mailing_list_signup', 'mailing_list_signup')], default='article', max_length=100)),
                ('body_text_1_md', models.TextField(blank=True)),
                ('cta_1_slug', models.SlugField(blank=True)),
                ('cta_1_label', models.CharField(blank=True, max_length=100)),
                ('body_text_2_md', models.TextField(blank=True)),
                ('cta_2_slug', models.SlugField(blank=True)),
                ('cta_2_label', models.CharField(blank=True, max_length=100)),
                ('body_image', models.ImageField(blank=True, upload_to='')),
                ('body_image_alt_text', models.CharField(blank=True, max_length=100)),
                ('body_text_3_md', models.TextField(blank=True)),
                ('cta_3_slug', models.SlugField(blank=True)),
                ('cta_3_label', models.CharField(blank=True, max_length=100)),
                ('social_description', models.TextField(blank=True)),
                ('twitter_title', models.CharField(blank=True, max_length=80)),
                ('twitter_description', models.TextField(blank=True)),
                ('twitter_image', models.CharField(blank=True, max_length=100)),
                ('og_title', models.CharField(blank=True, max_length=80)),
                ('og_description', models.TextField(blank=True)),
                ('og_image', models.CharField(blank=True, max_length=100)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='topicblog.TopicBlogTemplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
