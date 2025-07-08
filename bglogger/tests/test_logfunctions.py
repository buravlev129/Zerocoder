import pytest
from datetime import datetime
from libx import logf


def test_default_date_and_pattern():
    formatter = logf.get_date_formatter()
    result = formatter("base")
    expected_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    assert result.startswith("base_")
    # Проверяем, что дата в результате близка к текущей
    assert expected_date[:16] in result

def test_date_as_datetime():
    date = datetime(2023, 1, 1, 12, 30, 45)
    formatter = logf.get_date_formatter(date)
    assert formatter("prefix") == "prefix_2023-01-01_12-30-45"

def test_date_as_string():
    date_str = "2021-12-31_23-59-59"
    pattern = "%Y-%m-%d_%H-%M-%S"
    formatter = logf.get_date_formatter(date_str, pattern)
    assert formatter("test") == "test_2021-12-31_23-59-59"

def test_custom_output_pattern():
    date = datetime(2022, 6, 15, 8, 0, 0)
    formatter = logf.get_date_formatter(date)
    assert formatter("bf", output_pattern="%d/%m/%Y") == "bf_15/06/2022"

def test_empty_pattern_with_string_date_raises():
    date_str = "2021-01-01 12:00:00"
    with pytest.raises(ValueError):
        logf.get_date_formatter(date_str)  # паттерн не указан, strptime упадет


def test_version_formatter():
    formatter = logf.get_version_formatter('1.2.3.4')
    assert formatter("test") == "test_1.2.3.4"

    formatter = logf.get_version_formatter('x')
    assert formatter("test") == "test_x"

    with pytest.raises(ValueError):
        logf.get_version_formatter('')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

