import pygame


class Coracao:

    def __init__(
        self,
        sprites,
        largura_tela,
        altura_tela
    ):

        self.sprites = sprites

        self.ativo = False

        # ======================================
        # ANIMAÇÃO
        # ======================================

        self.indice = 0

        self.contador = 0

        self.velocidade = 8

        # ======================================
        # ESCURECIMENTO
        # ======================================

        self.escurecimento = pygame.Surface(
            (
                largura_tela,
                altura_tela
            )
        )

        self.escurecimento.fill(
            (0, 0, 0)
        )

        self.alpha = 0

    # ==========================================
    # ATUALIZAR
    # ==========================================

    def atualizar(self):

        self.contador += 1

        if (
            self.contador
            >=
            self.velocidade
        ):

            self.contador = 0

            self.indice += 1

            if (
                self.indice
                >=
                len(self.sprites)
            ):

                self.indice = 0

        # ======================================
        # ESCURECIMENTO
        # ======================================

        if self.ativo:

            if self.alpha < 150:

                self.alpha += 5

        else:

            if self.alpha > 0:

                self.alpha -= 5

        self.escurecimento.set_alpha(
            self.alpha
        )

    # ==========================================
    # DESENHAR
    # ==========================================

    def desenhar(
        self,
        tela,
        jogador
    ):

        if self.alpha <= 0:

            return

        # ======================================
        # ESCURECIMENTO
        # ======================================

        tela.blit(
            self.escurecimento,
            (0, 0)
        )

        # ======================================
        # SPRITE
        # ======================================

        sprite = (
            jogador.pegar_sprite()
        )

        sprite_coracao = (
            self.sprites[
                self.indice
            ].copy()
        )

        # 2 vezes menor que o tamanho atual
        nova_largura = max(1, int(sprite_coracao.get_width() * 0.3))
        nova_altura = max(1, int(sprite_coracao.get_height() * 0.3))
        sprite_coracao = pygame.transform.smoothscale(
            sprite_coracao,
            (nova_largura, nova_altura)
        )

        # ======================================
        # POSIÇÃO
        # ======================================

        coracao_x = (
            jogador.x
            +
            (
                sprite.get_width()
                -
                sprite_coracao.get_width()
            )
            // 2
        )

        coracao_y = (
            jogador.y
            +
            (
                sprite.get_height()
                -
                sprite_coracao.get_height()
            )
            // 2
        )

        # ======================================
        # ALPHA
        # ======================================

        sprite_coracao.set_alpha(
            self.alpha * 2
        )

        tela.blit(
            sprite_coracao,
            (
                coracao_x,
                coracao_y
            )
        )
