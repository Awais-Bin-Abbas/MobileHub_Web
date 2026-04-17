# tasks/models.py
# This file defines how our data is stored in the database
# We use Django ORM → it turns these classes into database tables automatically

from django.db import models
from django.contrib.auth.models import User     # Django's built-in User (for login)


# ───────────────────────────────────────────────
# CATEGORY
# ───────────────────────────────────────────────
class Category(models.Model):
    """
    Categories help group tasks (like folders in phone apps)
    Example: Work, Personal, Shopping, Study
    """
    name = models.CharField(
        max_length=80,
        help_text="Short name for the category, e.g. Work"
    )

    def __str__(self):
        # This shows the name when we print the object or see it in admin
        return self.name

    class Meta:
        verbose_name_plural = "Categories"   # better looking name in admin
        ordering = ['name']                  # sort alphabetically


# ───────────────────────────────────────────────
# TASK
# ───────────────────────────────────────────────
class Task(models.Model):
    """
    The main thing users create — a single to-do item
    Each task belongs to exactly one user (only owner can see/edit it)
    """
    
    # Basic fields
    title = models.CharField(
        max_length=200,
        help_text="What needs to be done? e.g. Buy groceries"
    )
    
    description = models.TextField(
        blank=True,          # can be empty
        null=True,           # can be NULL in database
        help_text="Extra details (optional)"
    )
    
    # Date fields
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text="When should this be finished? (optional)"
    )
    
    # Status with only two choices (simple dropdown)
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('completed', 'Completed'),
    ]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Automatic timestamps
    created_at = models.DateTimeField(auto_now_add=True)   # set once when created
    updated_at = models.DateTimeField(auto_now=True)       # updated every save
    
    # Important relationships
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,           # if user deleted → delete their tasks
        related_name='tasks',               # allows user.tasks.all()
        help_text="The user who owns this task"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,          # if category deleted → task stays, category=None
        null=True,
        blank=True,
        related_name='tasks',
        help_text="Optional category/group"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']          # newest tasks first
        verbose_name = "Task"
        verbose_name_plural = "Tasks"