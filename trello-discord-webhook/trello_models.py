import dateutil.parser
from pytz import timezone

class TrelloWebhookBody(object):

    def __init__(self, **kwargs):
        self.action = TrelloAction(**kwargs.get('action', {}))
        self.model = TrelloModel(**kwargs.get('model', {}))

    def get_embed_object(self):
        embed = {}

        embed['title'] = self.action.data.card.name
        embed['url'] = 'https://trello.com/c/{short_link}'.format(short_link=self.action.data.card.shortLink)

        if self.action.type == 'commentCard':
            embed['description'] = self.action.data.text
        
        elif self.action.type == 'updateCard':
            if 'idList' in self.action.data.old:
                embed['description'] = '[リスト移動]\n{before} -> {after}'.format(
                    before=self.action.data.listBefore.name, after=self.action.data.listAfter.name)
            if 'desc' in self.action.data.old:
                embed['description'] = '[詳細更新]\n{text}'.format(
                    text=self.action.data.card.desc
                )
            if 'idAttachmentCover' in self.action.data.old:
                embed['description'] = '画像が追加されました'
        
        elif self.action.type == 'updateCheckItemStateOnCard':
            # チェックリストアイテム更新時
            embed['description'] = '[{name}]\n - [{state}] {text}'.format(
                name=self.action.data.checklist.name,
                state='完了' if self.action.data.checkItem.state == 'complete' else '未完了',
                text=self.action.data.checkItem.name)

        elif self.action.type == 'addAttachmentToCard':
            embed['description'] = '[添付ファイル] {name}'.format(
                name=self.action.data.attachment.name
            )
            embed['image'] = {
                'url': self.action.data.attachment.url
            }
        
        embed['footer'] = {
            'text': 'Update by {username} ({time})'.format(
                username=self.action.memberCreator.fullName,
                time=self.action.date_jst)
        }

        return embed


class TrelloAction(object):

    def __init__(self, **kwargs):

        self.id = kwargs.get('id')
        self.idMemberCreator = kwargs.get('idMemberCreator')
        self.type = kwargs.get('type')
        self.date = kwargs.get('date')
        self.data = TrelloAction.Data(**kwargs.get('data', {}))
        self.memberCreator = TrelloAction.MemberCreator(
            **kwargs.get('memberCreator', {}))
        self.display = TrelloAction.Display(**kwargs.get('display', {}))

    @property
    def date_jst(self):
        if self.date is not None:
            d = dateutil.parser.parse(self.date).astimezone(timezone('Asia/Tokyo'))
            return d.strftime('%Y-%m-%d %H:%M:%S')
        
        return ''

    class MemberCreator(object):
        def __init__(self, **kwargs):
            self.id = kwargs.get('id')
            self.avatarHash = kwargs.get('avatarHash')
            self.fullName = kwargs.get('fullName')
            self.initials = kwargs.get('initials')
            self.username = kwargs.get('username')

    class Data(object):
        def __init__(self, **kwargs):
            self.board = TrelloAction.Data.Board(**kwargs.get('board', {}))
            self.card = TrelloAction.Data.Card(**kwargs.get('card', {}))
            self.list = TrelloAction.Data.List(**kwargs.get('list', {}))
            self.listAfter = TrelloAction.Data.List(**kwargs.get('listAfter', {}))
            self.listBefore = TrelloAction.Data.List(**kwargs.get('listBefore', {}))
            self.voted = kwargs.get('voted')
            self.text = kwargs.get('text')
            self.old = kwargs.get('old')
            self.checkItem = TrelloAction.Data.CheckItem(**kwargs.get('checkItem', {}))
            self.checklist = TrelloAction.Data.CheckList(**kwargs.get('checklist', {}))
            self.attachment = TrelloAction.Data.Attachment(**kwargs.get('attachment', {}))

        class Board(object):
            def __init__(self, **kwargs):
                self.shortLink = kwargs.get('shortLink')
                self.name = kwargs.get('name')
                self.id = kwargs.get('id')

        class Card(object):
            def __init__(self, **kwargs):
                self.shortLink = kwargs.get('shortLink')
                self.idShort = kwargs.get('idShort')
                self.name = kwargs.get('name')
                self.id = kwargs.get('id')
                self.desc = kwargs.get('desc')

        class List(object):
            def __init__(self, **kwargs):
                self.name = kwargs.get('name')
                self.id = kwargs.get('id')
        
        class CheckItem(object):
            def __init__(self, **kwargs):
                self.state = kwargs.get('state')
                self.name = kwargs.get('name')
                self.id = kwargs.get('id')
            
        class CheckList(object):
            def __init__(self, **kwargs):
                self.name = kwargs.get('name')
                self.id = kwargs.get('id')
        
        class Attachment(object):
            def __init__(self, **kwargs):
                self.url = kwargs.get('url')
                self.name = kwargs.get('name')
                self.id = kwargs.get('id')
                self.edgeColor = kwargs.get('edgeColor')
                self.previewUrl = kwargs.get('previewUrl')
                self.previewUrl2x = kwargs.get('previewUrl2x')

    class Display(object):
        def __init__(self, **kwargs):
            self.translationKey = kwargs.get('translationKey')
            self.entities = TrelloAction.Display.Entity(**kwargs.get('entities'))

        class Entity(object):
            def __init__(self, **kwargs):
                self.card = TrelloAction.Display.Entity.Card(**kwargs.get('card', {}))
                self.list = TrelloAction.Display.Entity.List(**kwargs.get('list', {}))
                self.memberCreator = TrelloAction.Display.Entity.MemberCreator(
                    **kwargs.get('memberCreator', {}))

            class Card(object):
                def __init__(self, **kwargs):
                    self.type = kwargs.get('type')
                    self.id = kwargs.get('id')
                    self.shortLink = kwargs.get('shortLink')
                    self.text = kwargs.get('text')

            class List(object):
                def __init__(self, **kwargs):
                    self.type = kwargs.get('type')
                    self.id = kwargs.get('id')
                    self.text = kwargs.get('text')

            class MemberCreator(object):
                def __init__(self, **kwargs):
                    self.type = kwargs.get('type')
                    self.id = kwargs.get('id')
                    self.username = kwargs.get('username')
                    self.text = kwargs.get('text')


class TrelloModel(object):

    def __init__(self, **kwargs):

        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.desc = kwargs.get('desc')

        self.closed = kwargs.get('closed')
        self.idOrganization = kwargs.get('idOrganization')
        self.pinned = kwargs.get('pinned')
        self.url = kwargs.get('url')
        self.shortUrl = kwargs.get('shortUrl')
