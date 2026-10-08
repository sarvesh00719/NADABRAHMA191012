from app.services.safety import check_crisis, validate_output

def test_crisis_matching():
    assert check_crisis("I want to die") is not None
    assert check_crisis("Kill Myself!!") is not None
    assert check_crisis("I am tired after a long day") is None

def test_validate_output():
    assert validate_output("I hear you. Tell me more about that.") is True
    assert validate_output("You suffer from depression.") is False
    long_text = "A. " * 700
    assert validate_output(long_text) is False
    assert validate_output("I am listening.", previous_assistant_message="I am listening.") is False
