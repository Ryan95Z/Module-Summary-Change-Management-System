from abc import ABC, abstractmethod
from django.db.models import ForeignKey, ManyToManyField
from timeline.models import TimelineEntry
from timeline.models.integrate.entry import TLEntry


class BaseEntry(ABC):
    def __init__(self, model):
        self.model = model
        self.changes = None

    @abstractmethod
    def have_changes(self):
        pass

    @abstractmethod
    def content(self):
        pass

    def create_entry(self, **kwargs):
        parent = kwargs.get('parent', None)
        entry_type = kwargs.get('entry_type', 'Generic')
        status = kwargs.get('status', 'Draft')
        requested_by = kwargs.get('requested_by', None)

        if not self.have_changes():
            return None

        title = self.model.title()
        changes = self.content()
        module_code = self.get_module_code()
        object_id = self.model.pk
        content_object = self.model

        return TimelineEntry.objects.create(
            title=title,
            changes=changes,
            module_code=module_code,
            object_id=object_id,
            content_object=content_object,
            parent_entry=parent,
            entry_type=entry_type,
            status=status,
            changes_by=requested_by
        )

    def get_module_code(self):
        cls = self.model.__class__
        if not issubclass(cls, TLEntry):
            return self.model.module_code
        return self.model.module_code()

    def title(self):
        return self.model.title()


class InitEntry(BaseEntry):
    def __init__(self, model):
        super(InitEntry, self).__init__(model)

    def have_changes(self):
        return True

    def content(self):
        diff = self.model.differences()

        md = ""
        for field, changes in diff.items():
            field_str = field.replace("_", " ")
            updated = changes[1]

            field_type = self.model._meta.get_field(field)
            if isinstance(field_type, ForeignKey):
                key_object = field_type.rel.to
                updated = key_object.objects.get(pk=updated)

            if isinstance(field_type, ManyToManyField):
                continue

            md += "* {}: {}\n".format(field_str, updated)
        return md

    def sum_changes(self):
        return "{} has been created for {}".format(
            self.model.title(),
            self.get_module_code()
        )


class UpdateEntry(BaseEntry):
    def __init__(self, model):
        super(UpdateEntry, self).__init__(model)

    def get_differences(self):
        if self.changes is None:
            self.changes = self.model.differences()
        return self.changes

    def have_changes(self):
        return bool(self.get_differences())

    def content(self):
        diff = self.model.differences()
        md = ""
        for field, changes in diff.items():
            field_str = field.replace("_", " ")
            original = changes[0]
            updated = changes[1]

            field_type = self.model._meta.get_field(field)
            if isinstance(field_type, ForeignKey):
                key_object = field_type.rel.to
                original = key_object.objects.get(pk=original)
                updated = key_object.objects.get(pk=updated)

            if isinstance(field_type, ManyToManyField):
                continue

            md += "* {}: {} -> {}\n".format(field_str, original, updated)
        return md

    def sum_changes(self):
        n_changes = len(self.get_differences())
        return "There are {} changes to {}".format(
            n_changes, self.model.title()
        )
