import pygame

from config import (
    LARGURA,
    ALTURA,
    TAMANHO_TILE,
    TAMANHO_TILE_FONTE
)


# ==========================================
# CONFIGURAÇÕES DO MAPA
# ==========================================

COLUNAS = LARGURA // TAMANHO_TILE
LINHAS = ALTURA // TAMANHO_TILE


# ==========================================
# MAPA DO CHÃO
# ==========================================
#
# 0 = vazio
# 1 = usa chao.png
#
# O chão não possui colisão.
#


# ==========================================
# MAPAS
# ==========================================

COLUNAS = (
    (LARGURA + TAMANHO_TILE - 1)
    // TAMANHO_TILE
)

LINHAS = (
    (ALTURA + TAMANHO_TILE - 1)
    // TAMANHO_TILE
)

MAPAS = {
    1: {
        "chao": [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ],
        "parede": [
            [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12]
        ]
    },
    2: {
        "chao": [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ],
        "parede": [
            [2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
            [10, 11, 11, 11, 11, 11, 0, 0, 11, 11, 11, 11, 12]
        ]
    }
}

MAPA_ATUAL = 1
MAPA_CHAO = [linha[:] for linha in MAPAS[MAPA_ATUAL]["chao"]]
MAPA_PAREDE = [linha[:] for linha in MAPAS[MAPA_ATUAL]["parede"]]
PORTA_ABERTA = False


def definir_mapa(numero):
    global MAPA_ATUAL, MAPA_CHAO, MAPA_PAREDE

    if numero not in MAPAS:
        return

    MAPA_ATUAL = numero
    MAPA_CHAO = [linha[:] for linha in MAPAS[numero]["chao"]]
    MAPA_PAREDE = [linha[:] for linha in MAPAS[numero]["parede"]]


def definir_porta_aberta(aberta):
    global PORTA_ABERTA
    PORTA_ABERTA = aberta


def obter_rect_porta():
    # Porta alinhada à grade de tiles: 2 tiles de largura na parte central
    # da linha superior das paredes.
    x = 6 * TAMANHO_TILE
    y = 0
    return pygame.Rect(x, y, 2 * TAMANHO_TILE, TAMANHO_TILE)


def obter_rect_passagem_porta():
    rect_porta = obter_rect_porta()
    largura_passagem = 54
    return pygame.Rect(
        rect_porta.centerx - largura_passagem // 2,
        rect_porta.top,
        largura_passagem,
        rect_porta.height
    )


# ==========================================
# PEGAR TILE DO TILESET
# ==========================================

def pegar_tile(
    tileset,
    indice
):

    # ======================================
    # VERIFICAR ÍNDICE
    # ======================================

    colunas_tileset = 4
    linhas_tileset = 3
    total_tiles = colunas_tileset * linhas_tileset

    if indice is None or indice <= 0:
        return None

    if indice > total_tiles:
        return None

    # ======================================
    # POSIÇÃO NO TILESET
    # ======================================
    # A ordem do atlas começa em 1, com blocos vazios posicionados em
    # 1, 5, 7 e 9, então a conversão precisa considerar esse deslocamento.

    indice_atlas = indice - 1
    coluna = indice_atlas % colunas_tileset
    linha = indice_atlas // colunas_tileset

    # ======================================
    # RECORTAR TILE
    # ======================================

    tile = tileset.subsurface(
        pygame.Rect(
            coluna * TAMANHO_TILE_FONTE,
            linha * TAMANHO_TILE_FONTE,
            TAMANHO_TILE_FONTE,
            TAMANHO_TILE_FONTE
        )
    )

    tile = pygame.transform.scale(
        tile,
        (
            TAMANHO_TILE,
            TAMANHO_TILE
        )
    )

    return tile


# ==========================================
# DESENHAR CHÃO
# ==========================================

def pegar_tile_chao(tileset):
    """O tileset do chão é 4x2; o único tile útil é o slot 2."""
    if tileset is None:
        return None

    largura = tileset.get_width() // 4
    altura = tileset.get_height() // 2

    tile = tileset.subsurface(
        pygame.Rect(
            1 * largura,
            0 * altura,
            largura,
            altura
        )
    )
    return pygame.transform.scale(tile, (TAMANHO_TILE, TAMANHO_TILE))


def desenhar_chao(
    tela,
    chao
):

    tile_chao = pegar_tile_chao(chao)
    if tile_chao is None:
        return

    for linha in range(
        len(MAPA_CHAO)
    ):

        for coluna in range(
            len(MAPA_CHAO[linha])
        ):

            tile_id = MAPA_CHAO[
                linha
            ][
                coluna
            ]

            if tile_id == 0:
                continue

            x = coluna * TAMANHO_TILE
            y = linha * TAMANHO_TILE

            tela.blit(
                tile_chao,
                (
                    x,
                    y
                )
            )


# ==========================================
# DESENHAR PAREDES
# ==========================================

def desenhar_paredes(
    tela,
    parede
):

    for linha in range(
        len(MAPA_PAREDE)
    ):

        for coluna in range(
            len(MAPA_PAREDE[linha])
        ):

            tile_id = MAPA_PAREDE[
                linha
            ][
                coluna
            ]

            # ==================================
            # 0 = VAZIO
            # ==================================

            if tile_id == 0:
                continue

            # ==================================
            # PEGAR TILE
            # ==================================

            tile = pegar_tile(
                parede,
                tile_id
            )

            if tile is None:
                continue

            # ==================================
            # POSIÇÃO
            # ==================================

            x = (
                coluna
                *
                TAMANHO_TILE
            )

            y = (
                linha
                *
                TAMANHO_TILE
            )

            # ==================================
            # DESENHAR
            # ==================================

            tela.blit(
                tile,
                (
                    x,
                    y
                )
            )


# ==========================================
# DESENHAR MAPA COMPLETO
# ==========================================

def desenhar_mapa(
    tela,
    chao,
    parede
):

    # ======================================
    # PRIMEIRO: CHÃO
    # ======================================

    desenhar_chao(
        tela,
        chao
    )

    # ======================================
    # SEGUNDO: PAREDE
    # ======================================

    desenhar_paredes(
        tela,
        parede
    )
