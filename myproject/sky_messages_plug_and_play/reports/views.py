from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Team
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def reports_home(request):
    return render(request, 'reports/reports_home.html')

@login_required
def team_count(request):
    total_teams = Team.objects.count()

    return render(request, 'reports/team_count.html', {
        'total_teams': total_teams
    })

@login_required
def team_count_pdf(request):
    from datetime import datetime

    teams = Team.objects.all().order_by('team_name')
    total_teams = teams.count()
    generated_date = datetime.now().strftime("%d %B %Y, %H:%M")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="team_count_report.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setTitle("Team Count Report")

    page_number = 1
    y = 800
    
    def draw_header():
        nonlocal y
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(70, 800, "Sky Engineering Team Count Report")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(70, 780, f"Generated: {generated_date}")
        pdf.drawString(70, 765, f"Total Teams: {total_teams}")

        y = 730

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(70, y, "No.")
        pdf.drawString(120, y, "Team Name")
        pdf.line(70, y - 5, 520, y - 5)

        y -= 25

    def draw_footer():
        pdf.setFont("Helvetica", 9)
        pdf.drawString(270, 30, f"Page {page_number}")

    draw_header()

    pdf.setFont("Helvetica", 10)

    for index, team in enumerate(teams, start=1):
        if y < 60:
            draw_footer()
            pdf.showPage()
            page_number += 1
            draw_header()
            pdf.setFont("Helvetica", 10)

        pdf.drawString(70, y, str(index))
        pdf.drawString(120, y, team.team_name[:60])
        y -= 20

    draw_footer()
    pdf.showPage()
    pdf.save()

    return response
@login_required
def team_summary_pdf(request):
    from datetime import datetime

    teams = Team.objects.select_related('department').all().order_by('team_name')
    generated_date = datetime.now().strftime("%d %B %Y, %H:%M")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="team_summary_report.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setTitle("Team Summary Report")

    page_number = 1
    y = 800

    def draw_header():
        nonlocal y
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 800, "Sky Engineering Team Summary Report")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 780, f"Generated: {generated_date}")

        y = 740

        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(50, y, "No.")
        pdf.drawString(85, y, "Team Name")
        pdf.drawString(240, y, "Department")
        pdf.drawString(390, y, "Team Leader")
        pdf.line(50, y - 5, 550, y - 5)

        y -= 22

    def draw_footer():
        pdf.setFont("Helvetica", 9)
        pdf.drawString(270, 30, f"Page {page_number}")

    draw_header()
    pdf.setFont("Helvetica", 8)

    for index, team in enumerate(teams, start=1):
        if y < 60:
            draw_footer()
            pdf.showPage()
            page_number += 1
            draw_header()
            pdf.setFont("Helvetica", 8)

        pdf.drawString(50, y, str(index))
        pdf.drawString(85, y, team.team_name[:28])
        pdf.drawString(240, y, team.department.name[:28])
        pdf.drawString(390, y, (team.team_leader or "No leader")[:28])

        y -= 18

    draw_footer()
    pdf.showPage()
    pdf.save()

    return response
@login_required
def teams_without_managers_pdf(request):
    from datetime import datetime

    teams = Team.objects.filter(
        Q(team_leader="") | Q(team_leader__isnull=True)
    ).order_by('team_name')
    generated_date = datetime.now().strftime("%d %B %Y, %H:%M")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="teams_without_managers.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setTitle("Teams Without Managers")

    page_number = 1
    y = 800

    def draw_header():
        nonlocal y
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(70, 800, "Teams Without Managers Report")

        pdf.setFont("Helvetica", 10)
        pdf.drawString(70, 780, f"Generated: {generated_date}")

        y = 740

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(70, y, "No.")
        pdf.drawString(120, y, "Team Name")
        pdf.line(70, y - 5, 500, y - 5)

        y -= 22

    def draw_footer():
        pdf.setFont("Helvetica", 9)
        pdf.drawString(270, 30, f"Page {page_number}")

    draw_header()
    pdf.setFont("Helvetica", 10)

    for index, team in enumerate(teams, start=1):
        if y < 60:
            draw_footer()
            pdf.showPage()
            page_number += 1
            draw_header()

        pdf.drawString(70, y, str(index))
        pdf.drawString(120, y, team.team_name[:60])

        y -= 20

    draw_footer()
    pdf.showPage()
    pdf.save()

    return response