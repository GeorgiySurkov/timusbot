from tortoise.models import Model
from tortoise import fields


class Group(Model):
    class Meta:
        table = 'group'
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=128)
    telegram_id = fields.IntField(unique=True, index=True)
    tracked_users = fields.ManyToManyField('models.TimusUser', related_name='tracked_in')


class TimusUser(Model):
    class Meta:
        table = 'timus_user'
    id = fields.IntField(pk=True)
    timus_id = fields.IntField()
