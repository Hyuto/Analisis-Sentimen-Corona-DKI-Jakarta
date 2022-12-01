from src.preprocessing import *


def test_TweetPreprocessing():
    assert preprocessing("") == ""
    assert (
        preprocessing(
            """@nonacik93 udah kedua kali ini hahaha
            pertama ga mau vaksin, eh Qadarullah kena covid 2-2nya bulan2 lalu dan agak parah.
            eh skrg kena lagi Ama dokter yg katanya udah dicopot itu 😣😣😣
            ketika wa grup keluarga lebih dipercaya drpd peneliti 😅"""
        )
        == (
            "nonacik sudah dua kali ini hahaha pertama enggak mau vaksin eh qadarullah kena covid"
            + " nya bulan lalu dan agak parah eh sekarang kena lagi sama dokter yang kata sudah "
            + "copot itu wajah tidak tuju wajah tidak tuju wajah tidak tuju ketika wa grup "
            + "keluarga lebih percaya daripada teliti wajah senyum lebar dan keringat"
        )
    )
