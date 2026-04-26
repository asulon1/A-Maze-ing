.PHONY: install run debug clean lint lint-strict

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python -m pdb a_maze_ing.py config.txt

clean:
	-del /s /q /f *.pyc
	-rmdir /s /q __pycache__
	-rmdir /s /q .mypy_cache
	-rmdir /s /q *.egg-info
	-rmdir /s /q dist
	-rmdir /s /q build

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	mypy --strict .
	flake8 .
