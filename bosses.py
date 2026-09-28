import math
import os
import random

import pygame

from config import ALTURA, LARGURA, TAMANHO_TILE
from colisao import eh_parede


# Adicione novos identificadores nesta lista quando novos bosses existirem.
BOSS_ORDEM = [
    "pbrr",
    "boss2",
    "boss3",
    "boss4",
    "boss5",
    "boss6",
    "boss7"
]

# Escolha individualmente para cada boss:
# True = mostra a queda/entrada; False = começa já na posição normal.
ANIMACAO_ENTRADA_BOSS = {
    "pbrr": True,
    "boss2": False,
    "boss3": True,
    "boss4": True,
    "boss5": False,
    "boss6": True,
    "boss7": False,
}


# Dados individuais de cada boss.
# A ordem dos documentos é definida pela sequência de BOSS_ORDEM e pelo campo
# "documento" de cada boss. Para trocar o documento de um boss, basta alterar esse valor.
BOSS_DADOS = {
    "pbrr": {
        "nome": "PBRR",
        "vida": 25,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Petulante e ignorante, ainda cogita ser capaz de dar continuidade à trama de seus devaneios? \nSabes que só trará mais sofrimento a ti e ao seu vassalo. \nVossa mercê não possuis o necessário para suportar tamanha desgraça.",
        "drop_papel": False
    },
    "boss2": {
        "nome": "Boss 2",
        "vida": 35,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Petulante e ignorante, ainda cogita ser capaz de dar continuidade à trama de seus devaneios? \nSabes que só trará mais sofrimento a ti e ao seu vassalo. \nVossa mercê não possuis o necessário para suportar tamanha desgraça.",
        "drop_papel": True
    },
    "boss3": {
        "nome": "Boss 3",
        "vida": 40,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Monstro! Tendes noção que não passas disso...\nAmiudadamente continuas a torturar sua pessoa e aquele que vos acompanha.\nContudo, não permitirei que prossigas!",
        "drop_papel": True
    },
    "boss4": {
        "nome": "Boss 4",
        "vida": 50,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Indescritível! Indescritivel é o ódio que sinto por sua pessoa!\nJá que não foram suficientes as criaturas minhas, trarei fim a este pequeno contratempo com a mão de quem a vós delata.\nPrepare-se para experimentar o verdadeiro temor... ",
        "drop_papel": True
    },
    "boss5": {
        "nome": "Boss 5",
        "vida": 80,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Boss 5\nO confronto cresce.",
        "drop_papel": False
    },
    "boss6": {
        "nome": "Boss 6",
        "vida": 50,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Boss 6\nA ameaça se revela.",
        "drop_papel": False
    },
    "boss7": {
        "nome": "Boss 7",
        "vida": 70,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Cuidado com o botão da próxima sala, ele pode ser perigoso...",
        "drop_papel": True
    }
}


VELOCIDADE_BALA = 10
INTERVALO_DISPARO = 250
DURACAO_QUEDA_BOSS_MS = 500
TEMPO_DESAPARECER_BOSS_MS = 3000
BOSS5_QUANTIDADE_FILEIRAS = 5
BOSS5_INTERVALO_ATAQUE_MS = 350
BOSS5_VELOCIDADE_ATAQUE = 7
BOSS5_VELOCIDADE_ORBITA = 0.7
BOSS5_AMPLITUDE_X = 210
BOSS5_AMPLITUDE_Y = 80
BOSS5_DURACAO_PARADO_MS = 750
BOSS5_ATRASO_ATAQUE_ABERTURA_MS = 1200
BOSS5_DURACAO_FORMACAO_MS = 900
BOSS5_VELOCIDADE_ATAQUE7 = 5
BOSS5_QUANTIDADE_ESTILHACOS = 5
BOSS5_PASSO_FUSAO_PX = 1
BOSS5_FLASH_DURACAO_MS = 2000
BOSS5_INTERVALO_PEAO_MS = 2000
BOSS5_PEAO_FADE_IN_MS = 500
BOSS5_PEAO_SAIDA_MS = 300
BOSS5_PEAO_FADE_OUT_MS = 400


