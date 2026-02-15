import sys
from PySide6.QtWidgets import QApplication

from core.PokeApiClient import PokeApiClient
from builders.PokemonTextBuilder import PokemonTextBuilder
from builders.MoveTextBuilder import MoveTextBuilder
from app.FrontPokedex import FrontPokedex  # ajusta el import según tu ruta


def main():
    app = QApplication(sys.argv)

    w = FrontPokedex(
        api=PokeApiClient(),                 # ✅ instancia
        pokemon_builder=PokemonTextBuilder(),# ✅ instancia
        move_builder=MoveTextBuilder()       # ✅ instancia
    )

    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
