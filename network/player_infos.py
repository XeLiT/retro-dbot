
class PlayerInfos:
    def __init__(self) -> None:
        self.selecting_server = False
        self.selecting_player = False
        self.max_pods = None
        self.pods = None
        self.spells = None

    def parse_login(self, raw_data):
        self.selecting_server = True

    def parse_select_server(self, raw_data):
        self.selecting_server = False
        self.selecting_player = True

    def parse_select_player(self, raw_data): # ASK|80146042|Xelit
        self.selecting_player = False

    def parse_pods(self, raw_data):  # Ow400|1005
        tmp = raw_data[2:].split('|')
        self.pods = tmp[0]
        self.max_pods = tmp[1]

    def parse_spells(self, raw_data):  # SL142~5~b;157~5~c;143~5~d;151~1~f;155~1~h;149~5~i;153~5~j;144~5~k;148~1~l;147~1~m;413~2~n;410~1~o;145~1~_;146~1~_;154~1~_;150~1~_;152~1~_;141~5~_;156~1~_;
        pass

    def parse_stats(self, raw_data):  #  As28850152,28264000,29882000|6709634|2|2|0~0,0,0,0,0,0|534,534|10000,10000|410|110|6,2,0,0,8|3,2,0,0,5|0,-100,0,0|0,114,0,0|121,40,0,0|0,-100,0,0|0,410,0,0|0,-100,0,0|0,0,0,0|1,0,0,0|0,8,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,2,0,0|0,0,0,0|0,0,0,0|0,8,0,0|0,0,0,0|30,10,0,0|30,10,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,5,0,0|0,0,0,0|0,0,0,0|0,0,0,0|0,5,0,0|0,0,0,0|0,0,0,0|5
        pass