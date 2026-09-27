import math

import pygame

import mapa

from config import TAMANHO_TILE


# ==========================================
# VERIFICAR SE É PAREDE
# ==========================================

def eh_parede(px, py):

    mapa_parede = mapa.MAPA_PAREDE

    coluna = int(
        px // TAMANHO_TILE
    )

    linha = int(
        py // TAMANHO_TILE
    )

    # ======================================
    # FORA DO MAPA
    # ======================================

    if linha < 0:
        return True

    if linha >= len(mapa_parede):
        return True

    if coluna < 0:
        return True

    if coluna >= len(mapa_parede[linha]):
        return True

    # ======================================
    # VERIFICAR TILE
    # ======================================

    if mapa_parede[linha][coluna] > 0:

        return True

    return False


# ==========================================
# COLISÃO DO JOGADOR
# ==========================================

def pode_andar(
    novo_x,
    novo_y,
    sprite,
    largura_colisao=None,
    altura_colisao=None,
    deslocamento_x=0
):

    largura = sprite.get_width()
    altura = sprite.get_height()

    # ======================================
    # HITBOX DOS PÉS
    # ======================================

    if largura_colisao is None:
        largura_colisao = largura

    if altura_colisao is None:
        altura_colisao = int(altura * 0.20)

    margem_colisao = 1

    # ======================================
    # POSIÇÃO DA HITBOX
    # ======================================

    colisao_x = (
        novo_x
        +
        (largura - largura_colisao) // 2
        +
        deslocamento_x
    )

    colisao_y = (
        novo_y
        +
        altura
        -
        altura_colisao
    )

    limite_esquerdo = math.floor(colisao_x)
    limite_superior = math.floor(colisao_y)
    limite_direito = math.ceil(
        colisao_x + largura_colisao
    )
    limite_inferior = math.ceil(
        colisao_y
        +
        altura_colisao
        +
        margem_colisao
    )

    hitbox = pygame.Rect(
        limite_esquerdo,
        limite_superior,
        limite_direito - limite_esquerdo,
        limite_inferior - limite_superior
    )
    mapa_parede = mapa.MAPA_PAREDE

    if (
        hitbox.left < 0
        or hitbox.top < 0
        or hitbox.right > len(mapa_parede[0]) * TAMANHO_TILE
        or hitbox.bottom > len(mapa_parede) * TAMANHO_TILE
    ):
        return False

    # ======================================
    # VERIFICAR SOBREPOSIÇÃO COM AS PAREDES
    # ======================================

    primeira_coluna = max(
        0,
        hitbox.left // TAMANHO_TILE
    )

    ultima_coluna = min(
        len(mapa_parede[0]) - 1,
        hitbox.right // TAMANHO_TILE
    )

    primeira_linha = max(
        0,
        hitbox.top // TAMANHO_TILE
    )

    ultima_linha = min(
        len(mapa_parede) - 1,
        hitbox.bottom // TAMANHO_TILE
    )

    for linha in range(
        primeira_linha,
        ultima_linha + 1
    ):

        for coluna in range(
            primeira_coluna,
            ultima_coluna + 1
        ):

            if mapa_parede[linha][coluna] <= 0:
                continue

            parede = pygame.Rect(
                coluna * TAMANHO_TILE,
                linha * TAMANHO_TILE,
                TAMANHO_TILE,
                TAMANHO_TILE
            )

            if hitbox.colliderect(parede):
                if (
                    mapa.MAPA_ATUAL == 1
                    and mapa.PORTA_ABERTA
                    and linha == 0
                    and coluna in (6, 7)
                    and mapa.obter_rect_passagem_porta().contains(
                        hitbox.clip(parede)
                    )
                ):
                    continue
                return False

    return True
