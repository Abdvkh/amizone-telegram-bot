import importlib
amizone_core = importlib.import_module("amizone-api.core")

from core import User

from rocketgram import Bot, Dispatcher, UpdatesExecutor, UpdateType, ChatType
from rocketgram import context, commonfilters
from rocketgram import SendMessage
from rocketgram import make_waiter

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_API_TOKEN')

router = Dispatcher()
bot = Bot(token, router=router)

TRANSLATIONS = {
    'en': {
        'start': 'Hello {}! If you want to get your Amizone information, run /login.',
        'enter_amizone_username': 'Enter your amizone\'s username',
        'enter_amizone_password': 'Enter your amizone\'s password. By continuing, you agree that your information '
                                  'will be stored in the 3rd party storage!',
        'got_username': 'Your username is `{}`.',
        'got_password': 'Your password is `{}`.',
        'logged': 'You are successfully logged in!',
        'information_updated': 'Your information was successfully updated!',
        'under_construction': 'This section is under construction',
        'went_wrong': 'Something went wrong!',
        'information_update': 'Your information is updated successfully!',
        'process': 'Being processed...'
    }
}


def get_translation(keyword, language='en'):
    return TRANSLATIONS[language][keyword]


@router.handler
@commonfilters.command('/start')
async def start_command():
    msg = get_translation('start').format(context.message.user.first_name)
    await SendMessage(context.user.user_id, msg).send()


@make_waiter
@commonfilters.update_type(UpdateType.message)
@commonfilters.chat_type(ChatType.private)
def next():
    return True


@router.handler
@commonfilters.command('/login')
async def auth():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)

    await SendMessage(
        user_telegram_id,
        get_translation('enter_amizone_username')
    ).send()
    yield next()

    username = context.message.text
    user.set_property('username', username)

    await SendMessage(
        user_telegram_id,
        get_translation('got_username').format(username)
    ).send()

    await SendMessage(
        user_telegram_id,
        get_translation('enter_amizone_password')
    ).send()
    yield next()

    password = context.message.text
    user.set_property('password', password)

    await SendMessage(
        user_telegram_id,
        get_translation('got_password').format(password)
    ).send()
    await SendMessage(
        user_telegram_id,
        get_translation('got_password').format(password)
    ).send()

    login = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    if login:
        msg = get_translation('logged')
    else:
        msg = get_translation('went_wrong')

    await SendMessage(user_telegram_id, msg).send()


@router.handler
@commonfilters.command('/help')
async def help():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/profile')
async def profile():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)
    amizone = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    profile_information = '\n'.join(amizone.get_profile().values())

    await SendMessage(user_telegram_id, profile_information).send()


@router.handler
@commonfilters.command('/timetable')
async def timetable():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)
    amizone = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    timetable_information = amizone.get_timetable()
    msg = '\n'.join([' | '.join(information.values()) for information in timetable_information])

    await SendMessage(context.user.user_id, msg).send()


@router.handler
@commonfilters.command('/courses')
async def courses():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)

    amizone = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    courses_information = amizone.get_courses()
    msg = '\n'.join([' | '.join(course_information.values()) for course_information in courses_information])

    await SendMessage(context.user.user_id, msg).send()


@router.handler
@commonfilters.command('/faculties')
async def faculties():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)

    amizone = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    faculties_information = amizone.get_faculties()
    msg = '\n'.join([' | '.join(faculty_information.values()) for faculty_information in faculties_information])

    await SendMessage(context.user.user_id, msg).send()


@router.handler
@commonfilters.command('/examResults')
async def exam_results():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/examSchedule')
async def exams_schedule():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)

    amizone = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    exams_schedule_information = amizone.get_exam_schedule()
    msg = '\n'.join([' | '.join(exam_schedule_information.values()) for exam_schedule_information in exams_schedule_information])

    await SendMessage(context.user.user_id, msg).send()


@router.handler
@commonfilters.command('/update')
async def update_information():
    user_telegram_id = context.user.user_id
    user = User(user_telegram_id)
    amizone = amizone_core.Amizone(user.get_property('username'), user.get_property('password'))

    await SendMessage(context.user.user_id, get_translation('process')).send()

    amizone.update()
    await SendMessage(context.user.user_id, get_translation('information_updated')).send()

UpdatesExecutor.run(bot)