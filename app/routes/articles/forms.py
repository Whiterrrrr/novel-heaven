from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

# 分类选项配置
CATEGORY_CHOICES = [
    ('fantasy', '玄幻'),
    ('romance', '言情'), 
    ('sci-fi', '科幻'),
    ('mystery', '悬疑')
]

class ArticleForm(FlaskForm):
    title = StringField('文章标题', validators=[
        DataRequired(message='标题不能为空'),
        Length(max=100, message='标题长度不能超过100字符')
    ])
    
    category = SelectField(
        '文章分类',
        choices=CATEGORY_CHOICES,
        validators=[DataRequired(message='请选择分类')]
    )
    
    content = TextAreaField('内容', validators=[
        DataRequired(message='内容不能为空'),
        Length(min=500, message='内容至少需要500字')
    ])
    
    save_as_draft = BooleanField('保存为草稿')
    submit = SubmitField('立即发布')
    
class ChapterForm(FlaskForm):
    chapter_title = StringField('章节标题', validators=[
        DataRequired(),
        Length(max=100)
    ])
    content = CKEditorField('正文内容', validators=[
        DataRequired(),
        Length(min=1000)
    ])