from app.models.team import SkillType, Team, Member
from rest_framework import serializers


class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    skill_type = SkillTypeSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ["id", "xp", "motivation", "stress", "skill_type"]


class TeamSerializer(serializers.ModelSerializer):
    member = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "member")

    def create(self, validated_data):
        tasks_data = validated_data.pop("member")
        team = Team.objects.create(**validated_data)
        for task_data in tasks_data:
            Member.objects.create(team=team, **task_data)
        return team
