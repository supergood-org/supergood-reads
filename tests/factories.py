import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional, Union

import factory
import factory.fuzzy
from django.conf import settings
from django.forms import Form
from faker import Faker

from supergood_review_site import models
from supergood_review_site.reviews.forms import ReviewFormGroup
from supergood_review_site.utils.forms import get_initial_field_value

fake = Faker()


class FactoryParam(str, Enum):
    """Distinguish an empty "completed_at" field from an explit completed_at=None."""

    UNSET_COMPLETED_AT = "UNSET_COMPLETED_AT"


class UserFactory(factory.django.DjangoModelFactory):
    """Fake User for test data generation."""

    username = factory.LazyFunction(fake.unique.name)
    email = factory.LazyFunction(fake.unique.email)
    is_staff = False

    class Meta:
        model = settings.AUTH_USER_MODEL


class BookFactory(factory.django.DjangoModelFactory):
    id = factory.LazyFunction(uuid.uuid4)
    title = factory.LazyFunction(fake.unique.sentence)
    author = factory.LazyFunction(fake.name)
    publication_year = factory.LazyFunction(lambda: int(fake.year()))

    class Meta:
        model = models.Book

    @factory.post_generation
    def genres(self, create, extracted):
        """
        Args:
          extracted:
            Optional list of genres passed into initial factory invocation.
            BookFactory.create(genres=(genre1, genre2, genre3))
        """
        if not create:
            return
        elif extracted:
            self.genres.add(*extracted)
        else:
            self.genres.add(GenreFactory())


class FilmFactory(factory.django.DjangoModelFactory):
    id = factory.LazyFunction(uuid.uuid4)
    title = factory.LazyFunction(fake.unique.sentence)
    director = factory.LazyFunction(fake.name)
    release_year = factory.LazyFunction(lambda: int(fake.year()))

    class Meta:
        model = models.Film

    @factory.post_generation
    def genres(self, create, extracted):
        """
        Args:
          extracted:
            Optional list of genres passed into initial factory invocation.
            FilmFactory.create(genres=(genre1, genre2, genre3))
        """
        if not create:
            return
        elif extracted:
            self.genres.add(*extracted)
        else:
            self.genres.add(GenreFactory())

    @factory.post_generation
    def countries(self, create, extracted):
        """
        Args:
          extracted:
            Optional list of countries passed into initial factory invocation.
            FilmFactory.create(genres=(country1, country2, country3))
        """
        if not create:
            return
        elif extracted:
            self.countries.add(*extracted)
        else:
            self.countries.add(CountryFactory())


class GenreFactory(factory.django.DjangoModelFactory):
    genre = factory.fuzzy.FuzzyChoice(
        ["Drama", "Comedy", "Horror", "Documentary", "Action"]
    )

    class Meta:
        model = models.Genre
        django_get_or_create = ("genre",)


class CountryFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.country)

    class Meta:
        model = models.Country
        django_get_or_create = ("name",)


class EbertStrategyFactory(factory.django.DjangoModelFactory):
    stars = factory.fuzzy.FuzzyDecimal(0, 4, 0)
    great_film = False

    class Meta:
        model = models.EbertStrategy


class GoodreadsStrategyFactory(factory.django.DjangoModelFactory):
    stars = factory.fuzzy.FuzzyInteger(0, 5)

    class Meta:
        model = models.GoodreadsStrategy


class MaximusStrategyFactory(factory.django.DjangoModelFactory):
    recommended = factory.fuzzy.FuzzyChoice([True, False, None])

    class Meta:
        model = models.MaximusStrategy


