from rest_framework import serializers

from subtasks.models import Subtask
from tags.models import Tag
from tasks.models import Task, Category
from users.models import User


class TasksSlugRelatedField(serializers.SlugRelatedField):
    def __init__(self, manager=None, **kwargs):
        assert manager is not None, 'The `manager` argument is required.'
        self.manager = manager
        super().__init__(**kwargs)

    def get_queryset(self):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return self.manager.for_user(request.user)
        return self.manager.none()


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['name', 'is_completed']


class TaskSerializer(serializers.ModelSerializer):
    category = TasksSlugRelatedField(
        manager = Category.objects,
        slug_field='slug'
    )
    tags = TasksSlugRelatedField(
        manager=Tag.objects,
        slug_field='name',
        many=True,
        required=False
    )
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        tags_data = validated_data.pop('tags', [])

        task = Task.objects.create(**validated_data)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, user=task.user, **subtask_data)
        task.tags.set(tags_data)
        return task

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        subtasks_data = validated_data.pop('subtasks', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        if subtasks_data is not None:
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, user=instance.user, **subtask_data)

        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
