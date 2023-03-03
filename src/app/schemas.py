from marshmallow import Schema, fields


class BaseSchema(Schema):
    _id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    bonuses = fields.Dict(keys=fields.Str(), values=fields.Int(), dump_only=True)
    #image_src = fields.Url(dump_only=True)


class ShipSchema(BaseSchema):
    cargo_slots = fields.Int(dump_only=True)
    item_slots = fields.Int(dump_only=True)
    total_slots = fields.Int(dump_only=True)
    types = fields.List(fields.Str(), dump_only=True)


class SupplySchema(BaseSchema):
    base_morale = fields.Int(dump_only=True)
    combined_morale_per_50t = fields.Int(dump_only=True)
    extra_rations = fields.Boolean(dump_only=True)


class ItemSchema(BaseSchema):
    dlc = fields.List(fields.Str(), dump_only=True)
    equipped_in = fields.Str(dump_only=True)
    rarity = fields.Str(dump_only=True)
    rarity_order = fields.Int(dump_only=True)
    traits = fields.List(fields.Str(), dump_only=True)
