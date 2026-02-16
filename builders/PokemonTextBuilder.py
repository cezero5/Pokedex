from core.PokedexImport import QLabel

class PokemonTextBuilder:
    def build(self, data: dict) -> str:
        # Tipos
        types = [t["type"]["name"] for t in data.get("types", [])]

        # Stats (lista -> dict)
        stats = {}
        for s in data.get("stats", []):
            stats[s["stat"]["name"]] = s["base_stat"]

        # Abilities (lista -> lista de strings)
        abil_list = []
        for a in data.get("abilities", []):
            name = a["ability"]["name"]
            if a.get("is_hidden"):
                name += " (hidden)"
            abil_list.append("\n \t" + name)

        abilities_str = "".join(abil_list) if abil_list else "-"

        return (
            f"🧩 Nombre: {data.get('name', '-').title()}\n\n"
            f"🔥 Tipos: {', '.join(types) if types else '-'}\n"
            f"🎯 Abilities: {abilities_str}\n\n"
            f"❤️ HP: {stats.get('hp','-')}\n"
            f"⚔️ ATK: {stats.get('attack','-')}\n"
            f"🛡️ DEF: {stats.get('defense','-')}\n"
            f"✨ SpA: {stats.get('special-attack','-')}\n"
            f"🔮 SpD: {stats.get('special-defense','-')}\n"
            f"💨 Spe: {stats.get('speed','-')}"
        )