from ai.sequence.sequence import Sequence

class HitAndRun(Sequence):
    def get_player(self):
        return self.gs.map.cells[self.gs.get_player_entity().cell]

    def get_nearest(self):
        player_cell = self.get_player()
        mob_cells = list(map(lambda x: self.gs.map.cells[x.cell], self.gs.get_mob_entities()))
        nearest = min(mob_cells, key=lambda x: dist(player_cell.cellIJ, x.cellIJ))
        return nearest.entity

    def fight_turn(self):
        # TODO find nearest enemy
        nearest = self.get_nearest()
        path = self.gs.map.graph

        pass

    def in_range(self):
        pass

    def end_fight(self):
        # TODO close end message
        pass