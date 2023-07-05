from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.game import GameOfLife

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

game_field = GameOfLife()


@app.post('/new_game')
def new_game(residents: set[tuple[int]] | None = None) -> dict[str, str]:
    """Инициализирует новое поле."""
    game_field.fill_field_with_new_residents(residents=residents)
    return {'status': 'OK'}


@app.get('/game_of_life')
def game_of_life() -> list[list[int]]:
    """Возвращает обновлённый результат поля игры."""
    return game_field.update_field()
