class ModelLoader:

    def __init__(self, config):
        self.config = config
        self.models = {}

    def load_models(self):
        # Example
        self.models["llm"] = self._load_llm()
        self.models["asr"] = self._load_asr()

    def _load_llm(self):
        return "Load your LLM here"
