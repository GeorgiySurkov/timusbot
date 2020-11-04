from tortoise.models import Model
from tortoise import fields


class GroupModel(Model):
    class Meta:
        table = 'group'
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True, index=True)
    tracked_users = fields.ManyToManyField('models.TimusUserModel', related_name='tracked_in')
    leaderboard_message_id = fields.IntField(null=True, default=None)


class TimusUserModel(Model):
    class Meta:
        table = 'timus_user'
    id = fields.IntField(pk=True)
    timus_id = fields.IntField(index=True)
    solved_problems_amount = fields.IntField(null=True, default=None)
    joined = fields.DatetimeField(auto_now_add=True)