class ReviewFactory(factory.django.DjangoModelFactory):
    """Fake Review for test data generation.

    Includes an option to speed up test data generation by accepting a single
    "completed_at" datetime kwarg rather than forcing developers to enter
    completed_at_day, completed_at_month, and completed_at_year. Real Users submitting
    a non-factory Review would have to supply those 3 values.

    kwargs:
        completed_at: optional datetime that will be broken out into
          completed_at_day, completed_at_month, completed_at_year.

    Examples:
        Use today's date in completed_at* fields.
        r = ReviewFactory(completed_at=datetime.now())

        Set all completed_at* fields to None.
        r = ReviewFactory(completed_at=None)

        Set approximate date.
        r = ReviewFactory(completed_at_month=1, completed_at_year=1999)

        Let Faker choose a random date for you.
        r = ReviewFactory()
    """

    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    text = factory.LazyFunction(fake.unique.sentence)
    media_type = factory.SubFactory(BookFactory)
    strategy = factory.SubFactory(EbertStrategyFactory)

    @classmethod
    def _adjust_completed_at(cls, **kwargs: Any) -> Any:
        """Instructions for parsing a factory-only "completed_at" kwarg."""
        completed_at: Union[
            Optional[datetime], Literal[FactoryParam.UNSET_COMPLETED_AT]
        ] = kwargs.get("completed_at")

        unset_completed_at: bool = completed_at == FactoryParam.UNSET_COMPLETED_AT
        unset_completed_at_fields: bool = (
            "completed_at_day" not in kwargs
            and "completed_at_month" not in kwargs
            and "completed_at_year" not in kwargs
        )

        # If any completed_at* fields are set, then don't adjust them.
        if not unset_completed_at_fields:
            return kwargs

        # If any "completed_at" is explicitly set to None, then allow completed_at*
        # fields to be blank.
        if completed_at is None:
            return kwargs
        assert completed_at is not None

        # If "completed_at" is unset and the completed_at fields are also unset, then
        # fill in faker date values for them.
        if unset_completed_at and unset_completed_at_fields:
            completed_at = fake.date_time()
        assert isinstance(completed_at, datetime)

        kwargs["completed_at_day"] = completed_at.day
        kwargs["completed_at_month"] = completed_at.month
        kwargs["completed_at_year"] = completed_at.year

        return kwargs

    @classmethod
    def _adjust_kwargs(cls, **kwargs):
        kwargs = cls._adjust_completed_at(**kwargs)
        return kwargs

    class Meta:
        model = models.Review

    class Params:
        completed_at: Union[
            Optional[datetime], Literal[FactoryParam.UNSET_COMPLETED_AT]
        ] = FactoryParam.UNSET_COMPLETED_AT


class FormDataFactory:
    """
    Builds a data dictionary payload for form.
    """

    def __init__(self, form: Form):
        self.form = form
        self.data = self.build_data()

    def build_data(self) -> dict[str, str]:
        data = {}
        for key in self.form.fields.keys():
            if self.form.prefix:
                data_key = f"{self.form.prefix}-{key}"
            else:
                data_key = key
            value = get_initial_field_value(self.form, key)
            if value is None:
                form_field = self.form.fields[key]
                value = getattr(form_field, "empty_value", "") or ""
            elif isinstance(value, uuid.UUID):
                value = str(value)
            data.update({data_key: value})
        return data


class ReviewFormDataFactory:
    """
    Builds a data dictionary to populate a ReviewFormGroup.

    Pass in a review instance to populate your data dictionary with those values. This
    is useful for testing "update" operations.

    Omit a review instance to get a mostly-empty data dictionary filled with default
    initial values.
    """

    def __init__(self, instance: Optional[models.Review] = None) -> None:
        self.instance = instance
        self.review_form_group = ReviewFormGroup(instance=instance)
        self.data = self.build_data()

    def build_data(self) -> dict[str, Any]:
        data = {}

        review_form = self.review_form_group.review_form
        review_form_data = FormDataFactory(review_form).data
        data.update(review_form_data)

        review_mgmt_form = self.review_form_group.review_mgmt_form
        review_mgmt_form_data = FormDataFactory(review_mgmt_form).data
        data.update(review_mgmt_form_data)

        media_type_forms = (
            self.review_form_group.media_type_forms.by_content_type_id.values()
        )
        for form in media_type_forms:
            form_data = FormDataFactory(form).data
            data.update(form_data)

        strategy_forms = (
            self.review_form_group.strategy_forms.by_content_type_id.values()
        )
        for form in strategy_forms:
            form_data = FormDataFactory(form).data
            data.update(form_data)

        return data
