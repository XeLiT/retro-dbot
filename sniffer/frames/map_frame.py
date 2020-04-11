DATA = 'GM|+379;1;22;-3;79,48;-3;1560^105,1569^105;8,14;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;|+268;3;33;-1;59,47,47,31,31,103;-3;1565^100,1001^90,1001^90,1563^100,1563^110,1020^95;5,23,23,4,6,14;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;|+453;1;0;-2;31,47,47;-3;1563^90,1001^90,1001^90;2,23,23;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;'

def isFighting():
    return False

class Mob:
    def __init__(self, cell, id, monster_pa, monster_health, monster_pm, monster_team):
        self.cell = cell
        self.id = id
        self.monster_health = monster_health
        self.monster_pa = monster_pa
        self.monster_pm = monster_pm
        self.monster_team = monster_team

    def __str__(self):
        return '<Mob> {}'.format(self.__dict__)

class GroupMob:
    def __init__(self, cell, id, templates, levels):
        self.cell = cell
        self.id = id
        self.templates = list(map(int, templates))
        self.levels = list(map(int, levels))

    def __str__(self):
        return '<GroupMob> {}'.format(self.__dict__)

class Player:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return '<Player> {}'.format(self.__dict__)

# GM
class MapFrame:
    def __init__(self, data):
        self.mobs = []
        self.group_mobs = []
        self.players = []
        self.readData(data)

    def __repr__(self):
        return 'Groups\n{}\nMobs\n{}\nPlayers\n{}'.format(
            '\n'.join(map(lambda x: str(x), self.group_mobs)),
            '\n'.join(map(lambda x: str(x), self.mobs)),
            '\n'.join(map(lambda x: str(x), self.players)))

    def readData(self, data):
        instances = data[3:].split('|')
        for instance in instances:
            if len(instance) < 1:
                continue
            if instance[0] == '+':
                infos = instance[1:].split(';')
                cell = int(infos[0])
                id = int(infos[3])
                template = infos[4]
                type = int(infos[5]) if ',' not in infos[5] else int(infos[5].split(',')[0])

                # SWITCH
                if type == -1:  # creature
                    pass
                elif type == -2: # mob
                    if not isFighting():
                       return
                    monster_team = infos[15] if len(infos) <= 18 else infos[22]
                    self.mobs.append(Mob(cell, id, infos[12], infos[13], infos[14], monster_team))
                elif type == -3:  # group of mob
                    templates = template.split(',')
                    levels = infos[7].split(',')
                    self.group_mobs.append(GroupMob(cell, id, templates, levels))
                elif type == -4:  # NPC
                    pass  # mapa.entidades.TryAdd(id, new Npc(id, int.Parse(nombre_template), celda))
                elif type == -5:  # Merchants
                    pass  # mapa.entidades.TryAdd(id, new Mercantes(id, celda))
                elif type == -6:  # resources
                    pass
                else:  # players
                    self.players.append(Player(cell=cell, id=id, name=infos[4], guild=infos[16]))

if __name__ == '__main__':
    m = MapFrame(DATA)
    print(m)