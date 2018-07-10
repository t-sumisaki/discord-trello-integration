import os
import json
import requests
from trello_models import TrelloWebhookBody


def webhook_to_discord(event, context):
    print('incoming webhook')

    # for webhook initialize
    if event.get('httpMethod') == 'HEAD':
        return {
            'statusCode': 200,
            'body': None
        }

    body = json.loads(event['body'])
    webhook_body = TrelloWebhookBody(**body)

    print(json.dumps(body, indent=2))

    print('Trello Action Type = {type}'.format(type=webhook_body.action.type))
    if webhook_body.action.type == 'createCard':
        post_to_discord(
            message='カードが追加されました',
            embeds=[webhook_body.get_embed_object()]
        )

    elif webhook_body.action.type == 'deleteCard':
        post_to_discord(
            message='カードが削除されました',
            embeds=[webhook_body.get_embed_object()]
        )

    elif webhook_body.action.type == 'updateCard':
        post_to_discord(
            message='カードが更新されました',
            embeds=[webhook_body.get_embed_object()]
        )

    elif webhook_body.action.type == 'commentCard':
        post_to_discord(
            message='カードにコメントが追加されました',
            embeds=[webhook_body.get_embed_object()]
        )
    elif webhook_body.action.type == 'updateCheckItemStateOnCard':
        post_to_discord(
            message='チェックリストが更新されました',
            embeds=[webhook_body.get_embed_object()]
        )

    else:
        print('not supported => {action_type}'.format(
            action_type=webhook_body.action.type))

    response = {
        "statusCode": 200,
        "body": json.dumps({})
    }

    return response


def post_to_discord(message='', embeds=[]):

    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    body = {
        'content': '{message}'.format(message=message),
        'embeds': embeds
    }

    r = requests.post(
        discord_webhook_url,
        json.dumps(body),
        headers={'Content-Type': 'application/json'})

    print('STATUS_CODE={status_code}'.format(status_code=r.status_code))

