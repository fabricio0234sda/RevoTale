import pygame


# =========================================================
# CONFIGURAÇÕES
# =========================================================

ALTURA_CAIXA = 150

MARGEM = 15

TAMANHO_NOME = 24
TAMANHO_TEXTO = 22

COR_CAIXA = (20, 20, 20)
COR_BORDA = (255, 255, 255)

COR_NOME = (255, 230, 120)
COR_TEXTO = (255, 255, 255)

VELOCIDADE_DIGITACAO = 30


# =========================================================
# DIÁLOGOS
# =========================================================

DIALOGOS = [

    {
        "autor": "Mateus Valentin",
        "estado": "normal",
        "fala": "Que graça! Cogitei que não despertarias....",
        "podemover": False
    },

    {
        "autor": "Sebastiana Aparecida",
        "estado": "feliz",
        "fala": "Ai! Sinto minha fronte palpitar.",
        "podemover": False
    },

    {
        "autor": "Mateus Valentin",
        "estado": "triste",
        "fala": "Acertaram uma coronhada em ti, agora estamos presos nesta sala.",
        "podemover": False
    },

    {
        "autor": "Sebastiana Aparecida",
        "estado": "normal",
        "fala": "Imagino que nos apossarmos daquela conveniente arma próxima a nós seja a melhor decisão...",
        "podemover": True
    }

]


BOSS_DIALOGOS = {
    "boss6": [
        {
            "autor": "Vilão comicamente trajado",
            "estado": "normal",
            "fala": "Sua hora chegou...",
            "podemover": False
        },
        {
            "autor": "Vilão comicamente trajado",
            "estado": "normal",
            "fala": "Prepare-se para morrer!",
            "podemover": False
        }
    ]
}


# =========================================================
# CLASSE CAIXA DE DIÁLOGO
# =========================================================

