import project.analytics.requests as loveRequests


def get_room_by_player(player, freq):
    room = None
    if player.playerId in freq.closedEw + freq.closedNs:
        room = "closed"
    elif player.playerId in freq.openEw + freq.openNs:
        room = "open"
    else:
        raise KeyError("Player does not played")

    return room


def get_direction_by_player(player, freq):
    direction = None
    if player.playerId in freq.closedEw + freq.openEw:
        direction = ["E", "W"]
    elif player.playerId in freq.closedNs + freq.openNs:
        direction = ["N", "S"]
    else:
        raise KeyError("Player does not played")

    return direction


def get_board_result_by_player(player, freq):
    room = get_room_by_player(player=player, freq=freq)
    direction = get_direction_by_player(player=player, freq=freq)

    if room == "open":
        result = freq.openResult
    elif room == "closed":
        result = freq.closedResult
    else:
        raise KeyError("Player does not played")

    contract = result.get("contract")
    score = result.get("score", -1)
    decl = result.get("decl")

    mlplr = 1 if "N" in direction else -1

    return contract, decl, score, mlplr


if __name__ == "__main__":
    RR = loveRequests.Team.create_by_name("RR")

    Budinszky_Andras = loveRequests.Player.create_by_name("Budinszky András")
    Sinkovicz_Peter = loveRequests.Player.create_by_name("Sinkovicz Péter")

    nb_boards = 32

    f = open("misc/freqik.csv", "w")
    f.write("Optimal Score;")
    f.write(f"Contract {Budinszky_Andras.surname};Declarer {Budinszky_Andras.surname}; Score {Budinszky_Andras.surname};")
    f.write(f"Contract {Sinkovicz_Peter.surname};Declarer {Sinkovicz_Peter.surname}; Score {Sinkovicz_Peter.surname};")
    f.write(f"Diff {Budinszky_Andras.surname};Diff {Sinkovicz_Peter.surname};")
    f.write("Gain;\n")

    for i in range(nb_boards):
        board_i = loveRequests.Board.create_by_bd_nb(i + 1)  # board misindexing
        optimal_score = board_i.optimumScores.get("score", -1)

        freq_i = loveRequests.Freqi.create_by_team_id(RR.registrationId, i + 1)

        contract_Andras_i, decl_Andras_i, score_Andras_i, mlplr_Andras_i = get_board_result_by_player(player=Budinszky_Andras, freq=freq_i)
        contract_Zsuzsa_i, decl_Zsuzsa_i, score_Zsuzsa_i, mlplr_Zsuzsa_i = get_board_result_by_player(player=Sinkovicz_Peter, freq=freq_i)

        print(f"{i+1})", optimal_score, contract_Andras_i, decl_Andras_i, score_Andras_i, contract_Zsuzsa_i, decl_Zsuzsa_i, score_Zsuzsa_i)

        f.write(f"{optimal_score};{contract_Andras_i};{decl_Andras_i};{score_Andras_i};{contract_Zsuzsa_i};{decl_Zsuzsa_i};{score_Zsuzsa_i};")
        f.write(f"{mlplr_Andras_i*(score_Andras_i-optimal_score)};{mlplr_Zsuzsa_i*(score_Zsuzsa_i-optimal_score)};")
        f.write(f"{mlplr_Andras_i*(score_Andras_i-optimal_score) + mlplr_Zsuzsa_i*(score_Zsuzsa_i-optimal_score)};\n")

    f.close()
