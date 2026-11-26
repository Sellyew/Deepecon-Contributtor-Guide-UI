"""Forms for the Submit page (M3). Field rules mirror submission-manifest.schema.json 0.3.0."""
from django import forms
from django.utils.translation import gettext_lazy as _

BLANK = [("", "—")]
CHANNELS = [("upload", _("Upload a ZIP file here")),
            ("public_reference", _("The package is public: give its reference (and upload only what is missing)")),
            ("other_agreed", _("Another channel agreed with the team (for example, for a very large package)"))]
YES_NO = [("", "—"), ("yes", _("Yes")), ("no", _("No"))]
RUN_TIMES = [("<10 minutes", _("less than 10 minutes")), ("10-60 minutes", _("10–60 minutes")),
             ("1-2 hours", _("1–2 hours")), ("2-8 hours", _("2–8 hours")), ("8-24 hours", _("8–24 hours")),
             ("1-3 days", _("1–3 days")), ("3-14 days", _("3–14 days")), (">14 days", _("more than 14 days"))]
AVAILABILITY = [("included", _("Included in my upload")), ("public_elsewhere", _("Public elsewhere")),
                ("restricted_not_included", _("Restricted: not included")),
                ("confidential_not_included", _("Confidential: not included"))]
ROUTES = [("author_runs_and_returns_outputs", _("I or my RA run the team's versions and return the outputs (no data)")),
          ("team_applies_for_access", _("The team applies to the provider for access")),
          ("secure_environment", _("A secure environment where authorized team members run it")),
          ("fully_synthetic_substitute", _("A fully synthetic substitute built from the codebook")),
          ("to_be_decided", _("To be decided"))]
COVERAGE = [("provided", _("Provided")), ("in_public_package", _("In the public package")),
            ("not_available", _("Not available")), ("not_applicable", _("Not applicable"))]
TEXT = 5000


def _tri(value):
    return {"yes": True, "no": False}.get(value)


def tri_initial(value):
    return {True: "yes", False: "no"}.get(value, "")


