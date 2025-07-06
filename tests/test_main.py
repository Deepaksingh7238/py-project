import pytest
from src import main

def test_main(capsys):
    main.main()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
