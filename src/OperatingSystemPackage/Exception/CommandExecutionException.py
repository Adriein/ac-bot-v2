class CommandExecutionException(Exception):
    def __init__(self, console_args: list[str], output: str):
        self.console_args = console_args
        self.output = output
        super().__init__(f'CommandExecutionException(args={console_args} stdout={output})')
