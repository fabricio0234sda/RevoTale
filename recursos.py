import os

import pygame

from config import (
    ESCALA,
    ESCALA_CORACAO,
    TAMANHO_TILE
)


# ==========================================
# CARREGAR ARMA
# ==========================================

def carregar_arma():

    return pygame.image.load(
        "assets/arma.png"
    ).convert_alpha()


# ==========================================
# CARREGAR CHÃO
# ==========================================

def carregar_chao():

    chao = pygame.image.load(
        "assets/chao.png"
    ).convert_alpha()

    return chao


# ==========================================
# CARREGAR PAREDE
# ==========================================

def carregar_parede():

    parede = pygame.image.load(
        "assets/parede.png"
    ).convert_alpha()

    return parede


# ==========================================
# CARREGAR PORTA
# ==========================================

def carregar_porta():

    sprites = []
    for indice in range(8):
        sprite = pygame.image.load(
            f"assets/porta/porta{indice}.png"
        ).convert_alpha()
        sprite = pygame.transform.scale(
            sprite,
            (
                sprite.get_width() * ESCALA,
                sprite.get_height() * ESCALA
            )
        )
        sprites.append(sprite)

    return sprites


# ==========================================
# CARREGAR SPRITES DO JOGADOR
# ==========================================

def carregar_personagem():

    # ======================================
    # BAIXO
    # ======================================

    baixo = [

        pygame.image.load(
            "assets/Yuri/frente1.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/frente2.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/frente3.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/frente4.png"
        ).convert_alpha()
    ]

    # ======================================
    # CIMA
    # ======================================

    cima = [

        pygame.image.load(
            "assets/Yuri/cima1.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/cima2.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/cima3.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/cima4.png"
        ).convert_alpha()
    ]

    # ======================================
    # ESQUERDA
    # ======================================

    esquerda = [

        pygame.image.load(
            "assets/Yuri/esquerda1.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/esquerda2.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/esquerda3.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/esquerda4.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/esquerda5.png"
        ).convert_alpha()
    ]

    # ======================================
    # DIREITA
    # ======================================

    direita = [

        pygame.image.load(
            "assets/Yuri/direita1.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/direita2.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/direita3.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/direita4.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/Yuri/direita5.png"
        ).convert_alpha()
    ]

    # ======================================
    # AUMENTAR PERSONAGEM
    # ======================================

    for sprites in [
        baixo,
        cima,
        esquerda,
        direita
    ]:

        for i in range(len(sprites)):

            largura = sprites[i].get_width()
            altura = sprites[i].get_height()

            sprites[i] = pygame.transform.scale(
                sprites[i],
                (
                    largura * ESCALA,
                    altura * ESCALA
                )
            )

    return (
        baixo,
        cima,
        esquerda,
        direita
    )


# ==========================================
# CARREGAR SPRITES DO EREN
# ==========================================

def carregar_eren():

    # ======================================
    # LISTAS
    # ======================================

    baixo = []
    cima = []
    esquerda = []
    direita = []

    # ======================================
    # BAIXO
    # ======================================

    for indice in range(1, 6):

        sprite = pygame.image.load(
            f"assets/Eren/frente{indice}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        sprite = pygame.transform.scale(
            sprite,
            (
                largura * ESCALA,
                altura * ESCALA
            )
        )

        baixo.append(sprite)

    # ======================================
    # CIMA
    # ======================================

    for indice in range(1, 5):

        sprite = pygame.image.load(
            f"assets/Eren/Cima{indice}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        sprite = pygame.transform.scale(
            sprite,
            (
                largura * ESCALA,
                altura * ESCALA
            )
        )

        cima.append(sprite)

    # ======================================
    # ESQUERDA
    # ======================================

    for indice in range(1, 6):

        sprite = pygame.image.load(
            f"assets/Eren/esquerda{indice}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        sprite = pygame.transform.scale(
            sprite,
            (
                largura * ESCALA,
                altura * ESCALA
            )
        )

        esquerda.append(sprite)

    # ======================================
    # DIREITA
    # ======================================

    for indice in range(1, 6):

        sprite = pygame.image.load(
            f"assets/Eren/direita{indice}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        sprite = pygame.transform.scale(
            sprite,
            (
                largura * ESCALA,
                altura * ESCALA
            )
        )

        direita.append(sprite)

    # ======================================
    # RETORNAR
    # ======================================

    return (
        baixo,
        cima,
        esquerda,
        direita
    )


# ==========================================
# CARREGAR CORAÇÃO
# ==========================================

def carregar_coracao():

    coracao = [

        pygame.image.load(
            "assets/coracao/coracao1.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/coracao/coracao2.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/coracao/coracao3.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/coracao/coracao4.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/coracao/coracao5.png"
        ).convert_alpha(),

        pygame.image.load(
            "assets/coracao/coracao6.png"
        ).convert_alpha()
    ]

    # ======================================
    # AUMENTAR CORAÇÃO
    # ======================================

    for i in range(len(coracao)):

        largura = coracao[i].get_width()
        altura = coracao[i].get_height()

        coracao[i] = pygame.transform.scale(
            coracao[i],
            (
                largura * ESCALA_CORACAO,
                altura * ESCALA_CORACAO
            )
        )

    return coracao


# ==========================================
# CARREGAR SPRITES DO PBRR
# ==========================================

