from subprocess import run

from picker.AbstractionHelper import is_wayland, is_installed


class Typer:
    @staticmethod
    def best_option() -> 'Typer':
        try:
            return next(typer for typer in [XDoToolTyper, WTypeTyper] if typer.supported())()
        except StopIteration:
            print('Could not find a valid way to type characters.')
            exit(5)

    @staticmethod
    def supported() -> bool:
        pass

    def get_active_window(self) -> str:
        pass

    def type_characters(self, characters: str, active_window: str) -> None:
        pass

    def insert_from_clipboard(self, active_window: str) -> None:
        pass


class XDoToolTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return not is_wayland() and is_installed('xdotool')

    def get_active_window(self) -> str:
        return run(args=['xdotool', 'getactivewindow'], capture_output=True,
                   encoding='utf-8').stdout[:-1]

    def type_characters(self, characters: str, active_window: str) -> None:
        run([
            'xdotool',
            'type',
            '--clearmodifiers',
            '--window',
            active_window,
            characters
        ])

    def insert_from_clipboard(self, active_window: str) -> None:
        run([
            'xdotool',
            'windowfocus',
            '--sync',
            active_window,
            'key',
            '--clearmodifiers',
            'Shift+Insert',
            'sleep',
            '0.05',
        ])


class WTypeTyper(Typer):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed('wtype')

    def get_active_window(self) -> str:
        return "not possible with wtype"

    def type_characters(self, characters: str, active_window: str) -> None:
        run([
            'wtype',
            characters
        ])

    def insert_from_clipboard(self, active_window: str) -> None:
        run([
            'wtype',
            '-M',
            'shift',
            '-P',
            'Insert',
            '-p',
            'Insert',
            '-m',
            'shift'
        ])
