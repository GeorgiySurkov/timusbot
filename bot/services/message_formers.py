from aiogram.utils.markdown import escape_md

from ..models import GroupModel
from .parser.submission import Submission
from .parser.verdict import Verdict


async def form_leaderboard_message(group: GroupModel) -> str:
    await group.fetch_related('tracked_users')
    text = "Рейтинг по количеству решенных задач:\n"
    for i, user in sorted(group.tracked_users):
        # TODO: write correct form of word using pymorphy2
        text += f'{i}) {user.username} - {user.solved_problems_amount} задач'
    return text


def form_submission_message(submission: Submission) -> str:
    text = f'Задача {submission.problem.id}\. *{escape_md(submission.problem.name)}*\n'
    text += f'Отправил {submission.author.username}\n'
    text += f'Результат проверки:\n'
    if submission.verdict == Verdict.accepted:
        text += '✅ '
    else:
        text += '❌ '
    text += f'{submission.verdict.value}\n'
    text += f'_Язык:_ {escape_md(submission.language)}\n'
    if submission.test_number is not None:
        text += f'_№ теста:_ {submission.test_number}\n'
    if submission.runtime is not None:
        text += f'_Время работы:_ {submission.runtime} с\n'
    if submission.memory is not None:
        text += f'_Выделено памяти:_ {submission.memory} КБ\n'
    return text
