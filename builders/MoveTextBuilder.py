from core.PokedexImport import QLabel

class MoveTextBuilder:
    def stat_changes(self, data: dict):
        stat_changes = data.get('stat_changes', [])
        if stat_changes:
            stat_text = "\n".join(
                f' {s['stat']['name']}: {s['change']}'
                for s in stat_changes
            )
        else:
            stat_text = ' None'
        return stat_text
        
    def build(self, data: dict) -> str:

        return (
            f"🧩 Nombre: {data.get('name', '-').title()}\n\n"
            f"🔥 Type: {data['type']['name']}\n\n"
            f" Power: {data['power']}\n\n"
            f" PP: {data['pp']}\n\n"
            f" Priority: {data['priority']}\n\n"
            f" Stat changes: \n\t{self.stat_changes(data)}\n\n"
        )