class SubmissionForm(forms.Form):
    channel = forms.ChoiceField(required=False, widget=forms.RadioSelect, label=_("How the materials reach us"))
    pub_repository = forms.CharField(required=False, max_length=200, label=_("Repository (for example openICPSR, Dataverse, Zenodo)"))
    pub_identifier = forms.CharField(required=False, max_length=200, label=_("Identifier"))
    pub_version = forms.CharField(required=False, max_length=100, label=_("Version"))
    pub_url = forms.URLField(required=False, max_length=500, label=_("URL (optional)"))
    pub_doi = forms.RegexField(required=False, max_length=200, regex=r"^10\.[0-9]{4,9}/\S+$", label=_("DOI (optional)"),
                               error_messages={"invalid": _("A DOI starts with 10. followed by a prefix and a suffix.")})
    other_channel_note = forms.CharField(required=False, max_length=TEXT, widget=forms.Textarea(attrs={"rows": 2}),
                                         label=_("Which channel, as agreed with the team"))
    master_script = forms.CharField(required=False, max_length=500, label=_("Master script (path in your package)"))
    readme = forms.CharField(required=False, max_length=500, label=_("README (path in your package)"))
    software = forms.CharField(required=False, max_length=2000, widget=forms.Textarea(attrs={"rows": 3}),
                               label=_("Software and versions, one per line, for example: Stata, 18"))
    dependencies_included = forms.ChoiceField(required=False, choices=YES_NO, label=_("User-written packages included or pinned"))
    author_run_log_included = forms.ChoiceField(required=False, choices=YES_NO, label=_("The log of your own complete run is included"))
    expected_outputs_included = forms.ChoiceField(required=False, choices=YES_NO, label=_("The outputs of that run are included"))
    run_time = forms.ChoiceField(required=False, choices=BLANK + RUN_TIMES, label=_("Expected run time"))
    hardware_note = forms.CharField(required=False, max_length=TEXT, widget=forms.Textarea(attrs={"rows": 2}),
                                    label=_("Hardware or memory it needs (optional)"))
    no_restricted_included = forms.BooleanField(required=False, label=_("I confirm that nothing restricted or confidential is included in what I send."))
    permission_to_share = forms.BooleanField(required=False, label=_("I confirm that I may share the data I include with the project."))
    version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)

    def __init__(self, *args, channels=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["channel"].choices = [c for c in CHANNELS if c[0] in channels]

    def clean_software(self):
        rows = []
        for line in self.cleaned_data["software"].splitlines():
            if not line.strip():
                continue
            name, sep, version = line.rpartition(",")
            if not sep or not name.strip() or not version.strip():
                raise forms.ValidationError(_("Write each line as name, version (for example: Stata, 18)."))
            rows.append({"name": name.strip()[:200], "version": version.strip()[:100]})
        return rows

    def values(self):
        data = {f: (v.strip() if isinstance(v, str) else v) for f, v in self.cleaned_data.items() if f != "version"}
        for field in ("dependencies_included", "author_run_log_included", "expected_outputs_included"):
            data[field] = _tri(data[field])
        return data


def software_text(rows):
    return "\n".join(f"{r['name']}, {r['version']}" for r in rows or [])


class DatasetForm(forms.Form):
    name = forms.CharField(max_length=300, label=_("Dataset"))
    source = forms.CharField(required=False, max_length=500, label=_("Source or provider"))
    terms = forms.CharField(required=False, max_length=500, label=_("Licence or terms of use"))
    availability = forms.ChoiceField(choices=BLANK + AVAILABILITY, label=_("Availability"))
    where = forms.CharField(required=False, max_length=500, label=_("Where it is (URL, DOI, or provider)"))
    access_route = forms.ChoiceField(required=False, choices=BLANK + ROUTES, label=_("How the team can still run the code"))
    notes = forms.CharField(required=False, max_length=TEXT, widget=forms.Textarea(attrs={"rows": 2}), label=_("Notes"))

    def clean(self):
        data = super().clean()
        availability = data.get("availability")
        if availability in ("restricted_not_included", "confidential_not_included") and not data.get("access_route"):
            self.add_error("access_route", _("Restricted or confidential data need a route, or 'To be decided'."))
        if availability == "public_elsewhere" and not (data.get("where") or "").strip():
            self.add_error("where", _("Say where the public data are."))
        if availability not in ("restricted_not_included", "confidential_not_included"):
            data["access_route"] = ""
        return data


DatasetFormSet = forms.formset_factory(DatasetForm, extra=1, can_delete=True, max_num=50, validate_max=True)


class ChecklistForm(forms.Form):
    """One status and one note per checklist entry configured for the paper."""

    def __init__(self, *args, entries=(), language="en", localize=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.entries = []
        for entry in entries:
            if entry.get("requirement") == "not_needed":
                continue
            status = forms.ChoiceField(required=False, choices=BLANK + COVERAGE, label=localize(entry["label"], language))
            note = forms.CharField(required=False, max_length=TEXT, widget=forms.TextInput, label=_("Note"))
            self.fields[f"status_{entry['id']}"] = status
            self.fields[f"note_{entry['id']}"] = note
            self.entries.append({"entry": entry, "status": f"status_{entry['id']}", "note": f"note_{entry['id']}",
                                 "help": localize(entry["help"], language) if entry.get("help") else "",
                                 "requirement": entry.get("requirement")})

    def answers(self):
        return {e["entry"]["id"]: (self.cleaned_data.get(e["status"]) or "", (self.cleaned_data.get(e["note"]) or "").strip())
                for e in self.entries}

    def bound_entries(self):
        return [{**e, "status_field": self[e["status"]], "note_field": self[e["note"]]} for e in self.entries]
