"""Modulo de testes da classe Utils"""

from src.utils_layer import Utils


def test_true_validate_file_exist():
    """Testa a funcao que valida se o arquivo existe"""
    file_name = "dados/Lista_Servidor_072023.xlsx"
    utils_class = Utils()
    result = utils_class.validate_file_exist(file_name=file_name)
    assert result is True


def test_false_validate_file_exist():
    """Testa a funcao que valida se o arquivo existe"""
    file_name = "file_name_not_exist"
    utils_class = Utils()
    result = utils_class.validate_file_exist(file_name=file_name)
    assert result is False
