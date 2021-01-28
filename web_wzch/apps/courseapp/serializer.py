from rest_framework.serializers import ModelSerializer

from courseapp.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    """分类"""

    class Meta:
        model = CourseCategory
        fields = ['id', "name"]


class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', "name", "title", "signature", "image", "brief"]


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    # 返回课程列表所需的老师的信息
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", 'lesson_list']


class CourseDetailModelSerializer(ModelSerializer):
    """课程详情序列化器"""
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons","brief_html", "price", "teacher", "level_name","course_video"]


class CourseLessonModelSerializer(ModelSerializer):
    """课时序列化器"""

    class Meta:
        model = CourseLesson
        fields = ["id", "name", "free_trail","duration"]


class CourseChapterModelSerializer(ModelSerializer):
    """章节序列化器"""
    # 一对多 需要指定many=true

    #课时
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ["id", "name", "chapter", "coursesections"]
