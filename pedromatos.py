import streamlit as st
import numpy as np
import base64
import os, io
from pydub import AudioSegment
from pydub.playback import play
import random
import soundfile as sf
import tempfile
import requests

<style>
hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Dicionário de frequências e notas
frequencias_notas = {
        16.35: 'C-1', 17.32: 'C#-1/D♭-1', 18.35: 'D-1', 19.45: 'D#-1/E♭-1',
    20.60: 'E-1', 21.83: 'F-1', 23.12: 'F#-1/G♭-1', 24.50: 'G-1',
    25.96: 'G#-1/A♭-1', 27.50: 'A-1', 29.14: 'A#-1/B♭-1', 30.87: 'B-1',
    32.70: 'C0', 34.65: 'C#0/D♭0', 36.71: 'D0', 38.89: 'D#0/E♭0',
    41.20: 'E0', 43.65: 'F0', 46.25: 'F#0/G♭0', 49.00: 'G0',
    51.91: 'G#0/A♭0', 55.00: 'A0', 58.27: 'A#0/B♭0', 61.74: 'B0',
    65.41: 'C1', 69.30: 'C#1/D♭1', 73.42: 'D1', 77.78: 'D#1/E♭1',
    82.41: 'E1', 87.31: 'F1', 92.50: 'F#1/G♭1', 98.00: 'G1',
    103.83: 'G#1/A♭1', 110.00: 'A1', 116.54: 'A#1/B♭1', 123.47: 'B1',
    130.81: 'C2', 138.59: 'C#2/D♭2', 146.83: 'D2', 155.56: 'D#2/E♭2',
    164.81: 'E2', 174.61: 'F2', 185.00: 'F#2/G♭2', 196.00: 'G2',
    207.65: 'G#2/A♭2', 220.00: 'A2', 233.08: 'A#2/B♭2', 246.94: 'B2',
    261.63: 'C3', 277.18: 'C#3/D♭3', 293.66: 'D3', 311.13: 'D#3/E♭3',
    329.63: 'E3', 349.23: 'F3', 370.00: 'F#3/G♭3', 392.00: 'G3',
    415.30: 'G#3/A♭3', 440.00: 'A3', 466.16: 'A#3/B♭3', 493.88: 'B3',
    523.25: 'C4', 554.37: 'C#4/D♭4', 587.33: 'D4', 622.25: 'D#4/E♭4',
    659.26: 'E4', 698.46: 'F4', 739.99: 'F#4/G♭4', 783.99: 'G4',
    830.61: 'G#4/A♭4', 880.00: 'A4', 932.33: 'A#4/B♭4', 987.77: 'B4',
    1046.50: 'C5', 1108.73: 'C#5/D♭5', 1174.66: 'D5', 1244.51: 'D#5/E♭5',
    1318.51: 'E5', 1396.91: 'F5', 1479.98: 'F#5/G♭5', 1567.98: 'G5',
    1661.22: 'G#5/A♭5', 1760.00: 'A5', 1864.65: 'A#5/B♭5', 1975.53: 'B5',
    2093.00: 'C6', 2217.46: 'C#6/D♭6', 2349.32: 'D6', 2489.32: 'D#6/E♭6',
    2637.02: 'E6', 2793.83: 'F6', 2959.96: 'F#6/G♭6', 3135.96: 'G6',
    3322.44: 'G#6/A♭6', 3520.00: 'A6', 3729.31: 'A#6/B♭6', 3951.07: 'B6',
    4186.01: 'C7', 4434.92: 'C#7/D♭7', 4698.64: 'D7', 4978.03: 'D#7/E♭7',
    5274.04: 'E7', 5587.65: 'F7', 5919.91: 'F#7/G♭7', 6271.93: 'G7',
    6644.88: 'G#7/A♭7', 7040.00: 'A7', 7458.62: 'A#7/B♭7', 7902.13: 'B7',
    8372.02: 'C8', 8869.84: 'C#8/D♭8', 9397.27: 'D8', 9956.06: 'D#8/E♭8',
    10548.08: 'E8', 11175.30: 'F8', 11839.82: 'F#8/G♭8', 12543.86: 'G8',
    13289.75: 'G#8/A♭8', 14080.00: 'A8', 14917.24: 'A#8/B♭8', 15804.26: 'B8',
    16744.03: 'C9', 17739.69: 'C#9/D♭9', 18794.54: 'D9', 19912.13: 'D#9/E♭9',
    21096.17: 'E9', 22350.61: 'F9', 23679.64: 'F#9/G♭9', 25087.71: 'G9',
    26579.50: 'G#9/A♭9', 28160.00: 'A9', 29834.49: 'A#9/B♭9', 31608.53: 'B9'
}

