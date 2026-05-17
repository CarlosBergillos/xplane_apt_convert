from xplane_airports import AptDat


class AptMetadata(dict):
    def add_from_row(self, row: AptDat.AptDatLine):
        tokens = row.tokens

        key = tokens[1]
        value = tokens[2] if len(tokens) > 2 else None

        self[key] = value
