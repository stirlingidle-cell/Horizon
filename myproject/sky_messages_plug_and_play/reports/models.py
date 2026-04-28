# Author - Esa Ahmed W1989464

# Models used to store imported team registry data for reports such as departments names
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    department_head = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    team_leader = models.CharField(max_length=100, blank=True)
    jira_project_name = models.CharField(max_length=150, blank=True)
    github_repo = models.CharField(max_length=200, blank=True)
    focus_areas = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    downstream_dependencies = models.TextField(blank=True)
    dependency_type = models.CharField(max_length=100, blank=True)
    slack_channels = models.TextField(blank=True)
    team_wiki = models.CharField(max_length=200, blank=True)
    concurrent_projects = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.team_name