# Função para encontrar a nota mais próxima
def encontrar_nota_mais_proxima(freq):
    return min(frequencias_notas.items(), key=lambda x: abs(x[0] - freq))

# Inicialização do estado da sessão
if 'etapa' not in st.session_state:
    st.session_state.etapa = 1

# Etapa 1: Introdução
if st.session_state.etapa == 1:
    st.title("**ACOUSMÁTICA**")
    st.write("""
        *dos cálculos para o som: transformar progressões em música*
    """)
    if st.button("Começar"):
        st.session_state.etapa = 2

# Etapa 2: Seleção de parâmetros
elif st.session_state.etapa == 2:
    st.write("Termo geral de uma **progressão geométrica**:")
    st.latex("u_n = u_1 \\times r^{n-1}")
    razao = st.slider("*Escolha o valor para a **razão*** ($r$)", min_value=0.80, max_value=1.85, step=0.01)
    termo_inicial = st.slider("*Escolha o valor para o **termo inicial*** ($u_1$)", min_value=16, max_value=440, step=1)
    st.markdown(
    """
⚠️ ***Para o aproveitamento máximo do programa, é sugerido:***

*- Para valores maiores de $r$, escolher valores menores para $u_1$, e vice-versa.*

*- Evitar valores muito próximos ou iguais a 1 para $r$.*
"""
)
    if st.button("Submeter"):
        st.session_state.razao = razao
        st.session_state.u1 = termo_inicial
        st.session_state.etapa = 3

# Etapa 3: Cálculo da nota mais próxima
elif st.session_state.etapa == 3:
    u1 = st.session_state.u1
    nota_aproximada = encontrar_nota_mais_proxima(u1)
    st.write(f"Valor do termo inicial escolhido *(frequência)*: **{u1} Hz**")
    st.write(f"Frequência da nota mais próxima: **{nota_aproximada[1]} ({nota_aproximada[0]} Hz)**")
    st.write("***Nota**: Será utilizado, para calcular os próximos termos, o valor aproximado em vez do valor escolhido pelo utilizador.*")
    if st.button("Seguinte"):
        st.session_state.u1_aproximado = nota_aproximada[0]
        st.session_state.etapa = 4

