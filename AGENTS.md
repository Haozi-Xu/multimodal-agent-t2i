# AGENTS.md

## Project Goal

Build a multimodal agent for text-to-image generation.

## Architecture

* planner: analyze user intent
* prompt_builder: refine prompts
* generator: call T2I model
* evaluator: VLM judge
* refiner: improve results

## Rules

* Always explain before editing code
* Prefer minimal changes
* Do not modify core model files unless necessary
* All scripts must be reproducible

## Commands

* run: python main.py
* test: pytest
* experiment: bash scripts/run_experiment.sh

## Coding Style

* Python
* Clear variable names
* Modular design
