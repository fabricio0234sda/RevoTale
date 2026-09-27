import pygame
import math

from config import (
    VELOCIDADE,
    VELOCIDADE_CTRL,
    ACELERACAO,
    DESACELERACAO,
    STAMINA_MAXIMA
)

from colisao import pode_andar


class Jogador:

    def __init__(
        self,
        baixo,
        cima,
        esquerda,
        direita,
        mapa=None,
        largura_tela=800,
        altura_tela=600
    ):

        self.baixo = baixo
        self.cima = cima
        self.esquerda = esquerda
        self.direita = direita

        # ======================================
        # DIREÇÃO
        # ======================================

        self.direcao = "baixo"

        self.direcao_anterior = "baixo"

        self.direcao_mira = pygame.Vector2(0, 1)

        self.olhando_esquerda = False

        # ======================================
        # VELOCIDADE
        # ======================================

        self.velocidade = VELOCIDADE

        self.velocidade_x = 0
        self.velocidade_y = 0

        # ======================================
        # ANIMAÇÃO
        # ======================================

        self.sequencia_baixo = [
            0,
            1,
            2,
            3
        ]

        self.sequencia_cima = [
            0,
            1,
            2,
            3
        ]

        self.sequencia_lado = [
            0,
            1,
            2,
            3,
            4
        ]

        self.indice_animacao = 0

        self.frame = 0

        self.contador_animacao = 0

        self.velocidade_animacao = 8

        # ======================================
        # POSIÇÃO INICIAL
        # ======================================

        sprite = self.baixo[0]

        self.x = (
            largura_tela
            -
            sprite.get_width()
        ) // 2

        self.y = (
            altura_tela
            -
            sprite.get_height()
        ) // 2

        self.stamina = STAMINA_MAXIMA
        self.coracao = None
        self.usando_coracao = False
        self.tem_chave = False
        self._ultimo_tempo_stamina = pygame.time.get_ticks()

    def definir_coracao(self, coracao):
        self.coracao = coracao

    # ==========================================
    # PEGAR SPRITE
    # ==========================================

    def _direcao_sprite(self):

        if self.direcao in ("cima", "cima_esquerda", "cima_direita"):
            return "cima"

        if self.direcao in ("esquerda", "baixo_esquerda"):
            return "esquerda"

        if self.direcao in ("direita", "baixo_direita"):
            return "direita"

        return "baixo"

    def pegar_sprite(self):

        direcao_sprite = self._direcao_sprite()

        if direcao_sprite == "baixo":

            if self.frame >= len(
                self.baixo
            ):

                return self.baixo[0]

            return self.baixo[
                self.frame
            ]

        elif direcao_sprite == "cima":

            if self.frame >= len(
                self.cima
            ):

                return self.cima[0]

            return self.cima[
                self.frame
            ]

        elif direcao_sprite == "esquerda":

            if self.frame >= len(
                self.esquerda
            ):

                return self.esquerda[0]

            return self.esquerda[
                self.frame
            ]

        elif direcao_sprite == "direita":

            if self.frame >= len(
                self.direita
            ):

                return self.direita[0]

            return self.direita[
                self.frame
            ]

        return self.baixo[0]

    # ==========================================
    # ATUALIZAR
    # ==========================================

    @staticmethod
    def _desacelerar(valor):

        if valor > 0:
            return max(
                0,
                valor - DESACELERACAO
            )

        return min(
            0,
            valor + DESACELERACAO
        )

    def _acelerar(
        self,
        valor,
        direcao,
        velocidade_maxima
    ):

        if direcao == 0:
            return self._desacelerar(valor)

        valor += direcao * ACELERACAO

        return max(
            -velocidade_maxima,
            min(
                velocidade_maxima,
                valor
            )
        )

    def atualizar(self):

        teclas = pygame.key.get_pressed()

        agora = pygame.time.get_ticks()
        delta_tempo = min(
            (agora - self._ultimo_tempo_stamina) / 1000,
            0.1
        )
        self._ultimo_tempo_stamina = agora

        ctrl_apertado = (
            teclas[pygame.K_LCTRL]
            or
            teclas[pygame.K_RCTRL]
        )

        if ctrl_apertado and self.stamina > 0:
            self.stamina = max(
                0,
                self.stamina - 5 * delta_tempo
            )
        elif not ctrl_apertado:
            self.stamina = min(
                STAMINA_MAXIMA,
                self.stamina + delta_tempo
            )

        self.usando_coracao = ctrl_apertado and self.stamina > 0

        movendo = False

        novo_x = self.x
        novo_y = self.y

        # ======================================
        # DIREÇÃO
        # ======================================

        direcao_x = 0
        direcao_y = 0

        mira_x = int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])
        mira_y = int(teclas[pygame.K_DOWN]) - int(teclas[pygame.K_UP])

        if mira_x != 0 or mira_y != 0:
            self.direcao_mira = pygame.Vector2(mira_x, mira_y)

            if mira_y < 0:
                prefixo = "cima"
            else:
                prefixo = "baixo"

            if mira_x < 0:
                self.direcao = f"{prefixo}_esquerda"
                self.olhando_esquerda = True
            elif mira_x > 0:
                self.direcao = f"{prefixo}_direita"
                self.olhando_esquerda = False
            else:
                self.direcao = prefixo
                self.olhando_esquerda = mira_x < 0

        if self.usando_coracao:
            velocidade_atual = VELOCIDADE_CTRL

        else:
            velocidade_atual = self.velocidade

        # ======================================
        # ESQUERDA
        # ======================================

        if (
            teclas[pygame.K_a]
        ):

            direcao_x -= 1

        # ======================================
        # DIREITA
        # ======================================

        if (
            teclas[pygame.K_d]
        ):

            direcao_x += 1

        # ======================================
        # CIMA
        # ======================================

        if (
            teclas[pygame.K_w]
        ):

            direcao_y -= 1

        # ======================================
        # BAIXO
        # ======================================

        if (
            teclas[pygame.K_s]
        ):

            direcao_y += 1

        self.velocidade_x = self._acelerar(
            self.velocidade_x,
            direcao_x,
            velocidade_atual
        )

        self.velocidade_y = self._acelerar(
            self.velocidade_y,
            direcao_y,
            velocidade_atual
        )

        movimento_x = self.velocidade_x
        movimento_y = self.velocidade_y

        if movimento_x != 0 and movimento_y != 0:

            fator = max(
                1,
                math.sqrt(
                    movimento_x ** 2
                    +
                    movimento_y ** 2
                )
                /
                velocidade_atual
            )

            movimento_x /= fator
            movimento_y /= fator

        # ======================================
        # NOVA POSIÇÃO
        # ======================================

        novo_x += movimento_x
        novo_y += movimento_y

        # ======================================
        # DIREÇÃO DO SPRITE
        # ======================================

        movendo = direcao_x != 0 or direcao_y != 0

        # ======================================
        # COLISÃO
        # ======================================

        sprite = self.pegar_sprite()

        if pode_andar(
            novo_x,
            self.y,
            sprite
        ):

            self.x = novo_x

        else:

            self.velocidade_x = 0

        if pode_andar(
            self.x,
            novo_y,
            sprite
        ):

            self.y = novo_y

        else:

            self.velocidade_y = 0

        # ======================================
        # MUDOU DE DIREÇÃO
        # ======================================

        if (
            self.direcao
            !=
            self.direcao_anterior
        ):

            self.indice_animacao = 0

            self.frame = 0

            self.contador_animacao = 0

            self.direcao_anterior = (
                self.direcao
            )

        # ======================================
        # ANIMAÇÃO
        # ======================================

        if movendo:

            self.contador_animacao += 1

            if (
                self.contador_animacao
                >=
                self.velocidade_animacao
            ):

                self.contador_animacao = 0

                direcao_sprite = self._direcao_sprite()

                if direcao_sprite == "baixo":

                    sequencia = (
                        self.sequencia_baixo
                    )

                elif direcao_sprite == "cima":

                    sequencia = (
                        self.sequencia_cima
                    )

                else:

                    sequencia = (
                        self.sequencia_lado
                    )

                self.indice_animacao += 1

                if (
                    self.indice_animacao
                    >=
                    len(sequencia)
                ):

                    self.indice_animacao = 0

                self.frame = (
                    sequencia[
                        self.indice_animacao
                    ]
                )

        else:

            self.frame = 0

            self.indice_animacao = 0

            self.contador_animacao = 0

    # ==========================================
    # DESENHAR
    # ==========================================

    def desenhar(
        self,
        tela,
        alpha=255
    ):

        sprite = self.pegar_sprite().copy()
        sprite.set_alpha(alpha)

        tela.blit(
            sprite,
            (
                self.x,
                self.y
            )
        )

    # ==========================================
    # OBTER HITBOX DOS PÉS
    # ==========================================

    def obter_rect(self):

        sprite = self.pegar_sprite()
        sprite_rect = sprite.get_rect(
            topleft=(self.x, self.y)
        )

        if self.usando_coracao and self.coracao is not None:
            sprite_coracao = self.coracao.sprites[
                self.coracao.indice
            ]
            hitbox = sprite_coracao.get_bounding_rect()
            hitbox.topleft = (
                self.x
                + (sprite.get_width() - sprite_coracao.get_width()) // 2
                + hitbox.left,
                self.y
                + (sprite.get_height() - sprite_coracao.get_height()) // 2
                + hitbox.top
            )
            return hitbox

        hitbox = pygame.Rect(
            0,
            0,
            sprite.get_width(),
            int(sprite.get_height() * 0.20)
        )

        hitbox.midbottom = sprite_rect.midbottom

        return hitbox

    def obter_rect_dano(self):

        sprite = self.pegar_sprite()
        sprite_rect = sprite.get_rect(
            topleft=(self.x, self.y)
        )

        if self.usando_coracao and self.coracao is not None:
            sprite_coracao = self.coracao.sprites[
                self.coracao.indice
            ]
            hitbox = sprite_coracao.get_bounding_rect()
            hitbox.topleft = (
                self.x
                + (sprite.get_width() - sprite_coracao.get_width()) // 2
                + hitbox.left,
                self.y
                + (sprite.get_height() - sprite_coracao.get_height()) // 2
                + hitbox.top
            )
            return hitbox

        hitbox = sprite.get_bounding_rect().copy()
        hitbox.topleft = (
            sprite_rect.left + hitbox.left,
            sprite_rect.top + hitbox.top
        )
        return hitbox