#etapa4
elif st.session_state.etapa == 4:
    st.write("Cálculo dos primeiros 25 termos, exceto se $u_n > 35000$")

    escalas_maiores = {
        "C": ["C", "D", "E", "F", "G", "A", "B"],
        "G": ["G", "A", "B", "C", "D", "E", "F#"],
        "D": ["D", "E", "F#", "G", "A", "B", "C#"],
        "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
        "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
        "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
        "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
        "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
        "F": ["F", "G", "A", "Bb", "C", "D", "E"],
        "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
        "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
        "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"]
    }

    escalas_menores = {
        "A": ["A", "B", "C", "D", "E", "F", "G"],
        "E": ["E", "F#", "G", "A", "B", "C", "D"],
        "B": ["B", "C#", "D", "E", "F#", "G", "A"],
        "F#": ["F#", "G#", "A", "B", "C#", "D", "E"],
        "C#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
        "G#": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
        "D#": ["D#", "E#", "F#", "G#", "A#", "B", "C#"],
        "A#": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"],
        "D": ["D", "E", "F", "G", "A", "Bb", "C"],
        "G": ["G", "A", "Bb", "C", "D", "Eb", "F"],
        "C": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
        "F": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"]
    }

    enarmonicos = {
        "G#": "Ab", "D#": "Eb", "A#": "Bb",
        "C#": "Db", "F#": "Gb",
        "Cb": "B", "Fb": "E", "E#": "F", "B#": "C"
    }

    def simplificar(nota):
        return enarmonicos.get(nota, nota)

    def normalizar_nota(nota_extensa):
        nota = nota_extensa.split('/')[0]
        nota = ''.join(c for c in nota if c.isalpha() or c == '#')
        return nota.upper()

    def latex_safe(text):
        return (
            text.replace('#', r'\#')
                .replace('♯', r'\sharp')
                .replace('♭', r'b')
        )

    u1 = st.session_state.u1_aproximado
    r = st.session_state.razao
    termos = []
    notas_encontradas = []

    nota_inicial_info = encontrar_nota_mais_proxima(u1)
    tonica_raw = normalizar_nota(nota_inicial_info[1])
    tonica_original = tonica_raw
    tonica_simplificada = simplificar(tonica_raw)

    for n in range(1, 26):
        un = u1 * (r ** (n - 1))
        if un > 35000:
            break

        freq_aprox, nota_extensa = encontrar_nota_mais_proxima(un)
        nota_norm = normalizar_nota(nota_extensa)
        nota_simp = simplificar(nota_norm)

        if nota_simp not in notas_encontradas:
            notas_encontradas.append(nota_simp)

        termos.append({
            'indice': n,
            'valor': round(un, 2),
            'freq_aproximada': freq_aprox,
            'nota_extensa': nota_extensa,
            'nota_simplificada': nota_simp
        })

    # Verifica escalas maiores primeiro
    tipo_escala = None
    escala_final = None
    tonica_escala = None
    melhor_percentual = 0

    for nome, escala in escalas_maiores.items():
        if nome != tonica_original and nome != tonica_simplificada:
            continue
        correspondentes = [n for n in notas_encontradas if n in escala]
        percentual = len(correspondentes) / len(escala) * 100

        if percentual >= 45 and percentual > melhor_percentual:
            tipo_escala = "Maior"
            escala_final = escala
            tonica_escala = nome
            melhor_percentual = percentual

    # Depois verifica menores, que podem sobrepor a maior caso o percentual seja maior
    for nome, escala in escalas_menores.items():
        if nome != tonica_original and nome != tonica_simplificada:
            continue
        correspondentes = [n for n in notas_encontradas if n in escala]
        percentual = len(correspondentes) / len(escala) * 100

        if percentual >= 45 and percentual > melhor_percentual:
            tipo_escala = "menor"
            escala_final = escala
            tonica_escala = nome
            melhor_percentual = percentual

    st.markdown("**Notas obtidas:**")
    for termo in termos:
        nota_ext_latex = latex_safe(termo['nota_extensa'])
        notas_enarm = termo['nota_extensa'].split('/')
        notas_sem_oitava = [n[:-1] if n[-1].isdigit() else n for n in notas_enarm]
        notas_ou = " ou ".join(notas_sem_oitava)
        notas_ou_latex = latex_safe(notas_ou)

        st.latex(
            rf"u_{{{termo['indice']}}} = {termo['valor']} \, \text{{Hz}} \approx {termo['freq_aproximada']} \, \text{{Hz}} \rightarrow \text{{{nota_ext_latex}}} \rightarrow \text{{{notas_ou_latex}}}"
        )

    if escala_final:
        st.markdown(f"**Escala obtida:** ***{tonica_escala} {tipo_escala}***")
        st.write("Notas da escala:")
        notas_formatadas = [
            f"**{n}**" if n in notas_encontradas else n for n in escala_final
        ]
        st.write(" → ".join(notas_formatadas))
        st.markdown(f"Percentagem de notas calculadas encontradas na escala: *{melhor_percentual:.1f}%*")

        if st.button("Seguinte"):
            st.session_state.escala = escala_final
            st.session_state.tipo_escala = tipo_escala.lower()
            st.session_state.etapa = 5
    else:
        st.warning("⚠️ *Não foi possível encontrar uma escala adequada com pelo menos 45% de correspondência de notas onde $u_1$ é a tónica da escala.*")
        if st.button("Tentar novamente"):
            st.session_state.etapa = 1

