import pytest
from unittest.mock import Mock
from worlds.generic.Rules import add_rule, Location, Entrance

class TestAddRule:

    @pytest.fixture
    def mock_spot_location(self):
        mock_loc = Mock()
        mock_loc.access_rule = Location.access_rule
        return mock_loc

    @pytest.fixture
    def mock_spot_entrance(self):
        mock_ent = Mock()
        mock_ent.access_rule = Entrance.access_rule
        return mock_ent

    @pytest.fixture
    def mock_spot_custom_rule(self):
        mock_custom = Mock()
        mock_custom.access_rule = Mock(return_value=True)
        return mock_custom

    @pytest.fixture
    def mock_new_rule_true(self):
        return Mock(return_value=True)

    @pytest.fixture
    def mock_new_rule_false(self):
        return Mock(return_value=False)


    def test_tc1_location_and(self, mock_spot_location, mock_new_rule_true):
        add_rule(mock_spot_location, mock_new_rule_true, "and")
        assert mock_spot_location.access_rule == mock_new_rule_true


    def test_tc2_entrance_or(self, mock_spot_entrance, mock_new_rule_false):
        add_rule(mock_spot_entrance, mock_new_rule_false, "or")
        assert mock_spot_entrance.access_rule == mock_new_rule_false


    def test_tc3a_custom_and(self, mock_spot_custom_rule, mock_new_rule_true):
        original_custom_rule = mock_spot_custom_rule.access_rule
        add_rule(mock_spot_custom_rule, mock_new_rule_true, "and")
        state_mock = Mock()
        assert mock_spot_custom_rule.access_rule(state_mock) == (mock_new_rule_true(state_mock) and original_custom_rule(state_mock))

    # TC3b: custom_old_rule, combine="or"
    def test_tc3b_custom_or(self, mock_spot_custom_rule, mock_new_rule_false):
        original_custom_rule = mock_spot_custom_rule.access_rule
        add_rule(mock_spot_custom_rule, mock_new_rule_false, "or")
        state_mock = Mock()
        assert mock_spot_custom_rule.access_rule(state_mock) == (mock_new_rule_false(state_mock) or original_custom_rule(state_mock))


