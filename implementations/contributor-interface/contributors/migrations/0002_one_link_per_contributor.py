"""Links belong to contributors, and each contributor has a current paper (D-044).

Each contributor keeps one link: their newest working one (neither revoked nor expired; if
none works, their newest one). Its paper becomes their current paper, so that link keeps
opening the paper it opened before. Their other working links are revoked, as P-060 (g)
requires, and each revocation is written to the event log.
"""
import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone

ACTOR = "migration contributors 0002"


def forward(apps, schema_editor):
    Invitation = apps.get_model("contributors", "Invitation")
    Contributor = apps.get_model("contributors", "Contributor")
    EventLog = apps.get_model("papers", "EventLog")
    now = timezone.now()
    for inv in Invitation.objects.select_related("assignment"):
        inv.contributor_id = inv.assignment.contributor_id
        inv.save(update_fields=["contributor"])
    for contributor in Contributor.objects.all():
        links = Invitation.objects.filter(contributor=contributor).order_by("-created_at", "-pk")
        working = links.filter(revoked_at__isnull=True, expires_at__gt=now)
        kept = working.first() or links.first()
        if kept is None:
            continue
        contributor.current_assignment_id = kept.assignment_id
        contributor.save(update_fields=["current_assignment"])
        for other in links.filter(revoked_at__isnull=True).exclude(pk=kept.pk):
            other.revoked_at = now
            other.save(update_fields=["revoked_at"])
            EventLog.objects.create(actor=ACTOR, operation="invitation_revoked", object_type="Invitation",
                                    object_id=f"invitation {other.pk}",
                                    details={"invitation_id": other.pk, "contributor_id": contributor.public_id,
                                             "kept_invitation_id": kept.pk})


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
