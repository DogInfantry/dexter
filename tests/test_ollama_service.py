import importlib
import sys
import types


def _load_ollama_service():
    if "ollama" not in sys.modules:
        sys.modules["ollama"] = types.SimpleNamespace(
            AsyncClient=lambda *args, **kwargs: object(),
            Client=lambda *args, **kwargs: object(),
        )

    module = importlib.import_module("app.backend.services.ollama_service")
    return module.OllamaService


def _install_fake_llm_models_module():
    fake_src = types.ModuleType("src")
    fake_llm = types.ModuleType("src.llm")
    fake_models = types.ModuleType("src.llm.models")
    fake_models.OLLAMA_MODELS = [
        types.SimpleNamespace(
            model_name="llama3.1:latest",
            display_name="[meta] llama3.1 (8B)",
        )
    ]

    sys.modules["src"] = fake_src
    sys.modules["src.llm"] = fake_llm
    sys.modules["src.llm.models"] = fake_models


def test_format_models_for_api_keeps_known_display_names():
    _install_fake_llm_models_module()
    service = _load_ollama_service()()

    models = service._format_models_for_api(["llama3.1:latest"])

    assert models == [
        {
            "display_name": "[meta] llama3.1 (8B)",
            "model_name": "llama3.1:latest",
            "provider": "Ollama",
        }
    ]


def test_format_models_for_api_includes_custom_downloaded_models():
    _install_fake_llm_models_module()
    service = _load_ollama_service()()

    models = service._format_models_for_api(["custom-model:latest"])

    assert models == [
        {
            "display_name": "custom-model:latest",
            "model_name": "custom-model:latest",
            "provider": "Ollama",
        }
    ]