class CaixaDialogo:

    def __init__(self, largura, altura):

        self.largura = largura
        self.altura = altura

        # -----------------------------------------------
        # FONTE
        # -----------------------------------------------

        self.fonte_nome = pygame.font.Font(
            None,
            TAMANHO_NOME
        )

        self.fonte_texto = pygame.font.Font(
            None,
            TAMANHO_TEXTO
        )

        # -----------------------------------------------
        # ESTADO
        # -----------------------------------------------

        self.ativo = False

        self.indice = 0

        self.dialogos = DIALOGOS

        self.texto_completo = ""
        self.texto_digitado = ""

        self.letras_mostradas = 0

        self.terminou_digitacao = False

        self.ultimo_tempo_letra = 0

        # -----------------------------------------------
        # CONFIGURAÇÃO ATUAL
        # -----------------------------------------------

        self.autor = ""
        self.estado = "normal"
        self.podemover = True

        # -----------------------------------------------
        # SPRITE DO ESTADO
        # -----------------------------------------------

        self.sprite_estado = None

        # -----------------------------------------------
        # POSIÇÃO DA CAIXA
        # -----------------------------------------------

        self.caixa_rect = pygame.Rect(
            MARGEM,
            altura - ALTURA_CAIXA - MARGEM,
            largura - MARGEM * 2,
            ALTURA_CAIXA
        )


    # =====================================================
    # INICIAR DIÁLOGO
    # =====================================================

    def iniciar(self, indice=0, dialogos=None):

        if dialogos is not None:
            self.dialogos = dialogos

        if not self.dialogos:
            return

        self.indice = indice

        self.ativo = True

        self.carregar_dialogo()

    def iniciar_boss(self, identificador):
        dialogos = BOSS_DIALOGOS.get(identificador)
        if dialogos:
            self.iniciar(0, dialogos)


    # =====================================================
    # CARREGAR DIÁLOGO ATUAL
    # =====================================================

    def carregar_dialogo(self):

        if self.indice >= len(self.dialogos):

            self.ativo = False

            return

        dialogo = self.dialogos[self.indice]

        self.autor = dialogo.get(
            "autor",
            ""
        )

        self.estado = dialogo.get(
            "estado",
            "normal"
        )

        self.texto_completo = dialogo.get(
            "fala",
            ""
        )

        self.podemover = dialogo.get(
            "podemover",
            True
        )

        # -----------------------------------------------
        # RESET DA DIGITAÇÃO
        # -----------------------------------------------

        self.texto_digitado = ""

        self.letras_mostradas = 0

        self.terminou_digitacao = False

        self.ultimo_tempo_letra = pygame.time.get_ticks()

        # -----------------------------------------------
        # CARREGAR SPRITE
        # -----------------------------------------------

        self.carregar_sprite_estado()


    # =====================================================
    # CARREGAR SPRITE DO ESTADO
    # =====================================================

    def carregar_sprite_estado(self):

        self.sprite_estado = None

        caminho = (
            "assets/dialogos/"
            + self.estado
            + ".png"
        )

        try:

            imagem = pygame.image.load(
                caminho
            ).convert_alpha()

            self.sprite_estado = pygame.transform.scale(
                imagem,
                (
                    80,
                    80
                )
            )

        except:

            self.sprite_estado = None


    # =====================================================
    # AVANÇAR DIÁLOGO
    # =====================================================

    def avancar(self):

        if not self.ativo:
            return

        # -----------------------------------------------
        # SE AINDA ESTÁ DIGITANDO
        # -----------------------------------------------

        if not self.terminou_digitacao:

            self.texto_digitado = self.texto_completo

            self.letras_mostradas = len(
                self.texto_completo
            )

            self.terminou_digitacao = True

            return

        # -----------------------------------------------
        # PRÓXIMO DIÁLOGO
        # -----------------------------------------------

        self.indice += 1

        if self.indice >= len(self.dialogos):

            self.ativo = False

            return

        self.carregar_dialogo()


    # =====================================================
    # ATUALIZAR
    # =====================================================

    def atualizar(self):

        if not self.ativo:
            return

        agora = pygame.time.get_ticks()

        # -----------------------------------------------
        # DIGITAÇÃO
        # -----------------------------------------------

        if not self.terminou_digitacao:

            if (
                agora - self.ultimo_tempo_letra
                >= VELOCIDADE_DIGITACAO
            ):

                if self.letras_mostradas < len(
                    self.texto_completo
                ):

                    self.letras_mostradas += 1

                    self.texto_digitado = (
                        self.texto_completo[
                            :self.letras_mostradas
                        ]
                    )

                    self.ultimo_tempo_letra = agora

                else:

                    self.terminou_digitacao = True


    # =====================================================
    # QUEBRAR TEXTO
    # =====================================================

    def quebrar_texto(
        self,
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
                + palavra
                + " "
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
                    + " "
                )

        if linha_atual:

            linhas.append(
                linha_atual.strip()
            )

        return linhas


    # =====================================================
    # DESENHAR
    # =====================================================

    def desenhar(self, tela):

        if not self.ativo:
            return

        # -----------------------------------------------
        # CAIXA
        # -----------------------------------------------

        pygame.draw.rect(
            tela,
            COR_CAIXA,
            self.caixa_rect
        )

        pygame.draw.rect(
            tela,
            COR_BORDA,
            self.caixa_rect,
            3
        )

        # -----------------------------------------------
        # NOME DO AUTOR
        # -----------------------------------------------

        superficie_nome = self.fonte_nome.render(
            self.autor,
            True,
            COR_NOME
        )

        tela.blit(
            superficie_nome,
            (
                self.caixa_rect.x + 20,
                self.caixa_rect.y + 12
            )
        )

        # -----------------------------------------------
        # SPRITE DO ESTADO
        # -----------------------------------------------

        espaco_sprite = 100

        if self.sprite_estado is not None:

            tela.blit(
                self.sprite_estado,
                (
                    self.caixa_rect.right
                    - espaco_sprite,
                    self.caixa_rect.y
                    + 25
                )
            )

        # -----------------------------------------------
        # TEXTO
        # -----------------------------------------------

        largura_texto = (
            self.caixa_rect.width
            - 40
            - espaco_sprite
        )

        linhas = self.quebrar_texto(
            self.texto_digitado,
            self.fonte_texto,
            largura_texto
        )

        texto_y = (
            self.caixa_rect.y
            + 50
        )

        for linha in linhas:

            superficie = self.fonte_texto.render(
                linha,
                True,
                COR_TEXTO
            )

            tela.blit(
                superficie,
                (
                    self.caixa_rect.x + 20,
                    texto_y
                )
            )

            texto_y += (
                self.fonte_texto.get_height()
                + 5
            )

        # -----------------------------------------------
        # INDICADOR DE CONTINUAR
        # -----------------------------------------------

        if self.terminou_digitacao:

            pontos = "..."

            superficie = self.fonte_texto.render(
                pontos,
                True,
                COR_TEXTO
            )

            tela.blit(
                superficie,
                (
                    self.caixa_rect.right - 40,
                    self.caixa_rect.bottom - 35
                )
            )


    # =====================================================
    # EVENTOS
    # =====================================================

    def processar_evento(self, evento):

        if not self.ativo:
            return

        if evento.type == pygame.KEYDOWN:

            if evento.key in (
                pygame.K_RETURN,
                pygame.K_SPACE,
                pygame.K_z
            ):

                self.avancar()


    # =====================================================
    # PODE MOVER
    # =====================================================

    def pode_mover(self):

        if not self.ativo:

            return True

        return self.podemover