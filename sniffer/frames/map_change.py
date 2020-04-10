import data.map

DATA = 'GDM|1853|0706131721|4c2f4c4c7d204c71236065687966574a554e3d464841354820462930786b6f5f2f225f2f51632f7b78342f41206e7a2877377c61555a7378764d33553a622e5b57343a3d602422737c732447686a787538755d644660682d756864376e2a4b436c6b4f576c60263b703b2139766b44407326554c68327c5f39383031445d613d677369473b5877274262'

# DM
class MapChange:
    def __init__(self, raw):
        data = raw[4:].split('|')
        map_id = int(data[0])
        map_key = data[2]

        self.map = data.map.Map(map_id, map_date, map_key)


if __name__ == '__main__':
    m = MapChange(DATA)
    print(m)