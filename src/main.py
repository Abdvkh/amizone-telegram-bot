from rocketgram import Bot, Dispatcher, UpdatesExecutor, UpdateType, ChatType
from rocketgram import context, commonfilters, commonwaiters
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
        'under_construction': 'This section is under construction'
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
    await SendMessage(
        context.user.user_id,
        get_translation('enter_amizone_username')
    ).send()
    yield next()

    username = context.message.text
    await SendMessage(
        context.user.user_id,
        get_translation('got_username').format(username)
    ).send()

    await SendMessage(
        context.user.user_id,
        get_translation('enter_amizone_password')
    ).send()
    yield next()

    password = context.message.text
    await SendMessage(
        context.user.user_id,
        get_translation('got_password').format(password)
    ).send()
    await SendMessage(context.user.user_id, get_translation('logged'))


@router.handler
@commonfilters.command('/help')
async def help():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/update')
async def update():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/profile')
async def profile():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/timetable')
async def timetable():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/courses')
async def courses():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/faculties')
async def faculties():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/examResults')
async def exam_results():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


@router.handler
@commonfilters.command('/examSchedule')
async def exam_schedule():
    await SendMessage(context.user.user_id, get_translation('under_construction')).send()


UpdatesExecutor.run(bot)