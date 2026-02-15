# ----------------- 2) Texto: SOLO FORMATO (sin requests, sin UI) -----------------
class MoveTextBuilder:
    def build(self, data: dict) -> str:
        
        return (
            f"🧩 Nombre: {data.get('name', '-').title()}\n\n"
            f"🔥 Type: {data['type']['name']}\n"
        )