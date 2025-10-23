from django.contrib.auth import password_validation
from django.core import exceptions
from django.utils.text import slugify
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
            instance_subtasks = {sub.name: sub for sub in instance.subtasks.all()}

            for subtask in subtasks_data:
                subtask_name = subtask["name"]
                if subtask_name not in instance_subtasks.keys():
                    instance.subtasks.create(task=instance, user=instance.user, **subtask)
                else:
                    instance_subtasks.pop(subtask_name)
                    Subtask.objects.filter(name=subtask_name).update(**subtask)

            for subtask in instance_subtasks.values():
                subtask.delete()

        return instance

    def validate(self, data):
        user = self.context['request'].user
        if 'slug' in data:
            if Task.objects.filter(user=user, slug=data['slug']).exists():
                raise serializers.ValidationError({'slug': 'A slug must be unique.'})
        else:
            if not self.instance and 'name' in data:
                slug = slugify(data['name'])
                if Task.objects.filter(user=user, slug=slug).exists():
                    raise serializers.ValidationError({'name': 'A slug for this name already exists.'})

        if 'subtasks' in data:
            subtask_names = [sub['name'] for sub in data['subtasks']]
            if len(subtask_names) != len(set(subtask_names)):
                raise serializers.ValidationError({
                    'subtasks': 'The list of subtasks must not contain duplicates.'
                })

        if 'tags' in data:
            tags = data['tags']
            if len(tags) != len(set(tags)):
                raise serializers.ValidationError({
                    'tags': 'The list of tags must not contain duplicates.'
                })

        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation

    def validate(self, data):
        user = self.context['request'].user
        if 'slug' in data:
            if Category.objects.filter(user=user, slug=data['slug']).exists():
                raise serializers.ValidationError("A slug must be unique.")
        else:
            if not self.instance and 'name' in data:
                slug = slugify(data['name'])
                if Category.objects.filter(user=user, slug=slug).exists():
                    raise serializers.ValidationError("A slug for this name already exists.")
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation

    def validate_name(self, value):
        user = self.context['request'].user
        if Tag.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("A name must be unique.")
        return value


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

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = dict()

        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)