class GerenciadorBosses:

    def __init__(self, bosses, jogador):
        self.bosses = bosses
        self.jogador = jogador
        self.indice = -1
        self.boss = None
        self.bosses_ativos = []
        self.bosses_visiveis = []
        self.identificador = None
        self.dados = None
        self.vida = 0
        self.vida_maxima = 0
        self.finalizado = False
        self.mensagem = ""
        self.mensagem_expira = 0
        self.balas = []
        self.boss5_ataques = []
        self.boss5_proximo_ataque_ms = 0
        self.sprite_ataque_boss5 = self.bosses["boss5"].sprite_ataque_2
        self.sprite_ataque7 = pygame.image.load(
            "assets/ataques/ataque7.png"
        ).convert_alpha()
        self.boss5_orbita_fase = 0.0
        self.boss5_ultimo_update_ms = None
        self.boss5_movimento_inicio_ms = None
        self.boss5_combate_inicio_ms = None
        self.boss5_ataque_abertura_usado = False
        self.boss5_ataque_abertura_inicio_ms = 0
        self.boss5_ataque7 = None
        self.boss5_proxima_invocacao_ms = 0
        self.boss5_invocacao = None
        self.sprite_tile_boss5 = pygame.transform.scale(
            pygame.image.load("assets/ataques/CMV.png").convert_alpha(),
            (TAMANHO_TILE, TAMANHO_TILE)
        )
        self.sprite_peao_boss5 = pygame.transform.scale(
            pygame.image.load("assets/ataques/Peão.png").convert_alpha(),
            (TAMANHO_TILE, TAMANHO_TILE)
        )
        self.boss5_fusao = None
        self.tempo_ultimo_disparo = 0
        self.direcao_disparo = pygame.Vector2(0, 1)
        self.dialogo_pendente = None
        self.iniciado = False
        self.sprite_bala = pygame.image.load(
            "assets/ataques/ataque1.png"
        ).convert_alpha()
        self.sprite_papel = pygame.image.load(
            "assets/Documentos/Papel.png"
        ).convert_alpha()
        self.sprite_papel = pygame.transform.scale(
            self.sprite_papel,
            (
                max(1, int(self.sprite_papel.get_width() * 1.35)),
                max(1, int(self.sprite_papel.get_height() * 1.35))
            )
        )
        self.sprites_chave = [
            pygame.image.load(
                f"assets/Documentos/chave{i}.png").convert_alpha()
            for i in range(7)
        ]
        self.sprites_chave = [
            pygame.transform.scale(
                sprite,
                (
                    max(1, int(sprite.get_width() * 1.4)),
                    max(1, int(sprite.get_height() * 1.4))
                )
            )
            for sprite in self.sprites_chave
        ]
        self.item_papel = None
        self.documento_em_exibicao = None
        self.documento_ativo = False
        self.chave_coletada = False
        self.efeito_derrota = None
        self.posicao_ultimo_boss = None
        self._proximo_boss_em_execucao = False

    def iniciar(self):
        if self.iniciado:
            return

        self.iniciado = True
        self._proximo_boss()

    def _proximo_boss(self):
        if self._proximo_boss_em_execucao:
            return

        self._proximo_boss_em_execucao = True
        try:
            self._limpar_ataques()
            self.indice += 1

            while self.indice < len(BOSS_ORDEM):
                identificador = BOSS_ORDEM[self.indice]
                boss = self.bosses.get(identificador)
                dados = BOSS_DADOS.get(identificador)

                if boss is not None and dados is not None:
                    self.identificador = identificador
                    self.boss = boss
                    if identificador == "boss5":
                        self.bosses_ativos = [
                            self.bosses["boss3"],
                            self.bosses["boss4"]
                        ]
                        self.bosses_visiveis = [
                            self.bosses["boss3"],
                            self.bosses["boss4"]
                        ]
                    else:
                        self.bosses_ativos = [boss]
                        self.bosses_visiveis = [boss]
                        if identificador == "boss4":
                            self.bosses_visiveis.insert(
                                0,
                                self.bosses["boss3"]
                            )
                    self.dados = dados
                    for indice_ativo, boss_ativo in enumerate(self.bosses_ativos):
                        if identificador == "boss5":
                            boss_ativo.ia_ativa = False
                            boss_ativo.animacao_entrada_ativa = False
                            boss_ativo.entrando = False
                            boss_ativo.ataques.clear()
                            continue

                        boss_ativo.efeito_derrota = None
                        boss_ativo.animacao_entrada_ativa = ANIMACAO_ENTRADA_BOSS.get(
                            identificador,
                            True
                        )
                        boss_ativo.dano_ataque = dados["dano"]
                        boss_ativo.ia_ativa = False if identificador in (
                            "boss3", "boss4", "boss5", "boss6", "boss7"
                        ) else True
                        boss_ativo.entrando = False
                        boss_ativo.entrada_iniciada = False
                        boss_ativo.entrada_alpha = 255
                        boss_ativo.entrada_origem_y = boss_ativo.y
                        boss_ativo.entrada_destino_y = boss_ativo.y
                        sprite = boss_ativo.pegar_sprite()
                        destino_y = (ALTURA - sprite.get_height()) // 2

                        if identificador in ("boss3", "boss4"):
                            offset_x = 100 if identificador == "boss3" else -100
                            boss_ativo.x = (
                                LARGURA - sprite.get_width()
                            ) // 2 + offset_x
                            boss_ativo.y = -sprite.get_height() - 20
                            if not boss_ativo.animacao_entrada_ativa:
                                boss_ativo.y = destino_y
                        elif identificador == "boss6":
                            boss_ativo.x = (
                                LARGURA - sprite.get_width()
                            ) // 2
                            boss_ativo.y = -sprite.get_height() - 20
                            boss_ativo.entrada_origem_y = boss_ativo.y
                            boss_ativo.entrada_destino_y = destino_y
                            self.posicao_ultimo_boss = None
                        elif (
                            self.posicao_ultimo_boss is not None
                            and identificador != "boss5"
                        ):
                            boss_ativo.x = self.posicao_ultimo_boss[0]
                            boss_ativo.y = -sprite.get_height() - 20
                            if not boss_ativo.animacao_entrada_ativa:
                                boss_ativo.y = self.posicao_ultimo_boss[1]
                            self.posicao_ultimo_boss = None
                        else:
                            boss_ativo.x = (LARGURA - sprite.get_width()) // 2
                            boss_ativo.y = -sprite.get_height() - 20
                            if not boss_ativo.animacao_entrada_ativa:
                                boss_ativo.y = destino_y

                    self.vida = dados["vida"]
                    self.vida_maxima = self.vida

                    if identificador == "boss5":
                        sprite = self.boss.pegar_sprite()
                        self.boss.x = (LARGURA - sprite.get_width()) // 2
                        self.boss.y = (
                            ALTURA // 2 - 100 - sprite.get_height() // 2
                        )
                        self.boss.ia_ativa = False
                        self.boss.sprite_boss5_atual = (
                            self.boss.sprites_boss5["parado"][0]
                        )
                        self.boss5_orbita_fase = 0.0
                        self.boss5_ultimo_update_ms = pygame.time.get_ticks()
                        self.boss5_movimento_inicio_ms = None
                        self.boss5_combate_inicio_ms = None
                        self.boss5_ataque_abertura_usado = False
                        self.boss5_ataque7 = None
                        self.boss5_proxima_invocacao_ms = (
                            pygame.time.get_ticks() + BOSS5_INTERVALO_PEAO_MS
                        )
                        self.boss5_invocacao = None
                        self.posicao_ultimo_boss = None
                        self._iniciar_fusao_boss5()

                    if identificador == "boss6":
                        self.boss.iniciar_animacao_boss6()
                        self.boss.configurar_padrao_ataque("boss6")
                    elif identificador == "boss7":
                        self.boss.configurar_padrao_ataque("boss6")
                    if self.indice > 0 and identificador != "boss5":
                        self.dialogo_pendente = identificador
                    self.mensagem = (
                        f"Boss {self.indice + 1}/{len(BOSS_ORDEM)}: "
                        f"{dados['nome']}"
                    )
                    self.mensagem_expira = pygame.time.get_ticks() + 2200
                    return

                self.indice += 1

            self.boss = None
            self.bosses_ativos = []
            self.bosses_visiveis = []
            self.identificador = None
            self.dados = None
            self.finalizado = True
            self.mensagem = "Todos os bosses foram derrotados!"
            self.mensagem_expira = pygame.time.get_ticks() + 5000
        finally:
            self._proximo_boss_em_execucao = False

    def consumir_dialogo_pendente(self):
        identificador = self.dialogo_pendente
        self.dialogo_pendente = None
        return identificador

    def iniciar_entrada_boss_ativo(self):
        if self.boss is None:
            return

        if self.boss.animacao_entrada_ativa and not self.boss.entrada_iniciada:
            sprite = self.boss.pegar_sprite()
            destino_y = (ALTURA - sprite.get_height()) // 2
            self.boss.iniciar_entrada(destino_y)

    def _iniciar_fusao_boss5(self):
        agora = pygame.time.get_ticks()
        boss3 = self.bosses["boss3"]
        boss4 = self.bosses["boss4"]
        sprite3 = self._obter_sprite_derrota(boss3)
        sprite4 = self._obter_sprite_derrota(boss4)
        centro3 = pygame.Vector2(
            boss3.x + sprite3.get_width() / 2,
            boss3.y + sprite3.get_height() / 2
        )
        centro4 = pygame.Vector2(
            boss4.x + sprite4.get_width() / 2,
            boss4.y + sprite4.get_height() / 2
        )
        self.boss5_fusao = {
            "fase": "unindo",
            "inicio": agora,
            "distancia_inicial": max(1, abs(centro3.x - centro4.x)),
            "centros_unidos": centro3.distance_to(centro4) <= 0.5
        }

        for boss, sprite, centro_x in (
            (boss3, sprite3, centro3.x),
            (boss4, sprite4, centro4.x)
        ):
            boss.efeito_derrota = {
                "inicio": agora - DURACAO_QUEDA_BOSS_MS,
                "duracao": BOSS5_FLASH_DURACAO_MS,
                "duracao_queda": DURACAO_QUEDA_BOSS_MS,
                "sprite_final": sprite,
                "brilho": 1.0,
                "aplicar_brilho": True,
                "persistir": True,
                "angulo": 90
            }

    def _atualizar_fusao_boss5(self):
        agora = pygame.time.get_ticks()
        fusao = self.boss5_fusao
        if fusao["fase"] == "unindo":
            centros_sprites = []
            boss3 = self.bosses["boss3"]
            boss4 = self.bosses["boss4"]
            sprite3 = boss3.efeito_derrota["sprite_final"]
            sprite4 = boss4.efeito_derrota["sprite_final"]
            centro3_x = boss3.x + sprite3.get_width() / 2
            centro4_x = boss4.x + sprite4.get_width() / 2

            if centro3_x > centro4_x:
                boss3.x -= BOSS5_PASSO_FUSAO_PX
                boss4.x += BOSS5_PASSO_FUSAO_PX
            elif centro3_x < centro4_x:
                boss3.x += BOSS5_PASSO_FUSAO_PX
                boss4.x -= BOSS5_PASSO_FUSAO_PX

            for boss in (boss3, boss4):
                sprite = boss.efeito_derrota["sprite_final"]
                centros_sprites.append(
                    pygame.Vector2(
                        boss.x + sprite.get_width() / 2,
                        boss.y + sprite.get_height() / 2
                    )
                )

            distancia_centros = centros_sprites[0].distance_to(
                centros_sprites[1]
            )
            distancia_x = abs(
                centros_sprites[0].x - centros_sprites[1].x
            )
            progresso = 1 - min(
                1.0,
                distancia_x / fusao["distancia_inicial"]
            )
            for identificador in ("boss3", "boss4"):
                self.bosses[identificador].efeito_derrota["brilho"] = (
                    1 + progresso * 0.6
                )

            if distancia_centros <= 0.5:
                fusao["centros_unidos"] = True

            if (
                not fusao["centros_unidos"]
                or agora - fusao["inicio"] < BOSS5_FLASH_DURACAO_MS
            ):
                return

        self.boss5_fusao = None
        self.bosses_ativos = [self.boss]
        self.bosses_visiveis = [self.boss]
        self.boss.efeito_derrota = None
        self.boss.sprite_boss5_atual = self.boss.sprites_boss5["parado"][0]
        self.boss5_orbita_fase = 0.0
        self.boss5_ultimo_update_ms = agora
        self.boss5_movimento_inicio_ms = None
        self.boss5_combate_inicio_ms = None
        self.boss5_ataque_abertura_usado = False
        self.boss5_ataque7 = None
        self.boss5_proxima_invocacao_ms = agora + BOSS5_INTERVALO_PEAO_MS
        self.boss5_invocacao = None
        if self.indice > 0:
            self.dialogo_pendente = "boss5"

    def alpha_flash_boss5(self):
        if self.boss5_fusao is None:
            return 0

        elapsed = pygame.time.get_ticks() - self.boss5_fusao["inicio"]
        progresso = min(1.0, elapsed / BOSS5_FLASH_DURACAO_MS)
        return int(255 * progresso)

    def atualizar(self, interface):
        if not self.iniciado or self.boss is None:
            return

        if self.boss5_fusao is not None:
            self._atualizar_fusao_boss5()
            return

        if self.efeito_derrota is not None:
            self._atualizar_efeito_derrota()
            return

        if self.item_papel is not None or self.documento_ativo:
            return

        if any(boss.esta_em_entrada() for boss in self.bosses_ativos):
            for boss in self.bosses_ativos:
                boss.atualizar_entrada()
            return

        if self.identificador == "boss5":
            self._atualizar_boss5(interface)
        else:
            for boss in self.bosses_ativos:
                boss.atualizar(self.jogador, interface)
        self._atualizar_balas()

        teclas = pygame.key.get_pressed()
        if any(
            teclas[tecla]
            for tecla in (
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_DOWN
            )
        ):
            self._disparar_se_pronto()

    def _obter_direcao_disparo(self):
        direcao = pygame.Vector2(
            self.jogador.direcao_mira
        )
        direcao.normalize_ip()
        return direcao

    def _disparar_se_pronto(self):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_disparo < INTERVALO_DISPARO:
            return

        self.direcao_disparo = self._obter_direcao_disparo()
        origem = self.jogador.obter_rect_dano().center
        self.balas.append({
            "posicao": pygame.Vector2(origem),
            "direcao": self.direcao_disparo.copy(),
            "disparado_ms": agora
        })
        self.tempo_ultimo_disparo = agora

    def _limpar_ataques(self):
        self.balas.clear()
        self.boss5_ataques.clear()
        self.boss5_ataque7 = None
        self.boss5_invocacao = None
        for boss in self.bosses.values():
            boss.ataques.clear()

    def _atualizar_ataques_boss5(self, interface):
        agora = pygame.time.get_ticks()
        if agora >= self.boss5_proximo_ataque_ms:
            altura_fileira = (ALTURA / 2) / BOSS5_QUANTIDADE_FILEIRAS
            largura_sprite = self.sprite_ataque_boss5.get_width()
            for indice in range(BOSS5_QUANTIDADE_FILEIRAS):
                direcao = -1 if indice % 2 == 0 else 1
                x = (
                    LARGURA + largura_sprite / 2
                    if direcao < 0
                    else -largura_sprite / 2
                )
                self.boss5_ataques.append({
                    "posicao": pygame.Vector2(
                        x,
                        (indice + 0.5) * altura_fileira
                    ),
                    "direcao": direcao
                })
            self.boss5_proximo_ataque_ms = (
                agora + BOSS5_INTERVALO_ATAQUE_MS
            )

        rect_jogador = self.jogador.obter_rect_dano()
        novos_ataques = []
        for ataque in self.boss5_ataques:
            ataque["posicao"].x += (
                ataque["direcao"] * BOSS5_VELOCIDADE_ATAQUE
            )
            rect_ataque = self.sprite_ataque_boss5.get_rect(
                center=ataque["posicao"]
            )
            if rect_ataque.colliderect(rect_jogador):
                direcao_ataque = pygame.Vector2(ataque["direcao"], 0)
                interface.receber_dano(
                    1,
                    self.jogador,
                    direcao_ataque,
                    direcao_ataque * BOSS5_VELOCIDADE_ATAQUE
                )
                continue

            if rect_ataque.right >= 0 and rect_ataque.left <= LARGURA:
                novos_ataques.append(ataque)

        self.boss5_ataques = novos_ataques

    def _atualizar_invocacao_boss5(self, agora, interface):
        if self.boss5_invocacao is None:
            if agora < self.boss5_proxima_invocacao_ms:
                return
            self.boss5_invocacao = {
                "inicio": agora,
                "centro": pygame.Vector2(self.jogador.obter_rect().center),
                "dano_causado": False
            }
            self.boss5_proxima_invocacao_ms = (
                agora + BOSS5_INTERVALO_PEAO_MS
            )
            return

        elapsed = agora - self.boss5_invocacao["inicio"]
        duracao_total = (
            BOSS5_PEAO_FADE_IN_MS
            + BOSS5_PEAO_SAIDA_MS
            + BOSS5_PEAO_FADE_OUT_MS
        )
        if (
            elapsed >= BOSS5_PEAO_FADE_IN_MS
            and not self.boss5_invocacao["dano_causado"]
        ):
            centro_x, centro_y = self.boss5_invocacao["centro"]
            rect_tile = self.sprite_tile_boss5.get_rect(
                center=(centro_x, centro_y)
            )
            rect_peao = self.sprite_peao_boss5.get_rect(
                topleft=(
                    centro_x - self.sprite_peao_boss5.get_width() / 2,
                    rect_tile.top
                )
            )
            if rect_peao.colliderect(self.jogador.obter_rect_dano()):
                direcao = pygame.Vector2(0, -1)
                interface.receber_dano(
                    1,
                    self.jogador,
                    direcao,
                    pygame.Vector2(0, -3)
                )
                self.boss5_invocacao["dano_causado"] = True

        if elapsed >= duracao_total:
            self.boss5_invocacao = None

    def desenhar_invocacao_boss5(self, tela):
        if self.identificador != "boss5" or self.boss5_invocacao is None:
            return

        invocacao = self.boss5_invocacao
        elapsed = pygame.time.get_ticks() - invocacao["inicio"]
        centro_x, centro_y = invocacao["centro"]
        rect_tile = self.sprite_tile_boss5.get_rect(
            center=(centro_x, centro_y)
        )
        angulo = (elapsed * 0.36) % 360
        tile = pygame.transform.rotate(self.sprite_tile_boss5, angulo)
        tela.blit(tile, tile.get_rect(center=rect_tile.center))

        altura_peao = self.sprite_peao_boss5.get_height()
        largura_peao = self.sprite_peao_boss5.get_width()
        inicio_saida = BOSS5_PEAO_FADE_IN_MS
        inicio_fade_out = inicio_saida + BOSS5_PEAO_SAIDA_MS

        if elapsed < BOSS5_PEAO_FADE_IN_MS:
            progresso = max(0.0, elapsed / BOSS5_PEAO_FADE_IN_MS)
            altura_visivel = int(altura_peao * progresso)
            if altura_visivel <= 0:
                return
            sprite = self.sprite_peao_boss5.subsurface(
                pygame.Rect(
                    0,
                    altura_peao - altura_visivel,
                    largura_peao,
                    altura_visivel
                )
            ).copy()
            sprite.set_alpha(int(progresso * 255))
            posicao = (
                int(centro_x - largura_peao / 2),
                int(rect_tile.bottom - altura_visivel)
            )
            tela.blit(sprite, posicao)
            return

        if elapsed < inicio_fade_out:
            progresso = min(
                1.0,
                (elapsed - inicio_saida) / BOSS5_PEAO_SAIDA_MS
            )
            alpha = 255
            deslocamento_y = progresso * (TAMANHO_TILE // 2)
        else:
            progresso = min(
                1.0,
                (elapsed - inicio_fade_out) / BOSS5_PEAO_FADE_OUT_MS
            )
            alpha = int(255 * (1 - progresso))
            deslocamento_y = (
                TAMANHO_TILE // 2
                + progresso * (TAMANHO_TILE // 2)
            )

        peao = self.sprite_peao_boss5.copy()
        peao.set_alpha(alpha)
        tela.blit(
            peao,
            (
                int(centro_x - largura_peao / 2),
                int(rect_tile.top - deslocamento_y)
            )
        )

    def desenhar_ataques_boss5(self, tela):
        if self.identificador != "boss5":
            return

        for ataque in self.boss5_ataques:
            tela.blit(
                self.sprite_ataque_boss5,
                self.sprite_ataque_boss5.get_rect(
                    center=ataque["posicao"]
                )
            )

        if self.boss5_ataque7 is not None:
            sprite = self.boss5_ataque7.get("sprite")
            if sprite is not None:
                tela.blit(
                    sprite,
                    sprite.get_rect(center=self.boss5_ataque7["posicao"])
                )

    def _atualizar_orbita_boss5(self, agora):
        boss = self.boss
        if self.boss5_movimento_inicio_ms is None:
            self.boss5_movimento_inicio_ms = agora

        tempo_parado = agora - self.boss5_movimento_inicio_ms
        if tempo_parado < BOSS5_DURACAO_PARADO_MS:
            sprites_parado = boss.sprites_boss5["parado"]
            indice = min(
                len(sprites_parado) - 1,
                tempo_parado // 250
            )
            boss.sprite_boss5_atual = sprites_parado[indice]
            self.boss5_ultimo_update_ms = agora
            return

        tempo_anterior = self.boss5_ultimo_update_ms
        delta = 0 if tempo_anterior is None else min(
            0.05,
            max(0, (agora - tempo_anterior) / 1000)
        )
        self.boss5_ultimo_update_ms = agora
        self.boss5_orbita_fase += delta * BOSS5_VELOCIDADE_ORBITA

        fase = self.boss5_orbita_fase
        centro_x = LARGURA / 2 + BOSS5_AMPLITUDE_X * math.sin(fase)
        centro_y = (
            ALTURA / 2 - 100
            + BOSS5_AMPLITUDE_Y * math.sin(fase) * math.cos(fase)
        )
        sprite = boss.pegar_sprite()
        centro_anterior_x = boss.x + sprite.get_width() / 2
        boss.x = centro_x - sprite.get_width() / 2
        boss.y = centro_y - sprite.get_height() / 2
        boss.movimento_x = 0
        boss.movimento_y = 0
        boss.esta_se_movendo = False

        if centro_x - centro_anterior_x > 0.1:
            boss.direcao = "direita"
            boss.sprite_boss5_atual = boss.sprites_boss5["direita"]
        elif centro_x - centro_anterior_x < -0.1:
            boss.direcao = "esquerda"
            boss.sprite_boss5_atual = boss.sprites_boss5["esquerda"]
        elif self.boss5_ataque7 is None:
            sprites_parado = boss.sprites_boss5["parado"]
            boss.sprite_boss5_atual = sprites_parado[(
                agora // 250) % len(sprites_parado)]

    def _explodir_ataque7_boss5(self, posicao):
        agora = pygame.time.get_ticks()
        for indice in range(BOSS5_QUANTIDADE_ESTILHACOS):
            angulo = 2 * math.pi * indice / BOSS5_QUANTIDADE_ESTILHACOS
            direcao = pygame.Vector2(math.cos(angulo), math.sin(angulo))
            self.boss.ataques.append({
                "posicao": pygame.Vector2(posicao),
                "direcao": direcao,
                "disparado_ms": agora,
                "acertou": False,
                "tipo": "ataque3",
                "dano": 1,
                "sprite": self.boss.sprite_ataque_3
            })

    def _atualizar_ataque_abertura_boss5(self, interface, agora):
        if self.boss5_combate_inicio_ms is None:
            self.boss5_combate_inicio_ms = agora

        if (
            not self.boss5_ataque_abertura_usado
            and agora - self.boss5_combate_inicio_ms
            >= BOSS5_ATRASO_ATAQUE_ABERTURA_MS
        ):
            self.boss5_ataque_abertura_usado = True
            self.boss5_ataque_abertura_inicio_ms = agora
            self.boss5_ataque7 = {
                "fase": "formando",
                "inicio_ms": agora,
                "posicao": pygame.Vector2(0, 0),
                "direcao": pygame.Vector2(),
                "sprite": None
            }

        ataque = self.boss5_ataque7
        if ataque is None:
            return

        if ataque["fase"] == "formando":
            elapsed = agora - ataque["inicio_ms"]
            progresso = min(1.0, elapsed / BOSS5_DURACAO_FORMACAO_MS)
            frames_ataque = self.boss.sprites_boss5["ataque"]
            indice_frame = min(
                len(frames_ataque) - 1,
                int(progresso * len(frames_ataque))
            )
            self.boss.sprite_boss5_atual = frames_ataque[indice_frame]

            largura = max(1, int(self.sprite_ataque7.get_width() * progresso))
            altura = max(1, int(self.sprite_ataque7.get_height() * progresso))
            ataque["sprite"] = pygame.transform.scale(
                self.sprite_ataque7,
                (largura, altura)
            )
            ataque["posicao"] = pygame.Vector2(
                self.boss.x + self.boss.pegar_sprite().get_width() / 2,
                self.boss.y - altura / 2 - 12
            )

            if progresso >= 1.0:
                alvo = pygame.Vector2(self.jogador.obter_rect_dano().center)
                ataque["direcao"] = alvo - ataque["posicao"]
                if ataque["direcao"].length_squared() == 0:
                    ataque["direcao"] = pygame.Vector2(0, 1)
                else:
                    ataque["direcao"].normalize_ip()
                ataque["fase"] = "lancado"
                ataque["disparado_ms"] = agora
                ataque["sprite"] = self.sprite_ataque7
            return

        ataque["posicao"] += (
            ataque["direcao"] * BOSS5_VELOCIDADE_ATAQUE7
        )
        rect_ataque = self.sprite_ataque7.get_rect(
            center=ataque["posicao"]
        )
        acertou_jogador = rect_ataque.colliderect(
            self.jogador.obter_rect_dano()
        )
        pontos = (
            (rect_ataque.left, rect_ataque.top),
            (rect_ataque.right - 1, rect_ataque.top),
            (rect_ataque.left, rect_ataque.bottom - 1),
            (rect_ataque.right - 1, rect_ataque.bottom - 1)
        )
        acertou_parede = (
            rect_ataque.left <= 0
            or rect_ataque.right >= LARGURA
            or rect_ataque.top <= 0
            or rect_ataque.bottom >= ALTURA
            or (
                agora - ataque["disparado_ms"] >= 150
                and any(eh_parede(x, y) for x, y in pontos)
            )
        )

        if acertou_jogador or acertou_parede:
            if acertou_jogador:
                interface.receber_dano(
                    3,
                    self.jogador,
                    ataque["direcao"],
                    ataque["direcao"] * BOSS5_VELOCIDADE_ATAQUE7
                )
            self._explodir_ataque7_boss5(ataque["posicao"])
            self.boss5_ataque7 = None

    def _atualizar_boss5(self, interface):
        agora = pygame.time.get_ticks()
        self._atualizar_orbita_boss5(agora)
        self._atualizar_invocacao_boss5(agora, interface)
        self._atualizar_ataques_boss5(interface)
        self._atualizar_ataque_abertura_boss5(interface, agora)
        self.boss.atualizar_ataques(self.jogador, interface)

    def _iniciar_efeito_derrota(self):
        self.posicao_ultimo_boss = (self.boss.x, self.boss.y)
        pode_cair = self.identificador not in ("pbrr", "boss6")
        self.efeito_derrota = {
            "inicio": pygame.time.get_ticks(),
            "duracao": (
                TEMPO_DESAPARECER_BOSS_MS
                if pode_cair
                else 1600 if self.identificador == "boss6" else 1200
            ),
            "duracao_queda": DURACAO_QUEDA_BOSS_MS if pode_cair else 0,
            "offset_x": 0.0,
            "offset_y": 0.0,
            "sprite_final": self._obter_sprite_derrota(),
            "brilho": 1.0,
            "drop_papel": self.dados.get("drop_papel", True),
            "aplicar_brilho": self.identificador == "pbrr",
            "persistir": self.identificador in ("boss3", "boss4")
        }
        if pode_cair:
            self.boss.efeito_derrota = self.efeito_derrota

    def _obter_sprite_derrota(self, boss=None):
        alvo = boss or self.boss
        if alvo is None:
            return None

        for sprites in (
            getattr(alvo, "direita", None),
            getattr(alvo, "frente", None),
            getattr(alvo, "esquerda", None),
            getattr(alvo, "costas", None)
        ):
            if isinstance(sprites, list) and len(sprites) >= 3:
                return sprites[2]

        return alvo.pegar_sprite()

    def _atualizar_efeito_derrota(self):
        agora = pygame.time.get_ticks()
        elapsed = agora - self.efeito_derrota["inicio"]
        duracao = self.efeito_derrota["duracao"]

        if elapsed >= duracao:
            boss_anterior = self.boss
            if self.efeito_derrota.get("drop_papel"):
                self._criar_item_papel(boss_anterior)
            self.efeito_derrota = None
            if not self.dados or not self.dados.get("drop_papel", True):
                self._proximo_boss()
            return

        progresso = elapsed / duracao
        if progresso < 0.25:
            tremor = 3.0 * progresso
            self.efeito_derrota["offset_x"] = random.uniform(-tremor, tremor)
            self.efeito_derrota["offset_y"] = random.uniform(
                -tremor * 0.5, tremor * 0.5)
            self.efeito_derrota["brilho"] = 1.0
        elif progresso < 0.8:
            self.efeito_derrota["offset_x"] = 0.0
            self.efeito_derrota["offset_y"] = 0.0
            if self.efeito_derrota.get("aplicar_brilho"):
                self.efeito_derrota["brilho"] = 1.0 + \
                    ((progresso - 0.25) / 0.55) * 2.5
            else:
                self.efeito_derrota["brilho"] = 1.0
        else:
            self.efeito_derrota["offset_x"] = 0.0
            self.efeito_derrota["offset_y"] = 0.0
            if self.efeito_derrota.get("aplicar_brilho"):
                self.efeito_derrota["brilho"] = 1.0 + \
                    ((progresso - 0.8) / 0.2) * 6.0
            else:
                self.efeito_derrota["brilho"] = 1.0

    def _obter_dados_drop(self, boss=None):
        return self.dados

    def _criar_item_papel(self, boss=None):
        alvo = boss or self.boss
        if alvo is None:
            return

        dados_drop = self._obter_dados_drop(alvo)
        if not dados_drop or not dados_drop.get("documento"):
            return

        tipo_drop = "chave" if self.identificador == "boss7" else "papel"
        if tipo_drop == "chave":
            frames = self.sprites_chave
            sprite = frames[0]
        else:
            frames = None
            sprite = self.sprite_papel

        rect = sprite.get_rect(
            center=alvo.obter_rect_alvo().center
        )
        rect.centery -= 12
        self.item_papel = {
            "rect": rect,
            "documento": dados_drop["documento"],
            "texto_documento": dados_drop.get("texto_documento"),
            "sprite": sprite,
            "frames": frames,
            "frame_index": 0,
            "frame_timer": 0,
            "frame_interval": 80,
            "tipo": tipo_drop,
            "vel_y": -6.5,
            "vel_x": random.uniform(-2.2, 2.2),
            "gravidade": 0.28,
            "angulo": random.choice([-5, 5]),
            "rotacao_vel": random.choice([-1.0, 1.0]),
            "quicada": True,
            "altura_quicada": 0.0,
            "tempo_quica": 0.0,
            "girando": True
        }

    def _iniciar_documento(
        self,
        documento,
        texto_documento=None,
        avancar_boss=True
    ):
        if not documento:
            return

        if not os.path.exists(documento):
            return

        imagem = pygame.image.load(documento).convert_alpha()
        nova_larg = max(1, int(imagem.get_width() * 1.5))
        nova_alt = max(1, int(imagem.get_height() * 1.5))
        imagem = pygame.transform.smoothscale(imagem, (nova_larg, nova_alt))

        if texto_documento is None and self.dados and self.dados.get("texto_documento"):
            texto_documento = self.dados["texto_documento"]

        if texto_documento:
            fonte = pygame.font.SysFont("arial", 18, bold=True)
            largura_max_texto = max(220, imagem.get_width() - 100)
            linhas = []

            for paragrafo in texto_documento.split("\n"):
                if not paragrafo.strip():
                    linhas.append("")
                    continue

                palavras = paragrafo.split()
                linha_atual = ""
                for palavra in palavras:
                    teste = f"{linha_atual} {palavra}".strip()
                    if fonte.size(teste)[0] <= largura_max_texto:
                        linha_atual = teste
                    else:
                        if linha_atual:
                            linhas.append(linha_atual)
                        linha_atual = palavra

                if linha_atual:
                    linhas.append(linha_atual)

            maior_largura = max(
                fonte.size(linha)[0] for linha in linhas
            ) if linhas else 0
            altura_total = sum(
                fonte.size(linha)[1] for linha in linhas
            ) + max(0, len(linhas) - 1) * 8
            painel = pygame.Surface(
                (maior_largura + 40, altura_total + 90),
                pygame.SRCALPHA
            )

            x_offset = 20
            y_offset = 70
            y_cursor = y_offset
            for linha in linhas:
                texto = fonte.render(linha, True, (94, 60, 35))
                painel.blit(texto, (x_offset, y_cursor))
                y_cursor += fonte.get_linesize() + 8

            base = pygame.Surface(
                (
                    imagem.get_width(),
                    max(imagem.get_height(), painel.get_height() + 30)
                ),
                pygame.SRCALPHA
            )
            base.blit(imagem, (0, 0))
            x_texto = max(0, (base.get_width() - painel.get_width()) // 2)
            y_texto = 0
            base.blit(painel, (x_texto, y_texto))
            imagem = base

        rect_documento = imagem.get_rect(center=(LARGURA // 2, ALTURA // 2))
        rect_documento.top -= 40
        rect_documento.centery += 340
        self.documento_em_exibicao = {
            "imagem": imagem,
            "alpha": 0,
            "fase": "in",
            "inicio": pygame.time.get_ticks(),
            "scroll": 0,
            "documento": documento,
            "rect": rect_documento,
            "avancar_boss": avancar_boss
        }
        self.documento_ativo = True

    def iniciar_documento_final(self, texto_documento):
        self._iniciar_documento(
            "assets/Documentos/Documento1.png",
            texto_documento,
            avancar_boss=False
        )

    def _obter_x_parede_impacto(self, rect, sentido):
        passo = max(1, TAMANHO_TILE // 4)
        for y in range(rect.top, rect.bottom + 1, passo):
            for x in range(rect.left, rect.right + 1, passo):
                if not eh_parede(int(x), int(y)):
                    continue

                tile_coluna = int(x // TAMANHO_TILE)
                tile_linha = int(y // TAMANHO_TILE)
                borda_tile = tile_coluna * TAMANHO_TILE
                borda_direita = (tile_coluna + 1) * TAMANHO_TILE

                if sentido > 0:
                    return max(0, borda_tile - rect.width)
                return min(LARGURA, borda_direita)

        return rect.x

    def _colidiu_com_parede_item(self, rect):
        pontos = [
            (rect.left + 2, rect.top + 2),
            (rect.right - 2, rect.top + 2),
            (rect.left + 2, rect.bottom - 2),
            (rect.right - 2, rect.bottom - 2),
        ]
        return any(eh_parede(int(x), int(y)) for x, y in pontos)

    def atualizar_documentos(self, jogador):
        if self.item_papel is not None:
            frames = self.item_papel.get("frames")
            if frames:
                self.item_papel["frame_timer"] += 1
                if self.item_papel["frame_timer"] >= self.item_papel["frame_interval"]:
                    self.item_papel["frame_timer"] = 0
                    self.item_papel["frame_index"] = (
                        self.item_papel["frame_index"] + 1
                    ) % len(frames)
                    self.item_papel["sprite"] = frames[self.item_papel["frame_index"]]

            self.item_papel["rect"].x += self.item_papel["vel_x"]
            self.item_papel["rect"].y += self.item_papel["vel_y"]
            self.item_papel["vel_y"] += self.item_papel["gravidade"]

            if self._colidiu_com_parede_item(self.item_papel["rect"]):
                self.item_papel["vel_x"] = 0
                self.item_papel["vel_y"] = 0
                self.item_papel["gravidade"] = 0
                self.item_papel["quicada"] = False
                self.item_papel["rotacao_vel"] = 0
                self.item_papel["girando"] = False

            if self.item_papel["girando"]:
                self.item_papel["angulo"] += self.item_papel["rotacao_vel"]

            if self.item_papel["rect"].bottom >= self.boss.obter_rect_alvo().bottom + 16:
                self.item_papel["rect"].bottom = self.boss.obter_rect_alvo(
                ).bottom + 16
                if self.item_papel["quicada"]:
                    self.item_papel["vel_y"] = -1.0
                    self.item_papel["vel_x"] *= 1.2
                    self.item_papel["quicada"] = False
                    self.item_papel["tempo_quica"] = pygame.time.get_ticks()
                    self.item_papel["altura_quicada"] = 2.0
                else:
                    self.item_papel["vel_y"] = 0
                    self.item_papel["vel_x"] *= 0.92
                    self.item_papel["rotacao_vel"] = 0
                    self.item_papel["girando"] = False

                if abs(self.item_papel["vel_x"]) < 0.15:
                    self.item_papel["vel_x"] = 0

            if self.item_papel["rect"].left < 0:
                self.item_papel["rect"].left = 0
                self.item_papel["vel_x"] *= -0.4
            elif self.item_papel["rect"].right > LARGURA:
                self.item_papel["rect"].right = LARGURA
                self.item_papel["vel_x"] *= -0.4

            if jogador.obter_rect().colliderect(self.item_papel["rect"]):
                if self.item_papel.get("tipo") == "chave":
                    self.chave_coletada = True
                    jogador.tem_chave = True

                self._iniciar_documento(
                    self.item_papel["documento"],
                    self.item_papel.get("texto_documento")
                )
                self.item_papel = None

        if self.documento_em_exibicao is None:
            return

        agora = pygame.time.get_ticks()
        estado = self.documento_em_exibicao

        if estado["fase"] == "in":
            elapsed = agora - estado["inicio"]
            estado["alpha"] = min(255, int((elapsed / 500) * 255))
            if elapsed >= 500:
                estado["alpha"] = 255
                estado["fase"] = "visivel"
                estado["inicio"] = agora

        elif estado["fase"] == "visivel":
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_SPACE] or teclas[pygame.K_RETURN]:
                estado["fase"] = "out"
                estado["inicio"] = agora

        elif estado["fase"] == "out":
            elapsed = agora - estado["inicio"]
            estado["alpha"] = max(0, 255 - int((elapsed / 500) * 255))
            if elapsed >= 500:
                self.documento_em_exibicao = None
                self.documento_ativo = False
                if not estado.get("avancar_boss", True):
                    return
                self._proximo_boss()

    def desenhar_documentos(self, tela):
        if self.item_papel is not None:
            sprite = self.item_papel["sprite"]
            if self.item_papel.get("tipo") == "chave":
                glow = pygame.Surface(
                    (sprite.get_width() + 18, sprite.get_height() + 18),
                    pygame.SRCALPHA
                )
                pygame.draw.ellipse(
                    glow,
                    (255, 255, 255, 55),
                    glow.get_rect().inflate(-8, -8)
                )
                glow_rect = glow.get_rect(
                    center=self.item_papel["rect"].center)
                tela.blit(glow, glow_rect)

            sprite_rot = pygame.transform.rotate(
                sprite, self.item_papel["angulo"])
            rect = sprite_rot.get_rect(center=self.item_papel["rect"].center)
            tela.blit(sprite_rot, rect)

        if self.documento_em_exibicao is None:
            return

        estado = self.documento_em_exibicao
        imagem = estado["imagem"].copy()
        imagem.set_alpha(estado["alpha"])

        rect = estado["rect"].copy()
        rect.top += int(estado["scroll"])
        tela.blit(imagem, rect)

    def _atualizar_balas(self):
        novas_balas = []
        boss_rects = [
            (boss, boss.obter_rect_alvo())
            for boss in self.bosses_ativos
        ]

        for bala in self.balas:
            bala["posicao"] += bala["direcao"] * VELOCIDADE_BALA
            bala_rect = self.sprite_bala.get_rect(
                center=bala["posicao"]
            )

            boss_hit = None
            for boss, rect in boss_rects:
                if bala_rect.colliderect(rect):
                    boss_hit = boss
                    break

            if boss_hit is not None:
                self.vida = max(0, self.vida - 1)
                self.mensagem = f"{self.dados['nome']}: {self.vida} HP"
                self.mensagem_expira = pygame.time.get_ticks() + 900
                if self.vida == 0:
                    self._limpar_ataques()
                    self._iniciar_efeito_derrota()
                    return
                continue

            pontos = [
                (bala_rect.left, bala_rect.top),
                (bala_rect.right - 1, bala_rect.top),
                (bala_rect.left, bala_rect.bottom - 1),
                (bala_rect.right - 1, bala_rect.bottom - 1)
            ]
            disparado_ms = bala.setdefault(
                "disparado_ms",
                pygame.time.get_ticks()
            )
            if (
                pygame.time.get_ticks() - disparado_ms >= 200
                and any(eh_parede(x, y) for x, y in pontos)
            ):
                continue

            if (
                bala_rect.right >= 0
                and bala_rect.left <= LARGURA
                and bala_rect.bottom >= 0
                and bala_rect.top <= ALTURA
            ):
                novas_balas.append(bala)

        self.balas = novas_balas

    def desenhar_balas(self, tela):
        for bala in self.balas:
            tela.blit(
                self.sprite_bala,
                self.sprite_bala.get_rect(center=bala["posicao"])
            )

    def obter_boss(self):
        return self.boss

    def obter_bosses(self):
        return self.bosses_visiveis

    def desenhar_interface(self, tela):
        if (
            self.boss is None
            or self.dados is None
            or self.boss5_fusao is not None
        ):
            return

        largura = 360
        altura = 16
        x = (LARGURA - largura) // 2
        y = 18

        proporcao = self.vida / self.vida_maxima if self.vida_maxima else 0

        pygame.draw.rect(tela, (25, 25, 25), (x, y, largura, altura))
        pygame.draw.rect(
            tela,
            (190, 35, 45),
            (x, y, int(largura * proporcao), altura)
        )
        pygame.draw.rect(tela, (240, 220, 190), (x, y, largura, altura), 2)

        fonte = pygame.font.Font(None, 26)
        nome = fonte.render(self.dados["nome"], True, (255, 255, 255))
        tela.blit(nome, (x, y + altura + 4))

        if pygame.time.get_ticks() < self.mensagem_expira:
            mensagem = fonte.render(self.mensagem, True, (255, 230, 160))
            tela.blit(
                mensagem,
                mensagem.get_rect(center=(LARGURA // 2, ALTURA - 34))
            )
