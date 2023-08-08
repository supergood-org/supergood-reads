from typing import Any, Literal, Union

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser, User
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect

from supergood_reads.media_types.models import AbstractMediaType
from supergood_reads.reviews.models import Review


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class BasePermissionMixin:
    def login_redirect(self) -> HttpResponse:
        return redirect("401")

    def forbidden_redirect(self) -> HttpResponse:
        return redirect("403")

    def has_perm_dynamic(
        self, user: User, obj: Model, perm: Literal["view", "add", "change", "delete"]
    ) -> bool:
        """
        Test user permissions for any object and any base permission.

        Example:
          has_perm_dynamic(user, book, "view")
          Returns:
            user.has_perm("supergood_reads.view_book", book)
        """
        perm_string = f"{obj._meta.app_label}.{perm}_{obj._meta.model_name}"
        return user.has_perm(perm_string, obj)

    def has_owner_permission(
        self,
        user: Union[AbstractBaseUser, AnonymousUser],
        obj: AbstractMediaType | Review,
    ) -> bool:
        return user.is_authenticated and obj.owner == user


class CreateReviewPermissionMixin(BasePermissionMixin):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        messages.info(
            self.request,
            (
                "This is just a demo form, you can't submit it. If you want to create or "
                "update your own reviews, please sign in!"
            ),
        )
        return super().get(request, *args, **kwargs)  # type: ignore

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """Only allow authenticated users to create new Reviews."""
        user = request.user
        if not user.is_authenticated or not user.has_perm("supergood_reads.add_review"):
            if not user.is_authenticated:
                return self.login_redirect()
            else:
                return self.forbidden_redirect()
        return super().post(request, *args, **kwargs)  # type: ignore


class UpdateReviewPermissionMixin(BasePermissionMixin):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """
        A user can only view the update page for a review only if one of these
        conditions is met:
          - The review is a demo review
          - The user has a global "view_review" permission and is_staff
          - The user owns the Review
        """
        user = request.user
        obj = self.get_object()  # type: ignore
        if not (
            obj.is_demo()
            or (user.has_perm("supergood_reads.view_review") and user.is_staff)
            or self.has_owner_permission(user, obj)
        ):
            if not user.is_authenticated:
                return self.login_redirect()
            else:
                return self.forbidden_redirect()

        messages.info(
            self.request,
            (
                "This is just a demo form, you can't submit it. If you want to create or "
                "update your own reviews, please sign in!"
            ),
        )
        return super().get(request, *args, **kwargs)  # type: ignore

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """
        A user can only update a review if one of these conditions is met:
          - The user has global "change_review" permission and is_staff
          - The user owns the Review
        """
        user = request.user
        obj = self.get_object()  # type: ignore
        if not (
            (user.has_perm("supergood_reads.change_review") and user.is_staff)
            or self.has_owner_permission(user, obj)
        ):
            if not user.is_authenticated:
                return self.login_redirect()
            else:
                return self.forbidden_redirect()
        return super().post(request, *args, **kwargs)  # type: ignore


class UpdateMediaPermissionMixin(BasePermissionMixin):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        """Check if user is allowed to change MediaType instance."""
        user = request.user
        obj = self.get_object()  # type: ignore
        if not obj.can_user_change(user):
            if not user.is_authenticated:
                message = (
                    f"This is just a demo {obj._meta.verbose_name}. If you'd "
                    f"like to create and edit your own {obj._meta.verbose_name_plural},"
                    f" you can login."
                )
                return HttpResponse(message, status=401)
            else:
                return HttpResponseForbidden()
        return super().post(request, *args, **kwargs)  # type: ignore
