# Generated by Django 4.2.3 on 2023-08-07 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("supergood_reads", "0004_alter_review_media_type_content_type_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="user",
            new_name="owner",
        ),
        migrations.RenameIndex(
            model_name="review",
            new_name="supergood_r_strateg_fc52ec_idx",
            old_name="supergood_r_strateg_4a320c_idx",
        ),
        migrations.RenameIndex(
            model_name="review",
            new_name="supergood_r_media_t_641efa_idx",
            old_name="supergood_r_media_t_508ea0_idx",
        ),
        migrations.AddField(
            model_name="book",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="film",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="text",
            field=models.TextField(blank=True, default=""),
        ),
    ]
