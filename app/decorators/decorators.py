from rest_framework import status
from rest_framework.response import Response

from app.decorators.decorator_utils import roles_string_to_roles_list


def allowed_roles(allowed_roles=[]):
    def decorator(view_class):
        def wrapper_func(request, *args, **kwargs):

            if "all" in allowed_roles:
                return view_class(request, *args, **kwargs)

            roles = roles_string_to_roles_list(request.request.user.roles)

            # admin user can call any function
            if "admin" in roles:
                return view_class(request, *args, **kwargs)

            if any(role in roles for role in allowed_roles):
                return view_class(request, *args, **kwargs)
            else:
                return Response(
                    {
                        "message": f"User is not authorized for this request. This user has the roles {roles} but only {allowed_roles} are authorized"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        return wrapper_func

    return decorator
