import pytest

from project.base.bid import Bid
from project.base.contract import Contract


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl",
    [
        (1, "VUL", ["C", "D"], False, False),
        (3, "VUL", ["C", "D"], False, False),
        (6, "VUL", ["C", "D"], False, False),
        (7, "VUL", ["C", "D"], False, False),
        (2, "VUL", ["H", "S"], False, False),
        (5, "VUL", ["H", "S"], False, False),
        (6, "VUL", ["H", "S"], False, False),
        (7, "VUL", ["H", "S"], False, False),
    ],
)
def test_minor_major_plain(bid_level, vul, suits, is_dbl, is_rdbl):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl",
    [
        (1, "VUL", ["C", "D"], True, False),
        (3, "VUL", ["C", "D"], True, False),
        (6, "VUL", ["C", "D"], True, False),
        (7, "VUL", ["C", "D"], True, False),
        (2, "VUL", ["H", "S"], True, False),
        (5, "VUL", ["H", "S"], True, False),
        (6, "VUL", ["H", "S"], True, False),
        (7, "VUL", ["H", "S"], True, False),
    ],
)
def test_minor_major_dbl(bid_level, vul, suits, is_dbl, is_rdbl):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl",
    [
        (1, "VUL", ["C", "D"], False, True),
        (3, "VUL", ["C", "D"], False, True),
        (6, "VUL", ["C", "D"], False, True),
        (7, "VUL", ["C", "D"], False, True),
        (2, "VUL", ["H", "S"], False, True),
        (5, "VUL", ["H", "S"], False, True),
        (6, "VUL", ["H", "S"], False, True),
        (7, "VUL", ["H", "S"], False, True),
    ],
)
def test_minor_major_rdbl(bid_level, vul, suits, is_dbl, is_rdbl):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    for i in range(14):
        assert test_contracts[0].value(tricks=i) == test_contracts[1].value(tricks=i)


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl,tricks,expected",
    [
        (1, "VUL", ["C", "H", "NT"], False, False, 7, [70, 80, 90]),
        (1, "VUL", ["C", "H", "NT"], False, False, 8, [90, 110, 120]),
        (1, "VUL", ["C", "H", "NT"], False, False, 9, [110, 140, 150]),
        (1, "VUL", ["C", "H", "NT"], False, False, 10, [130, 170, 180]),
        (1, "VUL", ["C", "H", "NT"], False, False, 11, [150, 200, 210]),
        (1, "VUL", ["C", "H", "NT"], False, False, 12, [170, 230, 240]),
        (1, "VUL", ["C", "H", "NT"], False, False, 13, [190, 260, 270]),
    ],
)
def test_1_level_plain_contracts(bid_level, vul, suits, is_dbl, is_rdbl, tricks, expected):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    assert test_contracts[0].value(tricks) == expected[0]
    assert test_contracts[1].value(tricks) == expected[1]
    assert test_contracts[2].value(tricks) == expected[2]


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl,tricks,expected",
    [
        (5, "VUL", ["C", "H", "NT"], False, False, 11, [600, 650, 660]),
        (5, "VUL", ["C", "H", "NT"], False, False, 12, [620, 680, 690]),
        (5, "VUL", ["C", "H", "NT"], False, False, 13, [640, 710, 720]),
    ],
)
def test_5_level_plain_contracts(bid_level, vul, suits, is_dbl, is_rdbl, tricks, expected):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    assert test_contracts[0].value(tricks) == expected[0]
    assert test_contracts[1].value(tricks) == expected[1]
    assert test_contracts[2].value(tricks) == expected[2]


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl,tricks,expected",
    [
        (2, "NONVUL", ["C", "H", "NT"], True, False, 8, [180, 470, 490]),
        (2, "NONVUL", ["C", "H", "NT"], True, False, 9, [280, 570, 590]),
        (2, "NONVUL", ["C", "H", "NT"], True, False, 10, [380, 670, 690]),
        (2, "NONVUL", ["C", "H", "NT"], True, False, 11, [480, 770, 790]),
        (2, "NONVUL", ["C", "H", "NT"], True, False, 12, [580, 870, 890]),
        (2, "NONVUL", ["C", "H", "NT"], True, False, 13, [680, 970, 990]),
    ],
)
def test_2_level_dbl_contracts(bid_level, vul, suits, is_dbl, is_rdbl, tricks, expected):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    assert test_contracts[0].value(tricks) == expected[0]
    assert test_contracts[1].value(tricks) == expected[1]
    assert test_contracts[2].value(tricks) == expected[2]


