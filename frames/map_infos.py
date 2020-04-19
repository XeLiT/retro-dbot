from utils.entity import Entity
import logging

# DATA = 'GM|+379;1;22;-3;79,48;-3;1560^105,1569^105;8,14;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;|+268;3;33;-1;59,47,47,31,31,103;-3;1565^100,1001^90,1001^90,1563^100,1563^110,1020^95;5,23,23,4,6,14;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;|+453;1;0;-2;31,47,47;-3;1563^90,1001^90,1001^90;2,23,23;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;-1,-1,-1;0,0,0,0;'
DATA = 'GM|+503;3;0;-1;568;-4;9073^100;0;-1;-1;-1;0,0,0,0,0;;0'


# GM
class MapInfos:
    def __init__(self, raw_data):
        self.entities = []
        self.action = '+'
        self.parse_data(raw_data)
        logging.debug(self)

    def __repr__(self):
        return '\n'.join(map(str, self.entities)) if len(self.entities) else ''

    def parse_data(self, data):
        instances = data[3:].split('|')
        for instance in instances:
            if len(instance) < 1:
                continue
            if instance[0] == '+':
                infos = instance[1:].split(';')
                cell = int(infos[0])
                template = infos[4]
                type = int(infos[5]) if ',' not in infos[5] else int(infos[5].split(',')[0])
                entity_id = int(infos[3])

                # SWITCH
                if type == -1:  # creature
                    pass
                elif type == -2:  # mob
                    # monster_team = infos[15] if len(infos) <= 18 else infos[22]
                    self.entities.append(Entity('Mob', cell=cell, id=entity_id, template=template, pa=infos[12], health=infos[13], pm=infos[14]))
                elif type == -3:  # group of mob
                    templates = list(map(int, template.split(',')))
                    levels = list(map(int, infos[7].split(',')))
                    entity_id = int(infos[3])
                    self.entities.append(Entity('GroupMob', cell=cell, id=entity_id, templates=templates, levels=levels))
                elif type == -4:  # NPC
                    pass  # mapa.entidades.TryAdd(id, new Npc(id, int.Parse(nombre_template), celda))
                elif type == -5:  # Merchants
                    pass  # mapa.entidades.TryAdd(id, new Mercantes(id, celda))
                elif type == -6:  # resources
                    pass
                else:  # players
                    self.entities.append(Entity('Player', cell=cell, id=entity_id, name=infos[4]))

            elif instance[0] == '-':  # player leave
                entity_id = int(instance[1:])
                self.action = '-'
                self.entities.append(Entity('Player' if entity_id > 0 else 'GroupMob', cell=0, id=entity_id))




if __name__ == '__main__':
    m = MapInfos(DATA)
    print(m)