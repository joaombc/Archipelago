"""
Testes para validação de arquivos YAML de configuração de jogadores.
Relacionado à Issue #5004: YAML options silently ignored if invalid or of wrong type
"""

import pytest
import tempfile
import os
from unittest.mock import patch
from Generate import main
from Utils import parse_yamls


class TestYAMLValidation:
    """Testes para validação rigorosa de arquivos YAML de configuração."""
    
    def test_unknown_option_should_raise_error(self):
        """
        Teste que verifica se opções desconhecidas em arquivos YAML
        causam erro ao invés de serem silenciosamente ignoradas.
        """
        # Arrange: Criar um arquivo YAML com opção desconhecida
        yaml_content = """
game: Adventure
name: TestPlayer
Adventure:
  unknown_option_typo: "this_should_cause_error"
"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = os.path.join(temp_dir, "test_player.yaml")
            with open(yaml_file, 'w') as f:
                f.write(yaml_content)
            
            # Act & Assert: Executar geração deve falhar com opção desconhecida
            with pytest.raises(ValueError, match="File.*is invalid"):
                # Simular execução do Generate.py com arquivo contendo opção desconhecida
                import sys
                original_argv = sys.argv
                try:
                    sys.argv = [
                        "Generate.py",
                        "--player_files_path", temp_dir,
                        "--outputpath", temp_dir,
                        "--seed", "12345"
                    ]
                    main()
                finally:
                    sys.argv = original_argv
    
    def test_wrong_type_should_raise_error(self):
        """
        Teste que verifica se tipos incorretos em opções YAML
        causam erro ao invés de serem silenciosamente ignorados.
        """
        # Arrange: Criar um arquivo YAML com tipo incorreto
        yaml_content = """
game: Adventure
name: TestPlayer
Adventure:
  dragon_rando_type: 999  # Should be a string choice, not a number
"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            yaml_file = os.path.join(temp_dir, "test_player.yaml")
            with open(yaml_file, 'w') as f:
                f.write(yaml_content)
            
            # Act & Assert: Executar geração deve falhar com tipo incorreto
            with pytest.raises(ValueError, match="File.*is invalid"):
                # Simular execução do Generate.py com arquivo contendo tipo incorreto
                import sys
                original_argv = sys.argv
                try:
                    sys.argv = [
                        "Generate.py",
                        "--player_files_path", temp_dir,
                        "--outputpath", temp_dir,
                        "--seed", "12345"
                    ]
                    main()
                finally:
                    sys.argv = original_argv

