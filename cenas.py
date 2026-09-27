import pygame
import random


# ==================================================
# CONFIGURAÇÃO DAS CENAS
# ==================================================

CENAS = [

    {
        "Cena": 1,
        "Texto": "Há muito tempo, este mundo começou a esquecer.",
        "tremertexto": "off",
        "tremerimagem": "off"
    },

    {
        "Cena": 2,
        "Texto": "Nomes desapareceram dos livros. Feitos foram apagados. Histórias foram deixadas para trás.",
        "tremertexto": "off",
        "tremerimagem": "off"
    },

    {
        "Cena": 3,
        "Texto": "Mas algumas histórias se recusaram a desaparecer.",
        "tremertexto": "off",
        "tremerimagem": "off"
    },

    {
        "Cena": 4,
        "Texto": "Você não precisa mudar o passado. Apenas lute por um futuro melhor...",
        "tremertexto": "off",
        "tremerimagem": "off"
    },

    {
        "Cena": 5,
        "Texto": "LUTE!",
        "tremertexto": "on",
        "tremerimagem": "on"
    }

]


# ==================================================
# ARQUIVOS DAS CENAS
# ==================================================

ARQUIVOS_CENAS = [

    "assets/cenas/cena1.png",
    "assets/cenas/cena2.png",
    "assets/cenas/cena3.png",
    "assets/cenas/cena4.png",
    "assets/cenas/cena5.png",

]


# ==================================================
# CONFIGURAÇÕES
# ==================================================

DURACAO_CENA = 3000
DURACAO_FADE = 800

TAMANHO_FONTE = 42

COR_TEXTO = (
    255,
    255,
    255
)


# ==================================================
# CONFIGURAÇÕES DAS IMAGENS
# ==================================================

# RESOLUÇÃO ORIGINAL DAS IMAGENS:
#
# 256 x 192
#
# A imagem será ampliada 3x:
#
# 256 x 3 = 768
# 192 x 3 = 576
#
# Isso mantém os pixels nítidos.

IMAGEM_ORIGINAL_LARGURA = 256
IMAGEM_ORIGINAL_ALTURA = 192

ESCALA_IMAGEM = 3

# Quantidade de pixels removidos depois da imagem ser ampliada.
# Ajuste estes valores para escolher o corte superior e inferior.
CORTE_CIMA_PIXELS = 30
CORTE_BAIXO_PIXELS = 30

IMAGEM_LARGURA = (
    IMAGEM_ORIGINAL_LARGURA
    *
    ESCALA_IMAGEM
)

IMAGEM_ALTURA = (
    IMAGEM_ORIGINAL_ALTURA
    *
    ESCALA_IMAGEM
)

IMAGEM_OFFSET_Y = -100


# ==================================================
# CONFIGURAÇÃO DA DIGITAÇÃO
# ==================================================

VELOCIDADE_DIGITACAO = 35


# ==================================================
# CONFIGURAÇÃO DA TREMIDA
# ==================================================

# Tempo para a tremida chegar à força máxima.
#
# 3000 = 3 segundos

DURACAO_TREMIDA = 3000


# Força máxima da tremida do texto

FORCA_TREMIDA_TEXTO = 3


# Força máxima da tremida da imagem

FORCA_TREMIDA_IMAGEM = 8


# ==================================================
# CARREGAR CENAS
# ==================================================

def carregar_imagem_cena(arquivo):
    try:
        imagem_original = pygame.image.load(arquivo)

        if imagem_original.get_alpha() is not None:
            imagem_original = imagem_original.convert_alpha()
        else:
            imagem_original = imagem_original.convert()

        imagem = pygame.transform.scale(
            imagem_original,
            (IMAGEM_LARGURA, IMAGEM_ALTURA)
        )

        corte_cima = max(
            0,
            min(CORTE_CIMA_PIXELS, imagem.get_height() - 1)
        )
        corte_baixo = max(
            0,
            min(
                CORTE_BAIXO_PIXELS,
                imagem.get_height() - corte_cima - 1
            )
        )
        altura_cortada = (
            imagem.get_height()
            - corte_cima
            - corte_baixo
        )
        return imagem.subsurface(
            (0, corte_cima, imagem.get_width(), altura_cortada)
        ).copy()

    except pygame.error as erro:
        print(f"ERRO ao carregar cena: {arquivo}")
        print(erro)
        return None


def carregar_cenas():
    cenas = []

    for arquivo in ARQUIVOS_CENAS:
        imagem = carregar_imagem_cena(arquivo)
        if imagem is not None:
            cenas.append(imagem)

    return cenas


