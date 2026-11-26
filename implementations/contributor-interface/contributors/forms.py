"""Forms for Selection (M2). Field rules mirror contributor-review.schema.json 0.3.0."""
from django import forms
from django.utils.translation import gettext_lazy as _

BLANK = [("", "—")]
TEXT_LIMIT = 5000

# Translated choices for the contributor's interface (the model's labels are for the team's admin).
VERDICTS = [("keep", _("Keep")), ("keep_with_changes", _("Keep with changes")), ("reject", _("Reject")), ("unsure", _("Unsure"))]
REJECT_REASONS = [("not_realistic", _("Not realistic")), ("not_consequential", _("Not consequential")),
                  ("repair_or_acceptable_work_wrong", _("Repair or acceptable work wrong")), ("other", _("Other"))]
VARIANTS = [("first", _("The first")), ("second", _("The second")), ("both", _("Both")), ("neither", _("Neither"))]
TRI_STATE = [("yes", _("Yes")), ("no", _("No")), ("unsure", _("Unsure"))]
ACCOUNT_KINDS = [("work", _("Work or business")), ("personal", _("Personal")), ("api", _("API")), ("unknown", _("Unknown"))]


class AIHelpMixin(forms.Form):
    """The per-answer AI disclosure (D-039; MVP §5.6 rule 2)."""

    ai_used = forms.BooleanField(required=False, label=_("AI helped with this"))
    ai_tool = forms.CharField(required=False, max_length=200, label=_("Which tool?"))
    ai_account_kind = forms.ChoiceField(required=False, label=_("Type of account"),
                                        choices=BLANK + ACCOUNT_KINDS)
    ai_entered_items = forms.BooleanField(required=False, label=_("I entered the items or the task package"))

    def clean_ai(self, data):
        if data.get("ai_used") and not data.get("ai_tool", "").strip():
            self.add_error("ai_tool", _("Please name the tool."))
        if not data.get("ai_used"):
            data.update(ai_tool="", ai_account_kind="", ai_entered_items=None)
        return data


class ReviewForm(AIHelpMixin):
    verdict = forms.ChoiceField(choices=VERDICTS)
    reject_reason = forms.ChoiceField(required=False, label=_("Main reason"),
                                      choices=BLANK + REJECT_REASONS)
    variant_choice = forms.ChoiceField(required=False, label=_("Which version should the task keep?"),
                                       choices=BLANK + VARIANTS)
    check_realistic = forms.ChoiceField(required=False, label=_("Realistic"), choices=BLANK + list(TRI_STATE))
    check_consequential = forms.ChoiceField(required=False, label=_("Consequential"), choices=BLANK + list(TRI_STATE))
    check_repair_correct = forms.ChoiceField(required=False, label=_("Repair correct"), choices=BLANK + list(TRI_STATE))
    suggested_title = forms.CharField(required=False, max_length=500, label=_("Suggested title"))
    suggested_description = forms.CharField(required=False, max_length=TEXT_LIMIT, widget=forms.Textarea(attrs={"rows": 3}),
                                            label=_("Suggested description"))
    other_valid_repairs = forms.CharField(required=False, max_length=TEXT_LIMIT, widget=forms.Textarea(attrs={"rows": 3}),
                                          label=_("Other valid repairs"))
    comment = forms.CharField(required=False, max_length=TEXT_LIMIT, widget=forms.Textarea(attrs={"rows": 3}),
                              label=_("Comment"))
    version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)

    def __init__(self, *args, paired=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not paired:
            del self.fields["variant_choice"]

    def clean(self):
        data = super().clean()
        verdict = data.get("verdict")
        if verdict == "keep_with_changes" and not any(
                data.get(f, "").strip() for f in ("suggested_title", "suggested_description", "other_valid_repairs", "comment")):
            self.add_error("comment", _("Please say what should change: a suggested title or description, other valid repairs, or a comment."))
        if verdict != "reject":
            data["reject_reason"] = ""
        return self.clean_ai(data)

    def review_data(self):
        """The cleaned values to store on the ItemReview."""
        fields = ["verdict", "reject_reason", "check_realistic", "check_consequential", "check_repair_correct",
                  "suggested_title", "suggested_description", "other_valid_repairs", "comment",
                  "ai_used", "ai_tool", "ai_account_kind", "ai_entered_items"]
        if "variant_choice" in self.fields:
            fields.append("variant_choice")
        return {f: (self.cleaned_data.get(f).strip() if isinstance(self.cleaned_data.get(f), str) else self.cleaned_data.get(f))
                for f in fields}


class ProposalForm(AIHelpMixin):
    category = forms.ChoiceField(label=_("Category"))
    location = forms.CharField(required=False, max_length=500, label=_("Where (file and lines, or section)"))
    description = forms.CharField(max_length=TEXT_LIMIT, widget=forms.Textarea(attrs={"rows": 4}),
                                  label=_("What would change"))
    why_it_matters = forms.CharField(required=False, max_length=TEXT_LIMIT, widget=forms.Textarea(attrs={"rows": 3}),
                                     label=_("Why it matters"))
    suggested_repair = forms.CharField(required=False, max_length=TEXT_LIMIT, widget=forms.Textarea(attrs={"rows": 3}),
                                       label=_("Suggested fix"))

    def __init__(self, *args, categories=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = list(categories) + [("unsure", _("Not sure"))]

    def clean(self):
        return self.clean_ai(super().clean())


class QuestionForm(forms.Form):
    text = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={"rows": 2}), label=_("Your question to the team"))
