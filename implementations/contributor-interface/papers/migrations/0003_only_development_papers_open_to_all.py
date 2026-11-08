"""Only demo or development papers can be open to all contributors (D-047).

Scored papers that were open to all (fictional demo data only, before D-047) are closed first.
Contributors who already chose them keep their assignments.
"""
from django.db import migrations, models

import papers.models


def close_scored_papers(apps, schema_editor):
    apps.get_model("papers", "Paper").objects.exclude(publication_status="demo_or_development").update(in_pool=False)


class Migration(migrations.Migration):
    dependencies = [("papers", "0002_paper_in_pool")]

    operations = [
        migrations.RunPython(close_scored_papers, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="paper",
            name="in_pool",
            field=models.BooleanField(default=False, help_text=papers.models.OPEN_TO_ALL_HELP,
                                      verbose_name="open to all contributors"),
        ),
        migrations.AddConstraint(
            model_name="paper",
            constraint=models.CheckConstraint(
                condition=models.Q(("in_pool", False), ("publication_status", "demo_or_development"), _connector="OR"),
                name="only_development_papers_open_to_all",
                violation_error_message=papers.models.OPEN_TO_ALL_RULE),
        ),
    ]