def mostrar_final(tela):
    cena_final = carregar_imagem_cena("assets/cenas/cena6.png")
    cena_fuga = carregar_imagem_cena("assets/cenas/Fuga.png")
    if cena_final is None or cena_fuga is None:
        return False

    clock = pygame.time.Clock()
    fonte = pygame.font.Font(None, TAMANHO_FONTE)
    sobreposicao = pygame.Surface(tela.get_size())
    mensagem = "fim de jogo"

    def processar_eventos():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if (
                evento.type == pygame.KEYDOWN
                and evento.key == pygame.K_ESCAPE
            ):
                return False
        return True

    def desenhar_quadro(imagem, texto="", alpha=0):
        tela.fill((0, 0, 0))
        desenhar_imagem(tela, imagem)
        desenhar_texto(tela, texto, fonte)
        if alpha > 0:
            sobreposicao.fill((0, 0, 0))
            sobreposicao.set_alpha(alpha)
            tela.blit(sobreposicao, (0, 0))
        pygame.display.flip()

    def fazer_fade(imagem, alpha_inicial, alpha_final, texto=""):
        inicio = pygame.time.get_ticks()
        while True:
            if not processar_eventos():
                return False

            progresso = min(
                1.0,
                (pygame.time.get_ticks() - inicio) / 2000
            )
            alpha = int(
                alpha_inicial
                + (alpha_final - alpha_inicial) * progresso
            )
            desenhar_quadro(imagem, texto, alpha)

            if progresso >= 1.0:
                return True
            clock.tick(60)

    desenhar_quadro(cena_final)
    inicio = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inicio < 10000:
        if not processar_eventos():
            return False
        desenhar_quadro(cena_final)
        clock.tick(60)

    if not fazer_fade(cena_final, 0, 255):
        return False
    if not fazer_fade(cena_fuga, 255, 0):
        return False

    inicio = pygame.time.get_ticks()
    duracao_digitacao = len(mensagem) * 150
    while True:
        if not processar_eventos():
            return False

        elapsed = pygame.time.get_ticks() - inicio
        letras = min(len(mensagem), elapsed // 150)
        desenhar_quadro(cena_fuga, mensagem[:letras])
        if elapsed >= duracao_digitacao + 2000:
            break
        clock.tick(60)

    if not fazer_fade(cena_fuga, 0, 255, mensagem):
        return False
    desenhar_quadro(cena_fuga, mensagem, 255)
    return True


# ==================================================
# QUEBRAR TEXTO
# ==================================================

def quebrar_texto(
    texto,
    fonte,
    largura_maxima
):

    palavras = texto.split(" ")

    linhas = []

    linha_atual = ""

    for palavra in palavras:

        teste = (
            linha_atual
            +
            palavra
            +
            " "
        )

        if fonte.size(teste)[0] <= largura_maxima:

            linha_atual = teste

        else:

            if linha_atual:

                linhas.append(
                    linha_atual.strip()
                )

            linha_atual = (
                palavra
                +
                " "
            )

    if linha_atual:

        linhas.append(
            linha_atual.strip()
        )

    return linhas


# ==================================================
# CALCULAR TREMIDA
# ==================================================

def calcular_tremida(
    tempo,
    forca_maxima
):

    # ==============================================
    # CALCULAR PROGRESSO
    # ==============================================

    progresso = (
        tempo
        /
        DURACAO_TREMIDA
    )

    # ==============================================
    # LIMITAR ENTRE 0 E 1
    # ==============================================

    if progresso < 0:

        progresso = 0

    if progresso > 1:

        progresso = 1

    # ==============================================
    # SUAVIZAR O CRESCIMENTO
    #
    # Começa devagar:
    #
    # 0%
    # 5%
    # 20%
    # 50%
    # 100%
    #
    # aproximadamente.
    # ==============================================

    progresso_suave = (
        progresso
        *
        progresso
    )

    # ==============================================
    # FORÇA ATUAL
    # ==============================================

    forca_atual = (
        forca_maxima
        *
        progresso_suave
    )

    # ==============================================
    # SEM TREMIDA
    # ==============================================

    if forca_atual <= 0:

        return (
            0,
            0
        )

    # ==============================================
    # GERAR DESLOCAMENTO
    # ==============================================

    deslocamento_x = random.uniform(
        -forca_atual,
        forca_atual
    )

    deslocamento_y = random.uniform(
        -forca_atual,
        forca_atual
    )

    return (
        int(deslocamento_x),
        int(deslocamento_y)
    )


# ==================================================
# DESENHAR TEXTO
# ==================================================

def desenhar_texto(
    tela,
    texto,
    fonte,
    deslocamento_x=0,
    deslocamento_y=0
):

    if not texto:

        return

    largura = tela.get_width()

    altura = tela.get_height()

    # ==============================================
    # LARGURA MÁXIMA DO TEXTO
    # ==============================================

    largura_texto = (
        IMAGEM_LARGURA
        -
        60
    )

    # ==============================================
    # POSIÇÃO DA IMAGEM
    # ==============================================

    imagem_y = (
        altura // 2
        -
        IMAGEM_ALTURA // 2
        +
        IMAGEM_OFFSET_Y
    )

    # ==============================================
    # POSIÇÃO BASE DO TEXTO
    # ==============================================

    texto_y_base = (
        imagem_y
        +
        IMAGEM_ALTURA
        +
        25
    )

    # ==============================================
    # QUEBRAR TEXTO
    # ==============================================

    linhas = quebrar_texto(
        texto,
        fonte,
        largura_texto
    )

    # ==============================================
    # ESPAÇAMENTO
    # ==============================================

    espacamento = 8

    altura_linha = (
        fonte.get_height()
        +
        espacamento
    )

    altura_total = (
        len(linhas)
        *
        altura_linha
    )

    # ==============================================
    # POSIÇÃO Y
    # ==============================================

    texto_y = (
        texto_y_base
        +
        (
            140
            -
            altura_total
        ) // 2
    )

    # ==============================================
    # APLICAR TREMIDA
    # ==============================================

    texto_y += deslocamento_y

    # ==============================================
    # DESENHAR LINHAS
    # ==============================================

    for linha in linhas:

        superficie = fonte.render(
            linha,
            True,
            COR_TEXTO
        )

        rect = superficie.get_rect(
            center=(
                largura // 2
                +
                deslocamento_x,

                texto_y
                +
                fonte.get_height() // 2
            )
        )

        tela.blit(
            superficie,
            rect
        )

        texto_y += altura_linha


# ==================================================
# DESENHAR IMAGEM
# ==================================================

def desenhar_imagem(
    tela,
    imagem,
    deslocamento_x=0,
    deslocamento_y=0
):

    largura = tela.get_width()

    altura = tela.get_height()

    # ==============================================
    # CENTRALIZAR IMAGEM
    # ==============================================

    imagem_x = (largura - imagem.get_width()) // 2

    imagem_y = (
        altura // 2
        -
        imagem.get_height() // 2
        +
        IMAGEM_OFFSET_Y
    )

    # ==============================================
    # APLICAR TREMIDA
    # ==============================================

    imagem_x += deslocamento_x

    imagem_y += deslocamento_y

    # ==============================================
    # DESENHAR
    # ==============================================

    tela.blit(
        imagem,
        (
            imagem_x,
            imagem_y
        )
    )


# ==================================================
# MOSTRAR CENAS
# ==================================================

def mostrar_cenas(tela):

    clock = pygame.time.Clock()

    # ==============================================
    # FONTE
    # ==============================================

    fonte = pygame.font.Font(
        None,
        TAMANHO_FONTE
    )

    # ==============================================
    # CARREGAR CENAS
    # ==============================================

    cenas = carregar_cenas()

    if len(cenas) == 0:

        return True

    # ==============================================
    # CADA CENA
    # ==============================================

    for indice in range(len(cenas)):

        cena_atual = cenas[indice]

        # ==========================================
        # CONFIGURAÇÕES DA CENA
        # ==========================================

        if indice < len(CENAS):

            configuracao = CENAS[indice]

        else:

            configuracao = {
                "Texto": "",
                "tremertexto": "off",
                "tremerimagem": "off"
            }

        # ==========================================
        # TEXTO
        # ==========================================

        texto_completo = configuracao.get(
            "Texto",
            ""
        )

        # ==========================================
        # TREMIDA DO TEXTO
        # ==========================================

        tremer_texto = (
            configuracao.get(
                "tremertexto",
                "off"
            ).lower()
            ==
            "on"
        )

        # ==========================================
        # TREMIDA DA IMAGEM
        # ==========================================

        tremer_imagem = (
            configuracao.get(
                "tremerimagem",
                "off"
            ).lower()
            ==
            "on"
        )

        # ==========================================
        # DIGITAÇÃO
        # ==========================================

        letras_mostradas = 0

        texto_digitado = ""

        terminou_digitacao = False

        ultimo_tempo_letra = (
            pygame.time.get_ticks()
        )

        # ==========================================
        # TEMPO DA CENA
        # ==========================================

        inicio = (
            pygame.time.get_ticks()
        )

        pulou = False

        # ==========================================
        # LOOP DA CENA
        # ==========================================

        while True:

            agora = (
                pygame.time.get_ticks()
            )

            tempo_passado = (
                agora
                -
                inicio
            )

            # ======================================
            # DIGITAÇÃO
            # ======================================

            if not terminou_digitacao:

                if (
                    agora
                    -
                    ultimo_tempo_letra
                    >=
                    VELOCIDADE_DIGITACAO
                ):

                    if (
                        letras_mostradas
                        <
                        len(texto_completo)
                    ):

                        letras_mostradas += 1

                        texto_digitado = (
                            texto_completo[
                                :letras_mostradas
                            ]
                        )

                        ultimo_tempo_letra = agora

                    else:

                        terminou_digitacao = True

            # ======================================
            # EVENTOS
            # ======================================

            for evento in pygame.event.get():

                # ==================================
                # FECHAR
                # ==================================

                if evento.type == pygame.QUIT:

                    return False

                # ==================================
                # TECLA
                # ==================================

                if evento.type == pygame.KEYDOWN:

                    # ==============================
                    # ESC
                    # ==============================

                    if evento.key == pygame.K_ESCAPE:

                        return False

                    # ==============================
                    # COMPLETAR TEXTO
                    # ==============================

                    if not terminou_digitacao:

                        texto_digitado = (
                            texto_completo
                        )

                        letras_mostradas = (
                            len(texto_completo)
                        )

                        terminou_digitacao = True

                    # ==============================
                    # PASSAR CENA
                    # ==============================

                    else:

                        pulou = True

            # ======================================
            # LIMPAR TELA
            # ======================================

            tela.fill(
                (
                    0,
                    0,
                    0
                )
            )

            # ======================================
            # TREMIDA DA IMAGEM
            # ======================================

            deslocamento_imagem_x = 0

            deslocamento_imagem_y = 0

            if tremer_imagem:

                (
                    deslocamento_imagem_x,
                    deslocamento_imagem_y
                ) = calcular_tremida(
                    tempo_passado,
                    FORCA_TREMIDA_IMAGEM
                )

            # ======================================
            # DESENHAR IMAGEM
            # ======================================

            desenhar_imagem(
                tela,
                cena_atual,
                deslocamento_imagem_x,
                deslocamento_imagem_y
            )

            # ======================================
            # TREMIDA DO TEXTO
            # ======================================

            deslocamento_texto_x = 0

            deslocamento_texto_y = 0

            if tremer_texto:

                (
                    deslocamento_texto_x,
                    deslocamento_texto_y
                ) = calcular_tremida(
                    tempo_passado,
                    FORCA_TREMIDA_TEXTO
                )

            # ======================================
            # DESENHAR TEXTO
            # ======================================

            desenhar_texto(
                tela,
                texto_digitado,
                fonte,
                deslocamento_texto_x,
                deslocamento_texto_y
            )

            # ======================================
            # DISPLAY
            # ======================================

            pygame.display.flip()

            # ======================================
            # TERMINAR CENA
            # ======================================

            if (
                pulou
                or
                (
                    terminou_digitacao
                    and
                    tempo_passado
                    >=
                    DURACAO_CENA
                )
            ):

                break

            clock.tick(60)

        # ==========================================
        # TRANSIÇÃO
        # ==========================================

        if indice < len(cenas) - 1:

            proxima_cena = cenas[
                indice + 1
            ]

            # ======================================
            # ALPHA INICIAL
            # ======================================

            proxima_cena.set_alpha(0)

            inicio_fade = (
                pygame.time.get_ticks()
            )

            # ======================================
            # LOOP FADE
            # ======================================

            while True:

                agora = (
                    pygame.time.get_ticks()
                )

                tempo_fade = (
                    agora
                    -
                    inicio_fade
                )

                progresso = (
                    tempo_fade
                    /
                    DURACAO_FADE
                )

                if progresso > 1:

                    progresso = 1

                # ==================================
                # FUNDO
                # ==================================

                tela.fill(
                    (
                        0,
                        0,
                        0
                    )
                )

                # ==================================
                # CENA ATUAL
                # ==================================

                desenhar_imagem(
                    tela,
                    cena_atual
                )

                # ==================================
                # TEXTO ATUAL
                # ==================================

                desenhar_texto(
                    tela,
                    texto_completo,
                    fonte
                )

                # ==================================
                # PRÓXIMA IMAGEM
                # ==================================

                proxima_cena.set_alpha(
                    int(
                        progresso
                        *
                        255
                    )
                )

                desenhar_imagem(
                    tela,
                    proxima_cena
                )

                # ==================================
                # DISPLAY
                # ==================================

                pygame.display.flip()

                # ==================================
                # FINALIZAR FADE
                # ==================================

                if progresso >= 1:

                    proxima_cena.set_alpha(
                        255
                    )

                    break

                clock.tick(60)

    # ==================================================
    # FIM
    # ==================================================

    return True
