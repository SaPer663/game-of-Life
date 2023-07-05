from random import randint

from app.constants import FIELD_SIZE


class GameOfLife:
    """Класс объекта игры."""

    def __init__(
        self, size: int = FIELD_SIZE, residents: tuple[int] | None = None
    ) -> None:
        self.size: int = size
        self.residents = residents
        self.field: list[list[int]] = self._init_field()
        self.is_game_over: bool = True
        self.prev_configs: dict[int, bool] = {}

    def fill_field(self, residents: tuple[int]) -> list[list[int]]:
        field = [[0] * 50 for _ in range(50)]
        for t in residents:
            i, j = t
            field[i][j] = 1
        return field

    def _init_field(self) -> list[list[int]]:
        """Создаёт игровое поле с рандомным расположение живых клеток."""
        if self.residents is None:
            return [
                [randint(0, 1) for _ in range(self.size)]
                for _ in range(self.size)
            ]
        return self.fill_field()

    def _get_mask(self) -> int:
        """Возвращает битовую маску текущего поля."""
        mask = 0
        for row in self.field:
            for cell in row:
                mask = (mask << 1) | cell
        return mask

    def update_field(self) -> list[list[int]]:
        """Обновление поля согласно правила игры."""
        new_field = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                live_neighbors = sum(
                    [
                        self.field[i - 1][j - 1],
                        self.field[i - 1][j],
                        self.field[i - 1][(j + 1) % self.size],
                        self.field[i][j - 1],
                        self.field[i][(j + 1) % self.size],
                        self.field[(i + 1) % self.size][j - 1],
                        self.field[(i + 1) % self.size][j],
                        self.field[(i + 1) % self.size][(j + 1) % self.size],
                    ]
                )
                if self.field[i][j]:
                    if live_neighbors in (2, 3):
                        new_field[i][j] = 1
                        self.is_game_over = False
                else:
                    if live_neighbors == 3:
                        new_field[i][j] = 1
                        self.is_game_over = False
        self.field = new_field
        mask = self._get_mask()
        if mask in self.prev_configs or self.is_game_over:
            return []
        self.prev_configs[mask] = True
        self.is_game_over = True
        return self.field
