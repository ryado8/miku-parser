from src import section_parser

def test_extract_shadowing_section():
    text = """
    Conversation

    Shadowing

    1. I haven't cooked dinner yet.
    まだ ばんごはん(を) つくって(い)ない。
    まだ 晩御飯 (を) 作って (い)ない。

    2. I haven't cleaned my room yet.
    まだ へや(を) そうじして(い)ない。
    まだ 部屋(を) 掃除 して(い)ない。

    Japanese part

    1. まだ リビング(を) かたづけて(い)ない。
    """

    result = section_parser.extract_shadowing_section(text)

    assert "1. I haven't cooked dinner yet." in result
    assert "2. I haven't cleaned my room yet." in result
    assert "Japanese part" not in result