@pytest.mark.parametrize(
    "bid_level,vul,suits,is_dbl,is_rdbl,tricks,expected",
    [
        (6, "VUL", ["C", "H", "NT"], True, True, 12, [1830, 2070, 2110]),
        (6, "VUL", ["C", "H", "NT"], True, True, 13, [2230, 2470, 2510]),
    ],
)
def test_6_level_rdbl_contracts(bid_level, vul, suits, is_dbl, is_rdbl, tricks, expected):
    test_contracts = []
    for suit in suits:
        contract_str = str(bid_level) + suit
        test_contracts.append(Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul))

    assert test_contracts[0].value(tricks) == expected[0]
    assert test_contracts[1].value(tricks) == expected[1]
    assert test_contracts[2].value(tricks) == expected[2]


@pytest.mark.parametrize(
    "bid_level,vul,suit,is_dbl,is_rdbl,tricks,expected",
    [
        (3, "NONVUL", "C", False, False, 8, -50),
        (3, "NONVUL", "C", False, False, 7, -100),
        (3, "NONVUL", "C", False, False, 6, -150),
        (3, "NONVUL", "C", False, False, 5, -200),
        (3, "NONVUL", "C", False, False, 4, -250),
        (3, "NONVUL", "C", False, False, 3, -300),
        (3, "NONVUL", "C", False, False, 2, -350),
        (3, "NONVUL", "C", False, False, 1, -400),
        (3, "NONVUL", "C", False, False, 0, -450),
        (3, "VUL", "C", False, False, 8, -100),
        (3, "VUL", "C", False, False, 7, -200),
        (3, "VUL", "C", False, False, 6, -300),
        (3, "VUL", "C", False, False, 5, -400),
        (3, "VUL", "C", False, False, 4, -500),
        (3, "VUL", "C", False, False, 3, -600),
        (3, "VUL", "C", False, False, 2, -700),
        (3, "VUL", "C", False, False, 1, -800),
        (3, "VUL", "C", False, False, 0, -900),
        (3, "VUL", "C", True, False, 8, -200),
        (3, "VUL", "C", True, False, 7, -500),
        (3, "VUL", "C", True, False, 6, -800),
        (3, "VUL", "C", True, False, 5, -1100),
        (3, "VUL", "C", True, False, 4, -1400),
        (3, "VUL", "C", True, False, 3, -1700),
        (3, "VUL", "C", True, False, 2, -2000),
        (3, "VUL", "C", True, False, 1, -2300),
        (3, "VUL", "C", True, False, 0, -2600),
        (3, "NONVUL", "C", True, False, 8, -100),
        (3, "NONVUL", "C", True, False, 7, -300),
        (3, "NONVUL", "C", True, False, 6, -500),
        (3, "NONVUL", "C", True, False, 5, -800),
        (3, "NONVUL", "C", True, False, 4, -1100),
        (3, "NONVUL", "C", True, False, 3, -1400),
        (3, "NONVUL", "C", True, False, 2, -1700),
        (3, "NONVUL", "C", True, False, 1, -2000),
        (3, "NONVUL", "C", True, False, 0, -2300),
        (3, "VUL", "C", True, True, 8, -400),
        (3, "VUL", "C", True, True, 7, -1000),
        (3, "VUL", "C", True, True, 6, -1600),
        (3, "VUL", "C", True, True, 5, -2200),
        (3, "VUL", "C", True, True, 4, -2800),
        (3, "VUL", "C", True, True, 3, -3400),
        (3, "VUL", "C", True, True, 2, -4000),
        (3, "VUL", "C", True, True, 1, -4600),
        (3, "VUL", "C", True, True, 0, -5200),
        (3, "NONVUL", "C", True, True, 8, -200),
        (3, "NONVUL", "C", True, True, 7, -600),
        (3, "NONVUL", "C", True, True, 6, -1000),
        (3, "NONVUL", "C", True, True, 5, -1600),
        (3, "NONVUL", "C", True, True, 4, -2200),
        (3, "NONVUL", "C", True, True, 3, -2800),
        (3, "NONVUL", "C", True, True, 2, -3400),
        (3, "NONVUL", "C", True, True, 1, -4000),
        (3, "NONVUL", "C", True, True, 0, -4600),
    ],
)
def test_3_undertricks(bid_level, vul, suit, is_dbl, is_rdbl, tricks, expected):
    contract_str = str(bid_level) + suit
    test_contract = Contract("N", Bid(contract_str), is_dbl, is_rdbl, vul)

    assert test_contract.value(tricks) == expected
