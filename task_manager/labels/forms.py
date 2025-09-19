from task_manager.labels.models import Labels
from task_manager.status.forms import CreateStatusForm


class CreateLabelForm(CreateStatusForm):
    class Meta:
        model = Labels
        fields = ['name']


class UpdateLabelForm(CreateLabelForm):
    pass
