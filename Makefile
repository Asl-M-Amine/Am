# Makefile for A-MAZE-ING
# Terminal Maze Generator & Solver

# Python interpreter
PYTHON = python3

# Config file
CONFIG = config.txt

# Output maze file
OUTPUT = maze.txt

# Default target: run the game
.PHONY: run
run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

# Regenerate maze to file only
.PHONY: generate
generate:
	$(PYTHON) -c "from config import load_config; from a_maze_ing import generate_and_render; cfg = load_config('$(CONFIG)'); generate_and_render(cfg, 0)"

# Clean output files and Python cache
.PHONY: clean
clean:
	rm -f $(OUTPUT)
	rm -rf __pycache__
	find . -name "__pycache__" -type d -exec rm -rf {} +

# Help
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  run       Run the maze game"
	@echo "  generate  Generate maze file only"
	@echo "  clean     Remove generated files"
	@echo "  help      Show this help message"