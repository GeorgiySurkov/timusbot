from tortoise.models import Model
from tortoise import fields


class Group(Model):
    class Meta:
        table = 'group'
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True, index=True)
    tracked_users = fields.ManyToManyField('models.TimusUser', related_name='tracked_in')
    leaderboard_message_id = fields.IntField(null=True, default=None)


class TimusUser(Model):
    class Meta:
        table = 'timus_user'
    id = fields.IntField(pk=True)
    timus_id = fields.IntField()
