from pathlib import Path


class PromptLoader:

    def __init__(self) -> None:
        self.base_dir: Path = Path(__file__).parent
        self._prompts: dict[str, dict[str, str]] = self.load_prompts()


    def load_prompts(self) -> dict[str, dict[str, str]]:
        return {
            lang_dir.name: self.load_prompts_from_dir(lang_dir)
            for lang_dir in self.base_dir.iterdir()
            if lang_dir.is_dir()
        }


    def load_prompts_from_dir(self, dir_path: Path) -> dict[str, str]:
        return {
            md_file.name.replace(".md", ""): md_file.read_text(encoding='utf-8')
            for md_file in dir_path.glob('*.md')
        }


    @property
    def prompts(self) -> dict[str, dict[str, str]]:
        return self._prompts


promts = PromptLoader()
