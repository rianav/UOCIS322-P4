import nose
import acp_times
import arrow

def test_first_gate():
    # YYYY-MM-DDTHH:mm
    assert acp_times.open_time(0, 200, arrow.get("2021-05-0100:00")) == arrow.get("2021-05-0100:00")
    assert acp_times.close_time(0, 200, arrow.get("2021-05-0100:00")) == arrow.get("2021-05-0101:00")
