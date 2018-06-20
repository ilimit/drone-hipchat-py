#!/usr/bin/env python 
import sys, os, json, requests

VARS = [ 
        ('ROOM','ERROR'),
        ('TOKEN','ERROR'),
        ('NOTIFY', False),
        ('URL', 'https://api.hipchat.com/v2/'),
        ('FORMAT', 'html'),
        ]

CONFIG = dict()
for var_name, var_default in VARS:
    value=os.environ.get('PLUGIN_%s' % var_name, var_default)
    if value == 'ERROR': print('Var %s is required' % var_name)
    CONFIG[var_name]=value

if __name__ == '__main__':
    color = 'green' if os.environ.get('DRONE_BUILD_STATUS', 'success') else 'red'
    title = '%(DRONE_COMMIT_AUTHOR)s pushed to %(DRONE_REPO)s' % os.environ
    activity = 'Build launched <a href="%(DRONE_BUILD_LINK)s">%(DRONE_REPO)s</a> (%(DRONE_REPO_BRANCH)s)' % os.environ
    message = 'Last commit message: <a href="%(DRONE_COMMIT_LINK)s">%(DRONE_COMMIT_MESSAGE)s</a>' % os.environ

    card = dict(
            style = 'application',
            url = os.environ.get('CI_REPO_LINK'),
            format = 'medium',
            title = title,
            description = dict(
                format = 'html',
                value = message
                ),
            icon = dict(
                url = os.environ.get('CI_COMMIT_AUTHOR_AVATAR'),
                ),
            id = 'drone-hipchat-py',
            activity = dict(
                html = activity,
                icon = dict( url = '%s/favicon.png' % os.environ.get('CI_SYSTEM_LINK') ),
                )
            )

    full_message = title + '<br>' + activity + '<br>' + message

    requests.post(
        '%(URL)s/room/%(ROOM)s/notification?auth_token=%(TOKEN)s'  % CONFIG,
        data=json.dumps(dict(message=full_message, notify=CONFIG['NOTIFY'], message_format=CONFIG['FORMAT'], color=color, card=card )),
        headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
    )
