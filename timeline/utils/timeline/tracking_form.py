from timeline.models import TimelineEntry
from timeline.utils.timeline.factory import EntryFactory


def tracking_to_timeline(module_code, *args):
    processer = ProcessTrackingForm(*args)
    return processer.create_entries(module_code)


class ProcessTrackingForm(object):
    def __init__(self, *args):
        self.models = []

        for model in args:
            if isinstance(model, list):
                self.models += model
            else:
                self.models.append(model)

    def _object_type(self, model):
        if model.is_new:
            return "Init"
        return "Update"

    def prepare(self):
        entries = []
        for m in self.models:
            entry = self._object_type(m)
            entries.append(EntryFactory.makeEntry(entry, m))
        return entries

    def create_entries(self, module_code):
        entries = self.prepare()
        parent = ParentEntry(module_code, *entries)
        parent.create_master()


class ParentEntry(object):
    def __init__(self, module_code, *args):
        self.args = args
        self.module_code = module_code

    def create_master(self):
        title = "Changes to tracking form"
        content = "Changes to tracking form:\n\n"
        module_code = self.module_code
        object_id = 0
        content_object = None

        changes = 0

        for a in self.args:
            if a.have_changes():
                content += "* {}\n".format(a.sum_changes())
                changes += 1

        if changes > 0:
            master = TimelineEntry.objects.create(
                title=title,
                changes=content,
                module_code=module_code,
                object_id=object_id,
                content_object=content_object,
                entry_type='Tracking-Form'
            )

            for a in self.args:
                a.create_entry(master, 'Tracking-Form')