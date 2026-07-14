from filehasher.controller import FileHasherController


def test_verificar_hash_coincide() -> None:
    controller = FileHasherController()

    resultado = controller.verificar_hash(
        "ABC123",
        "abc123",
    )

    assert resultado is True


def test_verificar_hash_ignora_espacios() -> None:
    controller = FileHasherController()

    resultado = controller.verificar_hash(
        "  abc123  ",
        "abc123",
    )

    assert resultado is True


def test_verificar_hash_no_coincide() -> None:
    controller = FileHasherController()

    resultado = controller.verificar_hash(
        "abc123",
        "def456",
    )

    assert resultado is False
