import json

class TradeSignal:
    def __init__(self, type, propnames):
        self.type = type
        for name in propnames:
            # only include non empty names
            if name:
                # set the property to None
                # we don't want to include empty properties in the JSON
                setattr(self, name, None)

    def to_dict(self):
        # Only include attributes with non-empty names and non-None values
        return {k: v for k, v in self.__dict__.items() if k and v is not None}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
