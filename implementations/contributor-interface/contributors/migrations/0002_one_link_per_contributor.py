"""Links belong to contributors, and each contributor has a current paper (D-044).

Existing links keep opening the paper they opened before: each contributor's current paper
becomes the assignment of their most recent invitation.
"""
import django.db.models.deletion
from django.db import migrations, models


def forward(apps, schema_editor):
    Invitation = apps.get_model("contributors", "Invitation")
    Contributor = apps.get_model("contributors", "Contributor")
    for inv in Invitation.objects.select_related("assignment"):
        inv.contributor_id = inv.assignment.contributor_id
        inv.save(update_fields=["contributor"])
    for contributor in Contributor.objects.all():
        latest = (Invitation.objects.filter(contributor=contributor).order_by("-created_at", "-pk")
                  .select_related("assignment").first())
        if latest is not None:
            contributor.current_assignment_id = latest.assignment_id
            contributor.save(update_fields=["current_assignment"])


def backward(apps, schema_editor):
    Invitation = apps.get_model("contributors", "Invitation")
    Assignment = apps.get_model("contributors", "Assignment")
    for inv in Invitation.objects.select_related("contributor"):
        assignment_id = inv.contributor.current_assignment_id or (
            Assignment.objects.filter(contributor_id=inv.contributor_id).order_by("created_at")
            .values_list("pk", flat=True).first())
        if assignment_id is None:
            inv.delete()            # a link of a contributor with no paper has nowhere to point
        else:
            inv.assignment_id = assignment_id
            inv.save(update_fields=["assignment"])


class Migration(migrations.Migration):
    dependencies = [("contributors", "0001_initial"), ("papers", "0002_paper_in_pool")]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="added_by",
            field=models.CharField(choices=[("team", "Offered by the team"),
                                            ("contributor", "Chosen by the contributor from the papers open to all")],
                                   default="team", max_length=16),
        ),
        migrations.AlterField(
            model_name="assignment",
            name="relationship_to_paper",
            field=models.CharField(choices=[("author", "Author of the paper"), ("invited_expert", "Invited expert")],
                                   help_text="Only the team records authorship.", max_length=32),
        ),
        migrations.AddField(
            model_name="contributor",
            name="current_assignment",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name="+", to="contributors.assignment", verbose_name="current paper",
                                    help_text="The paper the contributor's link opens (D-044)."),
        ),
        migrations.AddField(
            model_name="invitation",
            name="contributor",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name="invitations", to="contributors.contributor"),
        ),
        migrations.AlterField(
            model_name="invitation",
            name="assignment",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name="invitations", to="contributors.assignment"),
        ),
        migrations.RunPython(forward, backward),
        migrations.RemoveField(model_name="invitation", name="assignment"),
        migrations.AlterField(
            model_name="invitation",
            name="contributor",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name="invitations", to="contributors.contributor"),
        ),
    ]
