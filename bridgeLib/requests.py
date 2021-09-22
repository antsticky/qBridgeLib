import requests
from collections import Counter

# TODO: config file
EVENT_CODE = "visoft_1798802_2_1"


class Reqest:
    headers = {"Content-type": "application/json", "Accept": "application/json"}

    url_team = f"https://vugraph.lovebridge.com/api/archive/teams/{EVENT_CODE}"
    url_boards = f"https://vugraph.lovebridge.com/api/archive/boards/{EVENT_CODE}"
    url_freq_base = f"https://vugraph.lovebridge.com/api/archive/team-frequencies/{EVENT_CODE}/"
    url_watch_base = f"https://vugraph.lovebridge.com/api/archive/watch/{EVENT_CODE}/"

    def __init__(self):
        pass

    @staticmethod
    def fetch(url, default_value=[]):
        res = requests.get(url, headers=Reqest.headers)
        return res.json() if res.status_code == 200 else default_value


class Player:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    @classmethod
    def create_by_name(cls, player_name):
        teams = Reqest.fetch(Reqest.url_team)

        res_player = None
        for team in teams:
            for player in team.get("players", []):
                if player_name == player.get("name", ""):
                    res_player = player
                    break

        assert res_player is not None, "Player not found"

        return cls(res_player)


class Team:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    @classmethod
    def create_by_name(cls, team_name):
        teams = Reqest.fetch(Reqest.url_team)

        res_team = None
        for team in teams:
            if team.get("name", "") == team_name:
                res_team = team
                break

        assert res_team is not None, "Team not found"

        return cls(res_team)


class Board:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    @classmethod
    def create_by_bd_nb(cls, bd_nb):
        boards = Reqest.fetch(Reqest.url_boards)

        assert len(boards) + 1 > bd_nb, "Less board were played"

        return cls(boards[bd_nb - 1])


class Freqi:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    @classmethod
    def create_by_team_id(cls, team_id, bd_nb):
        freqs = Reqest.fetch(f"{Reqest.url_freq_base}{bd_nb}")

        res_freq = None
        for freq in freqs:
            if team_id in freq.get("registrations", {}).values():
                res_freq = freq
                break

        assert res_freq is not None, "Freqi not found"

        return cls(res_freq)


class Watch:
    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    @classmethod
    def create_by_team_id(cls, team_id, bd_nb):
        watch_fetch = Reqest.fetch(f"{Reqest.url_watch_base}{team_id}/{bd_nb}")
        watch_dict = {"data": watch_fetch}

        topic_names = []
        for data in watch_dict.get("data"):
            if data.get("topicType", None) is not None:
                topic_names.append(data.get("topicType"))

        watch_dict["topicType"] = Counter(topic_names)

        return cls(watch_dict)

    def show_bidding(self):
        unit_scpae = "   "
        space_dict = {"N": 0, "E": 1, "S": 2, "W": 3}
        shift = None

        for data in self.data:
            if data.get("topicType") == "FULL":
                bids = data.get("payload").get("bg")
                for idx, bid in enumerate(bids):
                    alerted = "" if bid.get("al") == "f" else "".join([a for a in bid.get("alDir")])

                    if shift is None:
                        shift = 3 - space_dict.get(bid.get("d"))

                    end_char = "\n" if idx % 4 == 0 + shift else " - "
                    if idx == 0:
                        print(unit_scpae * space_dict.get(bid.get("d")), bid.get("bv"), alerted, end=end_char)
                    else:
                        print(bid.get("bv"), alerted, end=end_char)

    def show_play(self, show_play_card=True):
        NS_tricks = 0
        EW_tricks = 0
        trick_counter = 0
        for data in self.data:
            if data.get("topicType", "") == "PLAY_CARD":
                card = data.get("payload", {}).get("card", "")
                if show_play_card:
                    if trick_counter % 4 == 0:
                        print(f"{trick_counter // 4 + 1}) ", end="")
                    print(f"{card[0]}:{card[1:]}", end=" ")
                    trick_counter += 1
            elif data.get("topicType", "") == "END_TRICK":
                if data.get("payload", {}).get("wd", "") in ["E", "W"]:
                    EW_tricks += 1
                elif data.get("payload", {}).get("wd", "") in ["N", "S"]:
                    NS_tricks += 1

                if show_play_card:
                    print(f"\t\tNS: {NS_tricks}, EW: {EW_tricks}", end="\n")
            elif data.get("topicType", "") == "CLAIM":
                dir = data.get("payload", {}).get("dir", "")
                tcount = data.get("payload", {}).get("tcount", "")
                print(f"||CLAIM|| {dir}: {tcount} ")
            elif data.get("topicType", "") == "END_GAME":
                line = data.get("payload", {}).get("line", "")
                tricks = data.get("payload", {}).get("trick", "")
                value = data.get("payload", {}).get("value", "")

                contract = data.get("payload", {}).get("contractDto", {})
                dec = contract.get("dec", "")
                level = contract.get("level", "")

                print(f"||END||\nline (who we are watching): {line}\ntricks (dec): {tricks}\ndec (of the contract): {dec}\nlevel: {level}\nvalue (for us): {value}")

                # TODO: hard coded NS
                tricks_needed = level + 5
                is_made = "+++" if tricks_needed < tricks else "---"
                print(is_made)


######################################
######################################
# TODO: add DDS classes
# https://vugraph.lovebridge.com/api/archive/watch/visoft_1799866_1_1/1797460/2
# https://vugraph.lovebridge.com/api/archive/dds-archive/visoft_1799866_1_1/1797460/2/0/0
# https://vugraph.lovebridge.com/api/archive/dds-archive/visoft_1799866_1_1/1797460/2/1/1
# https://vugraph.lovebridge.com/api/archive/dds-archive/visoft_1799866_1_1/1797460/2/1/3
#
# url_dds = 'https://vugraph.lovebridge.com/api/archive/dds-archive/visoft_1799866_1_1/1797460/2/8/4' # board_num/trick/1-3
# res5 = requests.get(url_dds, headers=Reqest.headers)
# dds = res5.json() if res5.status_code == 200 else None
######################################
######################################
