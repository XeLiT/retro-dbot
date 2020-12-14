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
        while self.gs.is_fighting and self.gs.game_fight is not None and self.gs.game_fight:
            desired_start_cell = self.find_starting_cell()
            logging.info(f'HitAndRun Start cell {desired_start_cell}')
            self.player.window.click_cell(desired_start_cell)
            self.tick()
            self.wait_until(lambda gs: gs.get_playecr_entity() and gs.get_player_entity().ready, self.gs, 5)
            self.tick()
            self.player.window.click(*Coordinate.COORD_READY)
            self.tick(20)

    # find a cell in preferred distance form all mobs
    def find_starting_cell(self):
        elected = []
        preferred = []
        for cell in self.gs.game_fight.start_cells:
            min_distance_from_mobs = inf
            for mob_cell in self.get_mob_cells():
                d = Sight_Bresenham.distance(cell.posIJ, mob_cell.posIJ)
                if d < min_distance_from_mobs:
                    min_distance_from_mobs = d
                # TODO find cell in range of one mob

            rec = {'min_distance_from_mobs': min_distance_from_mobs, "cell": cell}
            if PREFERRED_MIN_DISTANCE_FROM_MOBS <= min_distance_from_mobs <= PREFERRED_MAX_DISTANCE_FROM_MOBS:
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
    #
    # def in_range(self):
    #     pass
    #
    # def end_fight(self):
    #     # TODO close end message
    #     pass