import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class TodoModel(Model):
    class Meta:
        table_name = os.environ.get('DYNAMODB_TABLE', 'todos')
        if os.environ.get('DYNAMODB_LOCAL') == 'true':
            host = 'http://localhost:8000'
        else:
            host = None

    todo_id = UnicodeAttribute(hash_key=True, null=False)
    text = UnicodeAttribute(null=False)
    checked = BooleanAttribute(null=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(TodoModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
