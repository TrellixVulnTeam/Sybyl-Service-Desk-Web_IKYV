from django.db import models
from django.conf import settings
from datetime import datetime, date

from company_management.models import Company
from user_management.models import User, UserTeamMember

from ckeditor.fields import RichTextField
# color palette import
from colorfield.fields import ColorField


# PRIORITIES
class Priority(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=255, blank=True)
    color = ColorField(default="#fff")
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# STATUS
class Status(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=255, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# ROLE
class Role(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=255, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# PROJECT
class Project(models.Model):
    name = models.CharField(max_length=100)
    project_status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    company = models.ManyToManyField(Company)
    description = RichTextField()
    project_code = models.CharField(max_length=255)
    estimated_cost = models.FloatField(default=0.00)
    final_cost = models.FloatField(null=True, blank=True)
    logo = models.FileField(null=True, blank=True, upload_to='logos/')
    thumbnail = models.CharField(max_length=100, null=True, blank=True)
    estimated_start_date = models.DateField(null=True, blank=True)
    estimated_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    @property
    def completion(self):
        completed           = Milestone.objects.filter(project_id=self.id, status='Completed').count()
        total_milestones    = Milestone.objects.filter(project_id=self.id).count()
        completion_level    = 0
        if total_milestones > 0:
            if completed > 0:
                completion_level  = round(((completed / total_milestones) * 100),2)
        return completion_level
    
    @property
    def task_completion(self):
        total_tasks         = Task.objects.filter(project_id=self.id).count()
        completed_tasks     = Task.objects.filter(project_id=self.id, status='Closed').count()
    
        completion_percet = 0
        if total_tasks > 0 and completed_tasks > 0:
            completion_percet = round(((completed_tasks / total_tasks) * 100),2)
        return completion_percet
    
    @property
    def incident_completion(self):
        total_incidents         = Incident.objects.filter(project_id=self.id).count()
        completed_incidents     = Incident.objects.filter(project_id=self.id, status='Closed').count()
    
        incident_completion_percet = 0
        if total_incidents > 0 and completed_incidents > 0:
            incident_completion_percet = round(((completed_incidents / total_incidents) * 100),2)
        return incident_completion_percet
    
    @property
    def milestone_count(self):
        milestone   = Milestone.objects.filter(project_id=self.id,status='Completed').count()
        milestone1  = Milestone.objects.filter(project_id=self.id).count()
        milestone_str = str(milestone) + '/' +str(milestone1)
        return milestone_str
    
    @property
    def task_count(self):
        task   = Task.objects.filter(project_id=self.id,status='Closed').count()
        task1  = Task.objects.filter(project_id=self.id).count()
        task_str = str(task) + '/' +str(task1)
        return task_str
    
    @property
    def incident_count(self):
        incident   = Incident.objects.filter(project_id=self.id,status='Closed').count()
        incident1  = Incident.objects.filter(project_id=self.id).count()
        incident_str = str(incident) + '/' +str(incident1)
        return incident_str
    
    @property
    def time_now(self):
        time = datetime.now()
        return time

    class Meta:
        db_table = 'project'


class ProjectTeam(models.Model):
    name = models.CharField(max_length=100)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectTeamMember(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    project_team = models.ManyToManyField(ProjectTeam)
    responsibility = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL )
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.member)


class ProjectDocument(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=50)
    document = models.FileField(upload_to='documents/projects/')
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ProjectAttachments
class ProjectAttachments(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'project_attachment'



class Milestone(models.Model):
    STATUS_CHOICES = (
        ('Open','Open'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Terminated', 'Terminated'),
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='New',
    )
    name                = models.CharField(max_length=100)
    description         = models.CharField(max_length=500, blank=True)
    startdate           = models.DateField(null=True, blank=True)
    enddate             = models.DateField(null=True, blank=True)
    actual_startdate    = models.DateField(null=True, blank=True)
    actual_enddate      = models.DateField(null=True, blank=True)
    project             = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    created_time        = models.DateTimeField(auto_now_add=True)
    creator             = models.ForeignKey(User, default=2, on_delete=models.CASCADE, related_name='milestone_creator')
    modified_time       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def completion(self):
        completed_tasks     = Task.objects.filter(milestone_id=self.id, status='Closed').count()
        total_tasks         = Task.objects.filter(milestone_id=self.id).count()
        completion_level    = 0
        if total_tasks > 0:
            if completed_tasks > 0:
                completion_level  = round(((completed_tasks / total_tasks) * 100),2)
        return completion_level

    @property
    def time_now(self):
        time = datetime.now()
        return time

    class Meta:
        ordering = ['enddate']


# MilestoneAttachment
class MilestoneAttachment(models.Model):
    milestone = models.ForeignKey(Milestone, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'milestone_attachment'


class Task(models.Model):
    STATUS_CHOICES      = (('Open', 'Open'), ('Ongoing', 'Ongoing'), ('Closed', 'Closed'))
    status              = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Open')
    name                = models.CharField(max_length=100)
    description         = models.CharField(max_length=500)
    project             = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    milestone           = models.ForeignKey(Milestone, on_delete=models.DO_NOTHING)
    start_date          = models.DateField(null=True, blank=True)
    end_date            = models.DateField(null=True, blank=True)
    actual_start_date   = models.DateField(null=True, blank=True)
    actual_end_date     = models.DateField(null=True, blank=True)
    created_time        = models.DateTimeField(auto_now_add=True)
    creator             = models.ForeignKey(User, default=2, on_delete=models.CASCADE, related_name='task_creator')
    modified_time       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'task'


# TaskAttachment
class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    attachment_name = models.CharField(max_length=45, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'task_attachment'


# Incident
class Incident(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField()
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, blank=True, null=True)
    assignee = models.ManyToManyField(ProjectTeamMember)
    creator = models.ForeignKey(ProjectTeamMember, on_delete=models.SET_NULL, null=True, related_name='incident_creator')
    image = models.ImageField(upload_to='images/incidents/', null=True, blank=True)
    document = models.FileField(upload_to='documents/incidents/', null=True, blank=True)
    resolution_time = models.DateTimeField(null=True, blank=True)
    reopen_time = models.DateTimeField(null=True, blank=True)
    close_time = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'incident'


# IncidentAttachment
class IncidentAttachment(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.DO_NOTHING)
    attachment_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'incident_attachment'


# IncidentComment
class IncidentComment(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'incident_comment'


# IncidentCommentAttachments
class IncidentCommentAttachments(models.Model):
    comment = models.ForeignKey(IncidentComment, on_delete=models.DO_NOTHING)
    attachment_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'incident_comment_attachment'


# IncidentCommentReply
class IncidentCommentReply(models.Model):
    comment = models.ForeignKey(IncidentComment, on_delete=models.DO_NOTHING)
    reply = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'incident_comment_reply'


# IncidentCommentReplyAttachment
class IncidentCommentReplyAttachment(models.Model):
    comment_reply = models.ForeignKey(IncidentCommentReply, on_delete=models.DO_NOTHING)
    attachment_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'incident_comment_reply_attachment'


# ProjectForum
class ProjectForum(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    forum_name = models.CharField(max_length=255, default=1)
    chat_room_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta():
        db_table = 'project_forum'


# ProjectForumMessages
class ProjectForumMessages(models.Model):
    projectforum = models.ForeignKey(ProjectForum, on_delete=models.DO_NOTHING)
    team_member = models.ForeignKey(ProjectTeamMember, on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    chat_message = RichTextField()

    class Meta():
        db_table = 'project_forum_messages'


# ProjectForumMessageAttachments
class ProjectForumMessageAttachments(models.Model):
    projectforummessage = models.ForeignKey(ProjectForumMessages, on_delete=models.DO_NOTHING)
    attachment_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'project_forum_message_attachments'


# ProjectForumMessageReplies
class ProjectForumMessageReplies(models.Model):
    projectforummessage = models.ForeignKey(ProjectForumMessages, on_delete=models.DO_NOTHING)
    team_member = models.ForeignKey(ProjectTeamMember, on_delete=models.DO_NOTHING)
    reply = RichTextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'project_forum_message_replies'


# ProjectForumMessageReplyAttachments
class ProjectForumMessageReplyAttachments(models.Model):
    projectforummessagereply = models.ForeignKey(ProjectForumMessageReplies, on_delete=models.DO_NOTHING)
    attachment_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'project_forum_message_reply_attachments'
