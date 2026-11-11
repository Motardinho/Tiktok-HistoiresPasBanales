import json
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
PROMPT_FILES = {"histoire": "narrateur.md", "top": "top.md", "fait": "fait.md"}


def _extract_json(text: str) -> dict:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Réponse sans JSON : " + text[:200])
    return json.loads(text[start : end + 1])


def write_story(cfg: dict, topic: str | None, avoid: list[str], fmt: str = "histoire") -> dict:
    import anthropic

    client = anthropic.Anthropic()
    system = (PROMPTS / PROMPT_FILES[fmt]).read_text(encoding="utf-8")

    if topic:
        user = f"Écris le script sur ce sujet : {topic}"
    elif fmt == "fait":
        user = "Choisis toi-même un fait étonnant, exact et vérifiable, et écris le script."
    elif fmt == "top":
        user = (
            "Choisis toi-même un classement fascinant et vérifiable "
            "(records, extrêmes, curiosités) et écris le script."
        )
    else:
        user = (
            "Choisis toi-même une histoire vraie, documentée et fascinante "
            "(affaire ancienne, survie extrême, disparition, phénomène inexpliqué) "
            "et écris le script."
        )
    if avoid:
        user += "\nNe traite pas ces sujets déjà faits : " + "; ".join(avoid)

    msg = client.messages.create(
        model=cfg["llm"]["model"],
        max_tokens=cfg["llm"]["max_tokens"],
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    story = _extract_json(msg.content[0].text)
    story["format"] = fmt
    story["script"] = " ".join(s["narration"].strip() for s in story["scenes"])
    return story
