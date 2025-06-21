from container import Container

if __name__ == "__main__":
    container = Container()
    orchestrator = container.build_backtest()
    orchestrator.run()