# Etapa 5
elif st.session_state.etapa == 5:
    st.write("**Escolha o número de acordes, onde:**")

    st.latex(r"2 \leq n_{\mathrm{acordes}} \leq 5")

    # Define um valor inicial, se ainda não estiver definido
    if "num_acordes" not in st.session_state:
        st.session_state.num_acordes = 2

    # Mostra o input numérico e atualiza o valor no estado
    num_acordes = st.number_input(
        label="*número de acordes:*",
        min_value=2,
        max_value=5,
        step=1,
        value=st.session_state.num_acordes,
        key="num_acordes_input"
    )
    st.write("⚠️ *Quanto maior o número de acordes, mais específica será a procura de músicas.*")
    # Só avança de etapa se o botão for clicado
    if st.button("Seguinte", key="botao_etapa5"):
        st.session_state.num_acordes = num_acordes
        st.session_state.etapa = 6

# --- ETAPA 6 --- 
elif st.session_state.etapa == 6: 

    num_acordes = st.session_state.num_acordes
    escala = st.session_state.escala
    tipo_escala = st.session_state.get("tipo_escala", None)

    if tipo_escala is None:
        st.error("Erro: 'tipo_escala' não definido. Por favor, volte à etapa 4.")
        st.stop()  # Para execução para evitar bug

    # A partir daqui, pode usar tipo_escala normalmente
    tipo_escala = tipo_escala.lower()

    # Progressões para escala maior
    progressoes_maior = {
        2: [["V", "I"], ["IV", "I"], ["I", "V"], ["vi", "IV"]],
        3: [["I", "IV", "V"], ["I", "V", "vi"], ["vi", "IV", "V"], ["IV", "V", "I"]],
        4: [["I", "V", "vi", "IV"], ["I", "IV", "vi", "V"], ["I", "vi", "IV", "V"], ["IV", "I", "V", "I"]],
        5: [["I", "vi", "IV", "V", "I"], ["I", "IV", "V", "IV", "I"], ["I", "V", "vi", "IV", "V"], ["vi", "IV", "I", "V", "I"]],
    }

    # Progressões para escala menor
    progressoes_menor = {
        2: [["V", "i"], ["iv", "i"], ["i", "VII"], ["VI", "V"]],
        3: [["iv", "V", "i"], ["i", "VII", "VI"], ["i", "iv", "V"], ["VI", "VII", "i"]],
        4: [["i", "VII", "VI", "V"], ["i", "iv", "V", "i"], ["VI", "III", "VII", "i"], ["i", "VI", "VII", "i"]],
        5: [["i", "VI", "III", "VII", "i"], ["i", "iv", "VII", "VI", "V"], ["i", "VII", "VI", "V", "i"], ["VI", "VII", "i", "iv", "V"]],
    }

    # Grau para índice na escala
    grau_para_indice_maior = {"I": 0, "ii": 1, "iii": 2, "IV": 3, "V": 4, "vi": 5, "vii°": 6}
    grau_para_indice_menor = {"i": 0, "ii°": 1, "III": 2, "iv": 3, "V": 4, "VI": 5, "VII": 6}

    tipo_acorde_maior = {"I": "", "ii": "m", "iii": "m", "IV": "", "V": "", "vi": "m", "vii°": "dim"}
    tipo_acorde_menor = {"i": "m", "ii°": "dim", "III": "", "iv": "m", "V": "", "VI": "", "VII": ""}

    # Escolher progressões, mapeamentos de grau e tipos de acorde conforme o tipo de escala
    if tipo_escala == 'maior':
        progressões_comuns = progressoes_maior
        grau_para_indice = grau_para_indice_maior
        tipo_acorde = tipo_acorde_maior
    else:
        progressões_comuns = progressoes_menor
        grau_para_indice = grau_para_indice_menor
        tipo_acorde = tipo_acorde_menor

    # Notas naturais e bemóis para acessar arquivos (sem sustenidos)
    notas_com_bemol = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

    def nome_arquivo_nota(nota, oitava=4):
        return f"samples/{nota}{oitava}.wav"

    def transpor_nota_bemol(nota_base, semitons):
        if nota_base in notas_com_bemol:
            idx = notas_com_bemol.index(nota_base)
        else:
            equivalencias = {'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'}
            if nota_base in equivalencias:
                idx = notas_com_bemol.index(equivalencias[nota_base])
            else:
                base = nota_base[0]
                idx = notas_com_bemol.index(base)
        idx_transp = (idx + semitons) % 12
        return notas_com_bemol[idx_transp]

    def gerar_arquivo_audio(acordes):
        duracao_acorde_ms = 1200
        acordes_audio = []

        for grau in acordes:
            idx = grau_para_indice[grau]
            nota_raiz = escala[idx]
            tipo = tipo_acorde[grau]

            intervalos = {
                "": [0, 4, 7],
                "m": [0, 3, 7],
                "dim": [0, 3, 6]
            }

            semitons = intervalos[tipo]
            notas_acorde_audio = []
            oitavas_por_intervalo = [4, 4, 3]

            for s, oitava in zip(semitons, oitavas_por_intervalo):
                nota_nome = transpor_nota_bemol(nota_raiz, s)
                arquivo = nome_arquivo_nota(nota_nome, oitava)

                if not os.path.exists(arquivo):
                    st.warning(f"Arquivo {arquivo} não encontrado! Usando nota raiz {nota_raiz}4")
                    arquivo = nome_arquivo_nota(nota_raiz, 4)

                nota_audio = AudioSegment.from_wav(arquivo)
                if len(nota_audio) > 1000:
                    nota_audio = nota_audio[1000:]
                else:
                    nota_audio = AudioSegment.silent(duration=duracao_acorde_ms)

                notas_acorde_audio.append(nota_audio)

            acorde_audio = notas_acorde_audio[0]
            for n_audio in notas_acorde_audio[1:]:
                acorde_audio = acorde_audio.overlay(n_audio)

            if len(acorde_audio) < duracao_acorde_ms:
                acorde_audio += AudioSegment.silent(duration=duracao_acorde_ms - len(acorde_audio))
            else:
                acorde_audio = acorde_audio[:duracao_acorde_ms]

            acordes_audio.append(acorde_audio)

        final_audio = sum(acordes_audio)
        tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        final_audio.export(tmpfile.name, format="wav")
        return tmpfile.name

    progressões = progressões_comuns.get(num_acordes, [])

    if not progressões:
        st.info("Nenhuma progressão disponível para esse número de acordes.")
    else:
        st.markdown(f"**Escala selecionada anteriormente:** *{escala[0]} {tipo_escala}*")
        st.markdown("**Notas da escala:**")
        st.write(" → ".join(escala))
        st.write("🎧 ***Escolha uma das sequências de acordes:***")
        st.markdown("---")
        for i, prog in enumerate(progressões, start=1):
            acordes_rotulo = " – ".join(prog)
            acordes_nomes = []
            for grau in prog:
                idx = grau_para_indice[grau]
                nota = escala[idx]
                sufixo = tipo_acorde[grau]
                acorde = f"{nota}{sufixo}"
                acordes_nomes.append(acorde)

            audio_path = gerar_arquivo_audio(prog)

            col1, col2, col3 = st.columns([1, 4, 2])

            with col1:
                if st.button(f"{i}", key=f"num_prog_{i}"):
                    st.session_state.progressao_escolhida = prog
                    st.session_state.etapa = 7

            with col2:
                st.write(f"**{acordes_rotulo}** ({' → '.join(acordes_nomes)})")

            with col3:
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format='audio/wav')
    st.markdown("---")

