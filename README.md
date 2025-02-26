# Castle of Illusions - DFA Simulator

## Overview
This project is a Python-based simulator that models a deterministic finite automaton (DFA) as an interactive game set in the "Castle of Illusions." It reads a DFA configuration from an input file (`date.in`), validates its components, and emulates navigation through castle rooms based on a sequence of actions (e.g., `look`, `take`, `go`, `drop`, `inventory`). The goal is to reach a final state (e.g., the "Secret Exit") using items and transitions defined by the DFA.

## Features
- **DFA Parsing**: Reads and processes DFA sections (`[Sigma]`, `[States]`, `[Delta]`, `[alfabet]`) from `date.in` into a dictionary.
- **Validation Functions**:
  - Checks for the presence of a valid alphabet (`[Sigma]`) and transitions (`[Delta]`).
  - Ensures a single initial state and no duplicate states or symbols.
  - Validates that transitions use existing states and symbols.
- **Game Logic**:
  - Simulates room navigation with actions like `take item`, `go room`, `drop item`, `look`, and `inventory`.
  - Tracks inventory and enforces item requirements for room transitions (e.g., needing a `key` to enter the "Armory").
  - Verifies if the action sequence reaches a final state.
- **Output**: Writes validation errors and acceptance status to `date.out`, with console output for game progression.
- **Castle Setting**: Defines rooms with descriptions (`roomDesc`), display names (`roomDisplayNames`), and item requirements (`roomReq`).

## Technologies Used
- **Python**: Core language for implementation, using built-in modules (`os` not explicitly used but implied for file handling).
- **File I/O**: Reads from `date.in` and writes to `date.out` using `open()`.

## Project Structure
- **`main.py`**: Contains all logic, including:
  - `section_list()`: Parses `date.in` into a dictionary of DFA sections.
  - `exista_sigma()`, `exista_deltaa()`, `exista_delta()`: Validate DFA components.
  - `start_final()`, `start_final1()`: Handle initial and final states.
  - `duplicate()`: Check for duplicates in states and symbols.
  - `isItemValid()`, `isItemInInventory()`, `canMoveToRoom()`: Support game mechanics.
  - `emulate_dfa()`: Main DFA emulation function for room navigation.
- **`date.in`**: Input file defining the DFA (e.g., states, transitions, alphabet).
- **`date.out`**: Output file for validation results and acceptance status.

## Purpose
This project was developed to demonstrate DFA concepts through an interactive game-like simulation. It combines formal language theory with practical programming, validating a DFA’s structure and emulating its behavior as a sequence of castle room transitions, requiring specific items to progress.
