from ai.sequence.sequence import Sequence
from ai.algorithm.line_of_sight import Sight_Bresenham
import logging
from math import inf
from input.coordinates import Coordinate

PREFERRED_MIN_DISTANCE_FROM_MOBS = 4
PREFERRED_MAX_DISTANCE_FROM_MOBS = 10


class HitAndRun(Sequence):
    def loop(self):
        logging.info('HitAndRun Sequence')
        while self.gs.is_fighting and self.gs.game_fight is not None and not self.gs.game_fight.fight_started:
            desired_start_cell = self.find_starting_cell()
            logging.info(f'HitAndRun Start cell {desired_start_cell}')
            self.player.window.click_cell(desired_start_cell)
            self.tick()
            self.wait_until(lambda gs: gs.get_player_entity() and gs.get_player_entity().ready, self.gs, 5)
            self.tick()
            self.player.window.click(*Coordinate.COORD_READY)
            self.wait_until(lambda gf: gf.fight_started, self.gs.game_fight, 1.5)

        while self.gs.is_fighting and self.gs.game_fight is not None and self.gs.game_fight.fight_started:
            # wait for turn
            logging.info('HitAndRun fight started')
            self.tick(1)

    # find a cell in preferred distance form all mobs
    def find_starting_cell(self):
        elected = []
        preferred = []
        max_range = self.player.player_info['attack_spell']['range'][1]
        for cell in self.gs.game_fight.start_cells:
            min_distance_from_mobs = inf
            has_sight = False
            for mob_cell in self.get_mob_cells():
                d = Sight_Bresenham.distance(cell.posIJ, mob_cell.posIJ)
                if d < min_distance_from_mobs:
                    min_distance_from_mobs = d
                if self.gs.map.sight.has_sight(cell.posIJ, mob_cell.posIJ, max_range):
                    has_sight = True

            rec = {'min_distance_from_mobs': min_distance_from_mobs, "cell": cell, "has_sight": has_sight}
            # logging.debug(f'find_starting_cell: {rec}')
            if PREFERRED_MIN_DISTANCE_FROM_MOBS <= min_distance_from_mobs <= PREFERRED_MAX_DISTANCE_FROM_MOBS and rec['has_sight']:
                preferred.append(rec)
            elected.append(rec)

        if len(preferred):
            logging.debug("find_starting_cell FOUND IN PREFFERED")
            return sorted(preferred, key=lambda x: x['min_distance_from_mobs'], reverse=True)[0]['cell']

        elected = sorted(elected, key=lambda x: x['min_distance_from_mobs'])
        for rec in elected:
            if rec['min_distance_from_mobs'] > PREFERRED_MIN_DISTANCE_FROM_MOBS:
                return rec['cell']

        logging.debug("find_starting_cell RETURN LAST")
        return elected[-1]['cell']

    def get_player_cell(self):
        return self.gs.map.cells[self.gs.get_player_entity().cell]

    def get_mob_cells(self):
        mob_cells = list(map(lambda x: self.gs.map.cells[x.cell], self.gs.get_mob_entities()))
        return mob_cells

    # TODO
    # def get_nearest_mob_cells(self, from_cell):
    #     mob_cells = self.get_mob_cells()
    #     nearest_cells = min(mob_cells, key=lambda x: Sight_Bresenham.distance(from_cell.cellIJ, x.cellIJ))
    #     return nearest_cells

    # def fight_turn(self):
    #     # TODO find nearest enemy in sight
    #     nearest = self.get_nearest()
    #     path = self.gs.map.graph
    #     pass
