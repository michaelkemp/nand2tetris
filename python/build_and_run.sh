#!/bin/bash
# Compiles a Jack program (or assembles an existing .asm file) all the
# way down to real Hack machine code, then launches the Python Hack
# computer (cpu.py + computer.py) to run it in a real window.
#
# Usage:
#   build_and_run.sh asm <path/to/File.asm>
#       Assembles an existing .asm file and runs it directly.
#
#   build_and_run.sh jack <program_dir> <OSClass1> [OSClass2 ...]
#       Compiles every .jack file in program_dir (via this repo's own
#       project 11 compiler), plus the named classes from python/os/
#       (this repo's own project 12 OS - compile only what the program
#       actually calls; see README.md's note on the 32K ROM limit),
#       translates the result to assembly (project 8) and assembles it
#       (project 6), then runs it.
#
# Examples:
#   ./build_and_run.sh jack programs/GraphicsDemo Math Memory Array Screen
#   ./build_and_run.sh asm programs/Pong/Pong.asm

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT

mode="${1:-}"

case "$mode" in
    asm)
        asm_path="${2:?usage: build_and_run.sh asm <file.asm>}"
        cp "$asm_path" "$BUILD_DIR/program.asm"
        asm_file="$BUILD_DIR/program.asm"
        ;;

    jack)
        program_dir="${2:?usage: build_and_run.sh jack <program_dir> <OSClass1> [...]}"
        shift 2
        os_classes=("$@")

        for jack_file in "$program_dir"/*.jack; do
            base=$(basename "${jack_file%.jack}")
            python3 "$REPO_ROOT/answers/11/main.py" "$jack_file" > "$BUILD_DIR/$base.vm"
        done

        for cls in "${os_classes[@]}"; do
            python3 "$REPO_ROOT/answers/11/main.py" "$SCRIPT_DIR/os/$cls.jack" > "$BUILD_DIR/$cls.vm"
        done

        python3 "$REPO_ROOT/answers/08/main.py" "$BUILD_DIR"
        asm_file="$(ls "$BUILD_DIR"/*.asm)"
        ;;

    *)
        echo "usage: build_and_run.sh asm <file.asm>"
        echo "       build_and_run.sh jack <program_dir> <OSClass1> [OSClass2 ...]"
        exit 1
        ;;
esac

python3 "$REPO_ROOT/answers/06/main.py" "$asm_file"
hack_file="$(dirname "$asm_file")/_$(basename "${asm_file%.asm}").hack"

echo "Built $hack_file ($(wc -l < "$hack_file") instructions, of a 32768 limit)"
python3 "$SCRIPT_DIR/computer.py" "$hack_file"
