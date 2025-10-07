from project.strategy import SMACrossoverStrategy

from proalgotrader_core.start import run_strategy


if __name__ == "__main__":
    run_strategy(strategy=SMACrossoverStrategy)
