from rest_framework import status
from rest_framework.response import Response


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            role = request.request.user.role

            print(role)

            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return Response(
                    f"User with role {role} is not authorized for this request. Only {allowed_roles} are authorized",
                    status=status.HTTP_403_FORBIDDEN,
                )

        return wrapper_func

    return decorator
