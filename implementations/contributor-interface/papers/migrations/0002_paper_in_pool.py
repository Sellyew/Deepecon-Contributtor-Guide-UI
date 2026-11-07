from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("papers", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="paper",
            name="in_pool",
            field=models.BooleanField(
                default=False, verbose_name="open to all contributors",
                help_text="Every invited contributor may choose this paper and then sees its items (D-044). "
                          "Leave it off for a scored task unless any invited contributor may see its items; "
                          "offer it to individual contributors through assignments instead. Switching it off "
                          "stops new choices only: contributors who already chose the paper keep it (see "
                          "Assignments, 'Chosen by the contributor'); to withdraw access, delete those assignments."),
        ),
    ]
