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

    # TC1: old_rule is Location.access_rule, combine="and"
    def test_tc1_location_and(self, mock_spot_location, mock_new_rule_true):
        # Caso de Teste: TC1
        # spot.access_rule Inicial: Location.access_rule
        # rule (nova): new_rule_A (mock_new_rule_true)
        # combine: "and"
        # Condições: (V, F, V)
        # Decisões: (V, N/A)
        # Resultado Esperado para spot.access_rule: new_rule_A
        add_rule(mock_spot_location, mock_new_rule_true, "and")
        assert mock_spot_location.access_rule == mock_new_rule_true

    # TC2: old_rule is Entrance.access_rule, combine="or"
    def test_tc2_entrance_or(self, mock_spot_entrance, mock_new_rule_false):
        # Caso de Teste: TC2
        # spot.access_rule Inicial: Entrance.access_rule
        # rule (nova): new_rule_B (mock_new_rule_false)
        # combine: "or"
        # Condições: (F, V, F)
        # Decisões: (V, N/A)
        # Resultado Esperado para spot.access_rule: new_rule_B
        add_rule(mock_spot_entrance, mock_new_rule_false, "or")
        assert mock_spot_entrance.access_rule == mock_new_rule_false

    # TC3a: custom_old_rule, combine="and"
    def test_tc3a_custom_and(self, mock_spot_custom_rule, mock_new_rule_true):
        # Caso de Teste: TC3a
        # spot.access_rule Inicial: custom_old_rule (mock_spot_custom_rule.access_rule)
        # rule (nova): new_rule_C (mock_new_rule_true)
        # combine: "and"
        # Condições: (F, F, V)
        # Decisões: (F, V)
        # Resultado Esperado para spot.access_rule: lambda state: new_rule_C(state) and custom_old_rule(state)
        original_custom_rule = mock_spot_custom_rule.access_rule
        add_rule(mock_spot_custom_rule, mock_new_rule_true, "and")
        # Test the combined rule
        state_mock = Mock()
        assert mock_spot_custom_rule.access_rule(state_mock) == (mock_new_rule_true(state_mock) and original_custom_rule(state_mock))

    # TC3b: custom_old_rule, combine="or"
    def test_tc3b_custom_or(self, mock_spot_custom_rule, mock_new_rule_false):
        # Caso de Teste: TC3b
        # spot.access_rule Inicial: custom_old_rule (mock_spot_custom_rule.access_rule)
        # rule (nova): new_rule_D (mock_new_rule_false)
        # combine: "or"
        # Condições: (F, F, F)
        # Decisões: (F, F)
        # Resultado Esperado para spot.access_rule: lambda state: new_rule_D(state) or custom_old_rule(state)
        original_custom_rule = mock_spot_custom_rule.access_rule
        add_rule(mock_spot_custom_rule, mock_new_rule_false, "or")
        # Test the combined rule
        state_mock = Mock()
        assert mock_spot_custom_rule.access_rule(state_mock) == (mock_new_rule_false(state_mock) or original_custom_rule(state_mock))
