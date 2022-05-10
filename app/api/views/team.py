from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.decorators.decorators import allowed_roles
from app.serializers.team import MemberSerializer, SkillTypeSerializer, TeamSerializer
from django.core.exceptions import ObjectDoesNotExist

from app.models.team import SkillType, Team, Member


@method_decorator(csrf_protect, name="dispatch")
class TeamViews(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles(["creator", "staff"])
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            print("Invalid")
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @allowed_roles(["creator", "staff"])
    def get(self, request, id=None):
        if id:
            item = Team.objects.get(id=id)
            serializer = TeamSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = Team.objects.all()
        serializer = TeamSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    @allowed_roles(["creator", "staff"])
    def patch(self, request, id=None):
        item = Team.objects.get(id=id)
        serializer = TeamSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    @allowed_roles(["creator", "staff"])
    def delete(self, request, id=None):
        item = get_object_or_404(Team, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


@method_decorator(csrf_protect, name="dispatch")
class MemberView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles(["creator", "staff"])
    def post(self, request):
        try:
            # Getting skill type from DB
            skill_type_str = request.data.get("skill_type")
            skill_type = SkillType.objects.get(name=skill_type_str)
        except ObjectDoesNotExist:
            return Response(
                {
                    "status": "error",
                    "data": {
                        "skill_type": f"'{skill_type_str}' is not a name of an existing skill-type in the database."
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            # Adding skill type to object
            member.skill_type = skill_type
            member.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @allowed_roles(["creator", "staff"])
    def get(self, request, id=None):
        if id:
            item = Member.objects.get(id=id)
            serializer = MemberSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = Member.objects.all()
        serializer = MemberSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    @allowed_roles(["creator", "staff"])
    def patch(self, request, id=None):
        item = Member.objects.get(id=id)
        serializer = MemberSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, id=None):
        item = get_object_or_404(Member, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})


@method_decorator(csrf_protect, name="dispatch")
class SkillTypeView(APIView):
    permission_classes = (IsAuthenticated,)

    @allowed_roles(["creator", "staff"])
    def post(self, request):
        print(request.data)

        serializer = SkillTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"status": "error", "data": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @allowed_roles(["creator", "staff"])
    def get(self, request, id=None):
        if id:
            item = SkillType.objects.get(id=id)
            serializer = SkillTypeSerializer(item)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )

        items = SkillType.objects.all()
        serializer = SkillTypeSerializer(items, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )

    @allowed_roles(["creator", "staff"])
    def patch(self, request, id=None):
        item = SkillType.objects.get(id=id)
        serializer = SkillTypeSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    @allowed_roles(["creator", "staff"])
    def delete(self, request, id=None):
        item = get_object_or_404(SkillType, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
