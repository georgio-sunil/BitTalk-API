from mongoengine import Document, fields


class Coins(Document):

    coin_rank = fields.IntField(default=0, unique=True)
    cmc_id = fields.IntField(unique=True)
    symbol = fields.StringField()
    name = fields.StringField()
    logo = fields.StringField()
    active = fields.BooleanField(default=True)


class CmcCoinsList(Document):
    cmc_id = fields.StringField(unique=True)
    logo = fields.StringField()
    name = fields.StringField()
    symbol = fields.StringField()
    price_usd = fields.FloatField(default=0)
    quotes_24h = fields.ListField(fields.DictField())
    percentage_change_24h = fields.FloatField(default=0)
    percentage_change_7d = fields.FloatField(default=0)
    percentage_change_30d = fields.FloatField(default=0)
    percentage_change_60d = fields.FloatField(default=0)
    percentage_change_90d = fields.FloatField(default=0)
    market_cap = fields.IntField(default=0)
    total_supply = fields.IntField(default=0)
    circulation_supply = fields.IntField(default=0)
    about = fields.StringField()
