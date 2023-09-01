# Generated by Django 4.2.3 on 2023-09-01 01:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import supergood_reads.models.review_strategies
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseMediaItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(db_index=True, default="", max_length=256)),
                (
                    "year",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MaxValueValidator(9999)],
                    ),
                ),
                ("created_at", models.DateTimeField()),
                (
                    "updated_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("validated", models.BooleanField(db_index=True, default=False)),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-updated_at",),
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="EbertStrategy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "stars",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=2,
                        null=True,
                        validators=[
                            supergood_reads.models.review_strategies.ebert_star_validator
                        ],
                    ),
                ),
                ("great_film", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Ebert",
            },
        ),
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="GoodreadsStrategy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "stars",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
            ],
            options={
                "verbose_name": "Goodreads",
            },
        ),
        migrations.CreateModel(
            name="ImdbStrategy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "score",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LetterboxdStrategy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "stars",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=2,
                        validators=[
                            supergood_reads.models.review_strategies.letterboxd_star_validator
                        ],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MaximusStrategy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("recommended", models.BooleanField()),
            ],
            options={
                "verbose_name": "Maximus",
            },
        ),
        migrations.CreateModel(
            name="UserReviewStrategyDefault",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "default_strategy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="strategy_user_default_set",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "media",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="media_user_default_set",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "completed_at_day",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(31),
                        ],
                    ),
                ),
                (
                    "completed_at_month",
                    models.PositiveIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                ("completed_at_year", models.IntegerField(blank=True, null=True)),
                ("text", models.TextField(blank=True, default="")),
                ("validated", models.BooleanField(db_index=True, default=False)),
                ("strategy_object_id", models.UUIDField(blank=True, null=True)),
                ("media_item_object_id", models.UUIDField(blank=True, null=True)),
                (
                    "media_item_content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="item_review_set",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "strategy_content_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="strategy_review_set",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": (
                    "-completed_at_year",
                    "-completed_at_month",
                    "-completed_at_day",
                    "-created_at",
                ),
                "indexes": [
                    models.Index(
                        fields=[
                            "completed_at_year",
                            "completed_at_month",
                            "completed_at_day",
                            "created_at",
                        ],
                        name="review_completed_at_idx",
                    ),
                    models.Index(
                        fields=["strategy_content_type", "strategy_object_id"],
                        name="supergood_r_strateg_fc52ec_idx",
                    ),
                    models.Index(
                        fields=["media_item_content_type", "media_item_object_id"],
                        name="supergood_r_media_i_968d1a_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Film",
            fields=[
                (
                    "basemediaitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="supergood_reads.basemediaitem",
                    ),
                ),
                ("director", models.CharField(default="", max_length=256)),
                ("countries", models.ManyToManyField(to="supergood_reads.country")),
                ("genres", models.ManyToManyField(to="supergood_reads.genre")),
            ],
            options={
                "verbose_name": "Film",
            },
            bases=("supergood_reads.basemediaitem",),
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "basemediaitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="supergood_reads.basemediaitem",
                    ),
                ),
                ("author", models.CharField(default="", max_length=256)),
                ("pages", models.IntegerField(blank=True, null=True)),
                ("genres", models.ManyToManyField(to="supergood_reads.genre")),
            ],
            options={
                "verbose_name": "Book",
            },
            bases=("supergood_reads.basemediaitem",),
        ),
    ]
