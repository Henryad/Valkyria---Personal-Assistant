# Valkyria - Personal-Assistant

**Valkyria — Assistente Pessoal 100% Local (Windows)**

Este repositório contém um MVP funcional da Valkyria (Val) com:
  
-Hotword por frase ("Val"/"Valkyria").

-ASR: whisper.cpp.

-LLM: llama-cpp-python (ex.: Llama 3.1 8B Q4_K_M).

-TTS: Piper (voz pt-BR).

-Casa: Tuya (TinyTuya) e MagicHome (flux_led) por LAN.

-Calendário: Outlook Desktop (COM) — 100% local.

-Ferramentas prontas com nomes dos seus dispositivos: Quarto (Tuya) e Fita de led (MagicHome).

# Valkyria — Assistente Pessoal 100% Local


## Requisitos
- Windows 10/11, Python 3.10+
- **whisper.cpp** (binário + modelo) e **Piper** (binário + voz pt-BR)
- Microfone configurado


## Setup rápido
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy config.example.yaml config.yaml # edite IDs/IPs/chaves
python .\src\jarvis.py



**Estrutura**

        valkyria-assistente-local/
        README.md
        .gitignore
        requirements.txt
        config.example.yaml
        tools/
        whisper/ # (coloque whisper.exe e modelos .bin/.gguf aqui)
        piper/ # (coloque piper.exe e vozes .onnx/.json aqui)
        src/
        jarvis.py
        core/
        audio.py
        vad.py
        asr_whispercpp.py
        tts_piper.py
        llm_llamacpp.py
        router.py
        memory.py
        wake_phrase.py
        tuya_client.py
        magichome_client.py
        outlook_calendar.py
        email_reader.py
        tools.py
