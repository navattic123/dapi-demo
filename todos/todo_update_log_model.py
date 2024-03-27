import os
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
from pynamodb.models import Model


class TodoUpdateLogModel(Model):
    class Meta:
        table_name = os.environ.get('DYNAMODB_TABLE', 'todo_update_log')
        if os.environ.get('DYNAMODB_LOCAL') == 'true':
            host = 'http://localhost:8000'
        else:
            host = None

    update_id = UnicodeAttribute(hash_key=True, null=False)
    todo_id = UnicodeAttribute(null=False)
    action_id = UnicodeAttribute(null=False)
    action_type = UnicodeAttribute(null=False)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now())
    updatedAt = UTCDateTimeAttribute(null=False)
    user_id = UnicodeAttribute(hash_key=False, null=False)

    def save(self, conditional_operator=None, **expected_values):
        self.updatedAt = datetime.now()
        super(TodoUpdateLogModel, self).save()

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))