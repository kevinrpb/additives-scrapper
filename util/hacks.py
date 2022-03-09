
__text_replace_map = {
  '\u2013': '-'
}
def cleanup_text(text: str) -> str:
  clean = text

  for _, (k, v) in enumerate(__text_replace_map.items()):
    clean = clean.replace(k, v)

  return clean
