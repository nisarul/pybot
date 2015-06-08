import tgl
from telex.DatabaseMixin import DatabaseMixin, DbType
from telex import auth
from telex.utils.decorators import group_only
from datetime import datetime
from telex import plugin



class QuotesPlugin(plugin.TelexPlugin, DatabaseMixin):
    """
    Store and retrieve quotes from a database.
    """

    patterns = {
        "^!quote$": "get_random_quote",
        "^!addquote (.*)": "add_quote",
        "^!quotethis$": "add_reply",
        "^!delquote ([0-9]+)$": "del_quote",
        "^!getquote ([0-9]+)$": "get_quote",
        "^!findquote (.*)": "find_quote",
    }

    usage = [
        "!quote: return random quote",
        "!addquote Text To Quote: add quote",
        "!quotethis: Add quote from a reply",
        "!findquote Text To Search: Search quote list, returning up to 5 answers",
        "!getquote [quote_id]: Get specific quote by id",
        "!delquote [quote_id]: (Admin) Delete quote from database",
    ]

    schema = {
        'quote_id': DbType.Integer,
        'timestamp': DbType.DateTime,
        'chat_id': DbType.Integer,
        'uid': DbType.Integer,
        'username': DbType.String,
        'full_name': DbType.String,
        'quote': DbType.String,
    }

    primary_key = 'quote_id'

    def __init__(self):
        super().__init__()
        DatabaseMixin.__init__(self)

    @group_only
    def add_quote(self, msg, matches):
        try:
            quote = matches.group(1)
        except AttributeError:
            quote = matches
        if hasattr(msg.src, 'username'):
            username = msg.src.username
        self.insert(timestamp=msg.date,
                    uid=msg.src.id, username=username,
                    full_name="{0} {1}".format(msg.src.first_name or '', msg.src.last_name or ''),
                    chat_id=msg.dest.id, quote=quote)
        return "Done!"

    @group_only
    def get_quote(self, msg, matches):
        chat_id = msg.dest.id
        quote_id = matches.group(1)
        results = self.query("SELECT * FROM {0} "
                             "WHERE chat_id = {1} and quote_id = ? LIMIT 1".format(self.table_name, chat_id), parameters=(quote_id,))
        if len(results) == 0:
            return "No such quote in the database for this channel!"
        result = results[0]
        text = "{quote} ({qid} Added By {name} on {date})\n".format(quote=result["quote"],
                                                                    name=result["full_name"],
                                                                    date=datetime.strptime(result["timestamp"], "%Y-%m-%d %H:%M:%S").date().isoformat(),
                                                                    qid=result["quote_id"])
        return text

    @group_only
    def find_quote(self, msg, matches):
        chat_id = msg.dest.id
        search = matches.group(1)
        results = self.query("SELECT * FROM {0} "
                             "WHERE chat_id = {1} and quote LIKE ? LIMIT 5".format(self.table_name, chat_id), parameters=("%{0}%".format(search),))

        if len(results) == 0:
            return "No such quote in the database for this channel!"

        text = "Quotes containing '{0}':\n".format(search)
        for result in results:
          text += "{quote} ({qid} Added By {name} on {date})\n".format(quote=result["quote"],
                                                                       name=result["full_name"],
                                                                       date=datetime.strptime(result["timestamp"], "%Y-%m-%d %H:%M:%S").date().isoformat(),
                                                                       qid=result["quote_id"])
        return text

    @auth.authorize(groups=['admins'])
    @group_only
    def del_quote(self, msg, matches):
        chat_id = msg.dest.id
        quote_id = matches.group(1)
        results = self.query("SELECT * FROM {0} "
                             "WHERE chat_id = {1} and quote_id = ? LIMIT 1".format(self.table_name, chat_id), parameters=(quote_id,))
        if len(results) == 0:
            return "No such quote in the database for this channel!"
        else:
            self.query("DELETE FROM {0} "
                       "WHERE chat_id = {1} and quote_id = ? LIMIT 1".format(self.table_name, chat_id), parameters=(quote_id,))
            return "Quote deleted!"

    @group_only
    def add_reply(self, msg, matches):
        if not hasattr(msg, 'reply_id'):
            return "The !quotethis must be used in a reply!"
        if not hasattr(msg, 'reply') or msg.reply is None:
            return "The reply is too old, cannot add it." # TODO look into fix in tgl that can't load from server
        if not hasattr(msg.reply, 'text'):
            return "Media message replys not supported currently."

        orig_peer = msg.reply.src

        quote = "{0} {1}: {2}".format(orig_peer.first_name or '', orig_peer.last_name or '', msg.reply.text)
        return self.add_quote(msg, quote)

    @group_only
    def get_random_quote(self, msg, matches):
        chat_id = msg.dest.id
        results = self.query("SELECT * FROM {0} "
                             "WHERE chat_id = {1} ORDER BY RANDOM() LIMIT 1".format(self.table_name, chat_id))
        if len(results) == 0:
            return "No quotes in the database!"
        result = results[0]
        text = "{quote} ({qid} Added By {name} on {date})\n".format(quote=result["quote"],
                                                                    name=result["full_name"],
                                                                    date=datetime.strptime(result["timestamp"], "%Y-%m-%d %H:%M:%S").date().isoformat(),
                                                                    qid=result["quote_id"])
        return text