def carregar_pbrr():

    # ======================================
    # CARREGAR SEQUÊNCIA DE ANIMAÇÃO
    # ======================================

    frente = []
    for i in range(1, 5):
        sprite = pygame.image.load(
            f"assets/pbrr/frente{i}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        frente.append(
            pygame.transform.scale(
                sprite,
                (
                    largura * ESCALA,
                    altura * ESCALA
                )
            )
        )

    costas = []
    for i in range(1, 5):
        sprite = pygame.image.load(
            f"assets/pbrr/cima{i}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        costas.append(
            pygame.transform.scale(
                sprite,
                (
                    largura * ESCALA,
                    altura * ESCALA
                )
            )
        )

    # A animacao lateral do PBRR usa os frames reais de esquerda.
    # Nao espelhamos para a esquerda, porque a ideia e manter o
    # eixo do sprite alinhado com a direcao do movimento.
    esquerda = []
    for i in range(1, 5):
        sprite = pygame.image.load(
            f"assets/pbrr/esquerda{i}.png"
        ).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        esquerda.append(
            pygame.transform.scale(
                sprite,
                (
                    largura * ESCALA,
                    altura * ESCALA
                )
            )
        )

    direita = []
    for i in range(1, 5):
        caminho = f"assets/pbrr/direita{i}.png"
        if not os.path.exists(caminho):
            direita = esquerda[:]
            break

        sprite = pygame.image.load(caminho).convert_alpha()

        largura = sprite.get_width()
        altura = sprite.get_height()

        direita.append(
            pygame.transform.scale(
                sprite,
                (
                    largura * ESCALA,
                    altura * ESCALA
                )
            )
        )

    if not direita:
        direita = esquerda[:]

    return (
        frente,
        costas,
        esquerda,
        direita
    )


# ==========================================
# CARREGAR SPRITES DOS OUTROS BOSSES
# ==========================================

def carregar_boss6():
    def carregar(nome):
        sprite = pygame.image.load(
            f"assets/boss6/{nome}.png"
        ).convert_alpha()
        return pygame.transform.scale(
            sprite,
            (
                sprite.get_width() * ESCALA,
                sprite.get_height() * ESCALA
            )
        )

    return (
        carregar("caindo"),
        [carregar(f"entrada{i}") for i in range(1, 4)],
        [carregar(f"frente{i}") for i in range(1, 5)]
    )


def carregar_boss7():
    def carregar(nome):
        caminhos = [
            f"assets/boss6/{nome}.png",
            f"assets/boss6/fase2/{nome}.png"
        ]
        for caminho in caminhos:
            if os.path.exists(caminho):
                sprite = pygame.image.load(caminho).convert_alpha()
                return pygame.transform.scale(
                    sprite,
                    (
                        sprite.get_width() * ESCALA,
                        sprite.get_height() * ESCALA
                    )
                )
        raise FileNotFoundError(f"Sprite do boss7 não encontrado: {nome}")

    sprites = [carregar(f"fase2{i}") for i in range(1, 5)]
    return (sprites, sprites, sprites, sprites)


def carregar_boss(pasta):

    if pasta == "boss2":
        sprite_frente = pygame.image.load(
            "assets/boss2/frente1.png"
        ).convert_alpha()
        frente = [pygame.transform.scale(
            sprite_frente,
            (
                sprite_frente.get_width() * ESCALA,
                sprite_frente.get_height() * ESCALA
            )
        )] * 4
        costas = frente[:]

        esquerda = []
        for i in range(1, 5):
            sprite = pygame.image.load(
                f"assets/boss2/esquerda{i}.png"
            ).convert_alpha()
            esquerda.append(pygame.transform.scale(
                sprite,
                (
                    sprite.get_width() * ESCALA,
                    sprite.get_height() * ESCALA
                )
            ))

        direita = []
        for i in range(1, 5):
            sprite = pygame.image.load(
                f"assets/boss2/direita{i}.png"
            ).convert_alpha()
            direita.append(pygame.transform.scale(
                sprite,
                (
                    sprite.get_width() * ESCALA,
                    sprite.get_height() * ESCALA
                )
            ))

        return (
            frente,
            costas,
            esquerda,
            direita
        )

    if pasta == "boss4":
        sprite_frente = pygame.image.load(
            "assets/boss4/MXfrente.png"
        ).convert_alpha()
        frente = [pygame.transform.scale(
            sprite_frente,
            (
                sprite_frente.get_width() * ESCALA,
                sprite_frente.get_height() * ESCALA
            )
        )] * 4
        costas = frente[:]

        esquerda = []
        for i in range(1, 6):
            sprite = pygame.image.load(
                f"assets/boss4/MXesquerda{i}.png"
            ).convert_alpha()
            esquerda.append(pygame.transform.scale(
                sprite,
                (
                    sprite.get_width() * ESCALA,
                    sprite.get_height() * ESCALA
                )
            ))

        direita = []
        for i in range(1, 6):
            sprite = pygame.image.load(
                f"assets/boss4/MXdireita{i}.png"
            ).convert_alpha()
            direita.append(pygame.transform.scale(
                sprite,
                (
                    sprite.get_width() * ESCALA,
                    sprite.get_height() * ESCALA
                )
            ))

        return (
            frente,
            costas,
            esquerda,
            direita
        )

    sprite = pygame.image.load(
        f"assets/{pasta}/frente1.png"
    ).convert_alpha()

    largura = sprite.get_width()
    altura = sprite.get_height()

    sprite_escalado = pygame.transform.scale(
        sprite,
        (
            largura * ESCALA,
            altura * ESCALA
        )
    )

    frente = [sprite_escalado] * 4
    costas = [sprite_escalado] * 4
    esquerda = [sprite_escalado] * 5
    direita = [sprite_escalado] * 5

    return (
        frente,
        costas,
        esquerda,
        direita
    )