#etapa7
elif st.session_state.etapa == 7:
    import requests

    st.write("🎼 **PROCURA DE MÚSICAS COMPATÍVEIS COM OS DADOS OBTIDOS:**")

    # Recuperar dados da sessão
    progressao_graus = st.session_state.get("progressao_escolhida", [])
    escala = st.session_state.get("escala", [])
    tipo_escala = st.session_state.get("tipo_escala", "maior").lower()
    tonica = escala[0] if escala else "C"

    tipo_escala_formatada = "Maior" if tipo_escala == "maior" else "menor"
    st.write(f"***Tonalidade:*** {tonica} {tipo_escala_formatada}")
    st.write(f"***Graus:*** {' → '.join(progressao_graus)}")

    if not progressao_graus or not escala:
        st.warning("⚠️ Nenhuma progressão ou escala definida. Volte à etapa 6.")
        st.stop()

    # Mapas para conversão grau → nota + sufixo
    grau_para_indice_maior = {"I": 0, "ii": 1, "iii": 2, "IV": 3, "V": 4, "vi": 5, "vii°": 6}
    tipo_acorde_maior = {"I": "", "ii": "m", "iii": "m", "IV": "", "V": "", "vi": "m", "vii°": "dim"}

    grau_para_indice_menor = {"i": 0, "ii°": 1, "III": 2, "iv": 3, "V": 4, "VI": 5, "VII": 6}
    tipo_acorde_menor = {"i": "m", "ii°": "dim", "III": "", "iv": "m", "V": "", "VI": "", "VII": ""}

    if tipo_escala == "maior":
        grau_para_indice = grau_para_indice_maior
        tipo_acorde = tipo_acorde_maior
    else:
        grau_para_indice = grau_para_indice_menor
        tipo_acorde = tipo_acorde_menor

    sequencia_acordes = []
    for grau in progressao_graus:
        idx = grau_para_indice.get(grau)
        if idx is None or idx >= len(escala):
            st.warning(f"⚠️ Grau inválido ou fora da escala: {grau}")
            continue
        nota = escala[idx]
        sufixo = tipo_acorde.get(grau, "")
        acorde = f"{nota}{sufixo}"
        sequencia_acordes.append(acorde)

    st.write(f"***Sequência de acordes selecionada:*** {' → '.join(sequencia_acordes)}")

    if not sequencia_acordes:
        st.warning("⚠️ Falha ao gerar sequência de acordes. Verifique a progressão.")
        st.stop()

    # Montar URL para busca no site HookTheory
    acordes_url = ','.join(sequencia_acordes)
    link_busca = f"https://www.hooktheory.com/theorytab/chord-search"

    # Tentar buscar via API - mas sabe que não funciona
    st.info(f'ℹ️ *A pesquisa automática via *HookTheory* não está disponível no momento. [Clique aqui]({link_busca}), após a leitura do **"Como é que procuro músicas com o que obti?"** para encontrar músicas com os mesmos dados obtidos.*')
    st.markdown("---")

    # Botão para mostrar instruções
    if st.button("***Como é que procuro músicas com o que obti?***"):
        st.session_state["mostrar_tutorial"] = True

    # Mostrar o "modal" simulado se ativado
    if st.session_state.get("mostrar_tutorial", False):
        with st.container():
            st.markdown("""
    *É simples! Basta seguir estes passos:*

    1. Abra o motor de pesquisa clicando em *“Clique aqui”*.
    2. Altere o _[Key]_ e _[Scale]_ de acordo com os dados em *Tonalidade*, onde _[Key]_ corresponde à *tónica da escala* *(Letra maiúscula + # ou b, se tiver)* e _[Scale]_ indica se é maior - _[major]_ ou menor - _[minor]_.
    3. Copie a *"Sequência de acordes selecionada"* ou  *"Graus"*, o resultado será o mesmo, e cole em _[Chord String]_, removendo as setas e espaçando os acordes como se fossem palavras (apenas 1 espaço, senão dá erro).
    4. Clique em _[Search]_ e explore as músicas compatíveis com os seus dados!

    ---

    ‼️ *Selecione “Start of Section Only” para resultados mais limitados e “Ignore Chord Extensions & Inversions” para resultados mais abrangentes.*
            """)
        st.markdown("---")
