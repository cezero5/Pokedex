import core.PokedexImport as qt

from core.PokeApiClient import PokeApiClient
from builders.PokemonTextBuilder import PokemonTextBuilder
from builders.MoveTextBuilder import MoveTextBuilder
# ----------------- 3) UI: SOLO PRESENTACIÓN -----------------

class FrontPokedex(qt.QWidget):
    
    def __init__(self, api: PokeApiClient, pokemon_builder: PokemonTextBuilder, move_builder: MoveTextBuilder):
        super().__init__()
        self.api = api
        self.pokemon_builder = pokemon_builder
        self.move_builder = move_builder
        self.setWindowTitle("Pokedex")
        self.resize(325, 450)

        self.sprite_cache = {}
        self.pokemon_cache = {}
        self.species_cache = {}
        
        self.current_move_name = None

        
        self.setup_tabs()
        self.load_data()
        self.connect_signals()

        self.update_list("", self.names_pokemon, self.list_pokemon)
        self.update_list("", self.names_moves, self.list_moves)

    # ---- filtros (UI) ----
    def filter_pokemon(self, text):
        self.list_pokemon.show()
        self.update_list(text, self.names_pokemon, self.list_pokemon)

    def filter_moves(self, text):
        self.list_moves.show()
        self.update_list(text, self.names_moves, self.list_moves)

    def setup_tabs(self):
        self.tabs = qt.QTabWidget()

        # TAB 1
        self.tab_pokemon = qt.QWidget()
        layout_pokemon = qt.QVBoxLayout(self.tab_pokemon)

        self.search_pokemon = qt.QLineEdit()
        self.search_pokemon.setPlaceholderText("Example: pikachu")

        self.list_pokemon = qt.QListWidget()

        info_layout = qt.QHBoxLayout()

        self.details_pokemon = qt.QLabel("Select pokemon")
        self.details_pokemon.setWordWrap(True)

        self.sprite_label = qt.QLabel()
        self.sprite_label.setFixedSize(120, 120)

        info_layout.addWidget(self.details_pokemon)
        info_layout.addWidget(self.sprite_label)

        layout_pokemon.addWidget(self.search_pokemon)
        layout_pokemon.addWidget(self.list_pokemon)
        layout_pokemon.addLayout(info_layout)
        layout_pokemon.addStretch(1)
        
        self.tabs.addTab(self.tab_pokemon, "Pokemon")

        # TAB 2
        self.tab_moves = qt.QWidget()
        layout_moves = qt.QVBoxLayout(self.tab_moves)

        self.search_moves = qt.QLineEdit()
        self.search_moves.setPlaceholderText("Example: tackle")

        self.list_moves = qt.QListWidget()

        self.details_moves = qt.QLabel("Select move")
        self.details_moves.setWordWrap(True)
        
        self.learned_label = qt.QLabel("📘 Learned by Pokémon:")
        self.learned_list = qt.QListWidget()
        self.learned_list.setMaximumHeight(150)
        self.learned_list.hide()
        self.learned_label.hide()

        layout_moves.addWidget(self.search_moves)
        layout_moves.addWidget(self.list_moves)
        layout_moves.addWidget(self.details_moves)
        layout_moves.addWidget(self.learned_label)
        layout_moves.addWidget(self.learned_list)
        layout_moves.addStretch(1)
        
        self.tabs.addTab(self.tab_moves, "Move")

        main_layout = qt.QVBoxLayout(self)
        main_layout.addWidget(self.tabs)

    def eventFilter(self, obj, event):
        if event.type() == qt.QEvent.KeyPress:
            key = event.key()

            if obj is self.search_pokemon:
                lst = self.list_pokemon
                select = self.on_pokemon_clicked
            elif obj is self.search_moves:
                lst = self.list_moves
                select = self.on_move_clicked
            else:
                return super().eventFilter(obj, event)

            if key == qt.Qt.Key_Down and lst.count() > 0:
                row = lst.currentRow()
                if row < 0:
                    lst.setCurrentRow(0)
                else:
                    lst.setCurrentRow(min(row + 1, lst.count() - 1))
                return True

            if key == qt.Qt.Key_Up and lst.count() > 0:
                row = lst.currentRow()
                if row < 0:
                    lst.setCurrentRow(0)
                else:
                    lst.setCurrentRow(max(row - 1, 0))
                return True

            if key in (qt.Qt.Key_Return, qt.Qt.Key_Enter):
                item = lst.currentItem()
                if item:
                    select(item)
                return True

        return super().eventFilter(obj, event)


    def load_data(self):
        self.names_pokemon = self.api.list_pokemon_names(limit=1302)
        self.names_moves = self.api.list_move_names(limit=937)

    def connect_signals(self):
        self.search_pokemon.installEventFilter(self)
        self.search_moves.installEventFilter(self)
        # Pokémon: vivo + Enter
        self.search_pokemon.textChanged.connect(self.filter_pokemon)
        self.search_pokemon.returnPressed.connect(
            lambda: self.filter_pokemon(self.search_pokemon.text())
        )

        # Moves: vivo + Enter
        self.search_moves.textChanged.connect(self.filter_moves)
        self.search_moves.returnPressed.connect(
            lambda: self.filter_moves(self.search_moves.text())
        )

        # Clicks
        self.list_pokemon.itemClicked.connect(self.on_pokemon_clicked)
        self.list_moves.itemClicked.connect(self.on_move_clicked)
        self.learned_list.itemClicked.connect(self.info_learned_move_pokemon)


    def update_list(self, text, names, widget):
        t = text.strip().lower()
        widget.clear()

        if not t:
            for n in names[:50]:
                widget.addItem(n)
            return

        count = 0
        for n in names:
            if t in n:
                widget.addItem(n)
                count += 1
                if count >= 50:
                    break

    def on_pokemon_clicked(self, item):
        name = item.text().strip().lower()
        self.details_pokemon.setText("Loading...")
        txt = item.text()
        

        try:
            if name in self.pokemon_cache:
              data = self.pokemon_cache[name]
            else:
                data = self.api.get_pokemon(name)
                self.pokemon_cache[name] = data

            if name in self.species_cache:
                species = self.species_cache[name]
            else:
                species = self.api.get_species(name)
                self.species_cache[name] = species

        except Exception as e:
            self.details_pokemon.setText(f"Error cargando Pokémon: {e}")
            return

        self.details_pokemon.setText(self.pokemon_builder.build(data, species))
        
        self.load_sprite_from_data(data)

        self.search_pokemon.blockSignals(True)
        self.search_pokemon.setText(txt)
        self.search_pokemon.blockSignals(False)
        self.list_pokemon.hide()


    def load_sprite_from_data(self, data):
        sprite_url = data.get("sprites", {}).get("front_default")
        if not sprite_url:
            self.sprite_label.clear()
            return

        if sprite_url in self.sprite_cache:
            self.sprite_label.setPixmap(self.sprite_cache[sprite_url])
            self.sprite_label.setScaledContents(True)
            return

        try:
            img = self.api.get_image_bytes(sprite_url)
            pixmap = qt.QPixmap()
            pixmap.loadFromData(img)
            self.sprite_cache[sprite_url] = pixmap

            self.sprite_label.setPixmap(pixmap)
            self.sprite_label.setScaledContents(True)
        except Exception:
            self.sprite_label.clear()

    def on_move_clicked(self, item):
        name = item.text().strip().lower()
        self.current_move_name = name
        self.details_moves.setText("Loading...")
        
        try:
            data = self.api.get_move(name)
        except Exception as e:
            self.details_moves.setText(f"Error cargando Pokemon: {e}")
            return
        
        self.details_moves.setText(self.move_builder.build(data))
        
        # 🔥 llenar lista learned
        self.learned_list.clear()
        learned = data.get("learned_by_pokemon", [])

        for p in learned:
            self.learned_list.addItem(p["name"])

        if learned:
            self.learned_label.show()
            self.learned_list.show()
        else:
            self.learned_label.hide()
            self.learned_list.hide()
        
        self.search_moves.blockSignals(True)
        self.search_moves.setText(item.text())
        self.search_moves.blockSignals(False)
        self.list_moves.hide()

    def on_pokemon_clicked_from_move(self, item):
        pokemon_name = item.text()
        self.tabs.setCurrentIndex(0)  # cambiar a tab Pokémon
        self.search_pokemon.setText(pokemon_name)
        self.on_pokemon_clicked(item)
        
    def on_learned_pokemon_clicked(self, item):
        name = item.text().strip().lower()

        # Cambiar a tab Pokémon
        self.tabs.setCurrentIndex(0)

        self.details_pokemon.setText("Loading...")
        
        try:
            if name in self.pokemon_cache:
                data = self.pokemon_cache[name]
            else:
                data = self.api.get_pokemon(name)
                self.pokemon_cache[name] = data

            if name in self.species_cache:
                species = self.species_cache[name]
            else:
                species = self.api.get_species(name)
                self.species_cache[name] = species

        except Exception as e:
            self.details_pokemon.setText(f"Error cargando Pokémon: {e}")
            return

        # Mostrar información
        self.details_pokemon.setText(self.pokemon_builder.build(data, species))
        self.load_sprite_from_data(data)

        # Actualizar barra de búsqueda
        self.search_pokemon.blockSignals(True)
        self.search_pokemon.setText(name)
        self.search_pokemon.blockSignals(False)

        # Ocultar lista desplegable si estaba visible
        self.list_pokemon.hide()
    
    def info_learned_move_pokemon(self, item):
        pokemon_name = item.text().lower()
        
        if pokemon_name in self.pokemon_cache:
            pokemon_data = self.pokemon_cache[pokemon_name]
        else:
            pokemon_data = self.api.get_pokemon(pokemon_name)
            self.pokemon_cache[pokemon_name] = pokemon_data
        
        stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon_data["stats"]}
        
        info_text = f"""\nPokemon: {pokemon_data['name'].capitalize()}\nStats:
            \tHP: {stats.get('hp')}
            \tAttack: {stats.get('attack')}
            \tDefense: {stats.get('defense')}
            \tSp. Atk: {stats.get('special-attack')}
            \tSp. Def: {stats.get('special-defense')}
            \tSpeed: {stats.get('speed')}
            \t\n"""
            
        
        learn_methods = []
        move_name = self.current_move_name
        for move in pokemon_data["moves"]:
            if move["move"]["name"] == move_name:
                for detail in move["version_group_details"]:
                    method = detail["move_learn_method"]["name"]
                    level = detail["level_learned_at"]
                    
                    if method == "level-up":
                        learn_methods.append(f"Level {level}")
                    else:
                        learn_methods.append(method.capitalize())
                break
        if learn_methods:
            info_text += "\nLearn method:\n"
            info_text += "\n".join(f"- {m}" for m in set(learn_methods))
        else:
            info_text += "\n This Pokemon canot learn this move."
        
        self.details_moves.setText(info_text)