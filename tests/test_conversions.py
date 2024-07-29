import index as mojibaka

def test_convert_japanese():
    """
    Test ability to convert Japanese mojibake to
    readable Japanese text
    """
    mojibake = "譚ｱ莠ｬ繧ｿ繝ｯ繝ｼ縺ｮ鬮倥＆縺ｯ333m縺ｧ縺吶�"
    conversion = mojibaka.convert_japanese(mojibake, "ignore")
    assert ("sjis to utf-8", "東京タワーの高さは333mです") in conversion
    assert ("utf8 to iso-2022-jp", "333m") in conversion
    assert ("shift-jis to iso-2022-jp", "333m") in conversion
    assert ("euc-jp to iso-2022-jp", "333m") in conversion
    assert ("shift-jis to euc-jp", "延根帥若蕭333mс") in conversion


def test_convert_simplified_cn():
    """
    Test ability to convert simplified Chinese mojibake to
    readable simplified Chinese text
    """
    mojibake = "ÎªÁËÓÐÐ§¡¢¸ßÐ§µØÊµÏÖÄ¿±ê£¬Äú×îÐèÒªµÄÊÇÊ²Ã´£¿"
    conversion = mojibaka.convert_simplified_cn(mojibake, "ignore")
    assert ("cp936", "为了有效、高效地实现目标，您最需要的是什么？") in conversion
    assert ("gb2312", "为了有效、高效地实现目标，您最需要的是什么？") in conversion


