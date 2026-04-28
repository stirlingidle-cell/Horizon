import openpyxl
from django.core.management.base import BaseCommand
from reports.models import Department, Team


class Command(BaseCommand):
    help = "Import teams from team_registry.xlsx"

    def handle(self, *args, **kwargs):
        workbook = openpyxl.load_workbook("team_registry.xlsx")
        sheet = workbook.active

        count = 0

        for row in sheet.iter_rows(min_row=2, values_only=True):
            department_name = row[0]
            team_leader = row[1]
            department_head = row[2]
            team_name = row[3]
            jira_project_name = row[4]
            github_repo = row[5]
            focus_areas = row[6]
            skills = row[7]
            downstream_dependencies = row[8]
            dependency_type = row[9]
            slack_channels = row[10]
            team_wiki = row[11]
            concurrent_projects = row[12]

            if not team_name or not department_name:
                continue

            department, created = Department.objects.get_or_create(
                name=department_name,
                defaults={"department_head": department_head or ""}
            )

            Team.objects.create(
                department=department,
                team_name=team_name,
                team_leader=team_leader or "",
                jira_project_name=jira_project_name or "",
                github_repo=github_repo or "",
                focus_areas=focus_areas or "",
                skills=skills or "",
                downstream_dependencies=downstream_dependencies or "",
                dependency_type=dependency_type or "",
                slack_channels=slack_channels or "",
                team_wiki=team_wiki or "",
                concurrent_projects=concurrent_projects or "",
            )

            count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {count} teams successfully."))