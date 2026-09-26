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
        "vida": 20,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Petulante e ignorante, ainda cogita ser capaz de dar continuidade à trama de seus devaneios? \nSabes que só trará mais sofrimento a ti e ao seu vassalo. \nVossa mercê não possuis o necessário para suportar tamanha desgraça.",
        "drop_papel": False
    },
    "boss2": {
        "nome": "Boss 2",
        "vida": 25,
        "dano": 1,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Petulante e ignorante, ainda cogita ser capaz de dar continuidade à trama de seus devaneios? \nSabes que só trará mais sofrimento a ti e ao seu vassalo. \nVossa mercê não possuis o necessário para suportar tamanha desgraça.",
        "drop_papel": True
    },
    "boss3": {
        "nome": "Boss 3",
        "vida": 30,
        "dano": 2,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Monstro! Tendes noção que não passas disso...\nAmiudadamente continuas a torturar sua pessoa e aquele que vos acompanha.\nContudo, não permitirei que prossigas!",
        "drop_papel": False
    },
    "boss4": {
        "nome": "Boss 4",
        "vida": 40,
        "dano": 2,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Indescritível! Indescritivel é o ódio que sinto por sua pessoa!\nJá que não foram suficientes as criaturas minhas, trarei fim a este pequeno contratempo com a mão de quem a vós delata.\nPrepare-se para experimentar o verdadeiro temor... ",
        "drop_papel": False
    },
    "boss5": {
        "nome": "Boss 5",
        "vida": 70,
        "dano": 2,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Boss 5\nO confronto cresce.",
        "drop_papel": True
    },
    "boss6": {
        "nome": "Boss 6",
        "vida": 50,
        "dano": 3,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Boss 6\nA ameaça se revela.",
        "drop_papel": True
    },
    "boss7": {
        "nome": "Boss 7",
        "vida": 60,
        "dano": 3,
        "documento": "assets/Documentos/Documento1.png",
        "texto_documento": "Boss 7\nA chave do final.",
        "drop_papel": True
    }
}


VELOCIDADE_BALA = 10
INTERVALO_DISPARO = 250


class GerenciadorBosses:

    def __init__(self, bosses, jogador):
        self.bosses = bosses
        self.jogador = jogador
        self.indice = -1
        self.boss = None
        self.bosses_ativos = []
        self.identificador = None
        self.dados = None
        self.vida = 0
        self.vida_maxima = 0
        self.finalizado = False
        self.mensagem = ""
        self.mensagem_expira = 0
        self.balas = []
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
        self.efeito_derrota = None
        self.posicao_ultimo_boss = None
        self._proximo_boss_em_execucao = False
        self.boss5_vidas = {}
        self.boss5_vivos = {}
        self.boss5_drop_fila = []

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
            self.indice += 1

            while self.indice < len(BOSS_ORDEM):
                identificador = BOSS_ORDEM[self.indice]
                boss = (
                    self.bosses.get("boss3")
                    if identificador == "boss5"
                    else self.bosses.get(identificador)
                )
                dados = BOSS_DADOS.get(identificador)

                if boss is not None and dados is not None:
                    self.identificador = identificador
                    self.boss = boss
                    self.bosses_ativos = (
                        [self.bosses["boss3"], self.bosses["boss4"]]
                        if identificador == "boss5"
                        else [boss]
                    )
                    self.dados = dados
                    for indice_ativo, boss_ativo in enumerate(self.bosses_ativos):
                        boss_ativo.animacao_entrada_ativa = ANIMACAO_ENTRADA_BOSS.get(
                            identificador,
                            True
                        )
                        boss_ativo.dano_ataque = dados["dano"]
                        boss_ativo.ia_ativa = False if identificador in (
                            "boss3", "boss4", "boss5", "boss6", "boss7"
                        ) else True
                        sprite = boss_ativo.pegar_sprite()
                        destino_y = (ALTURA - sprite.get_height()) // 2

                        if self.posicao_ultimo_boss is not None and identificador not in (
                            "boss5",
                        ):
                            boss_ativo.x = self.posicao_ultimo_boss[0]
                            if boss_ativo.animacao_entrada_ativa:
                                boss_ativo.y = -sprite.get_height() - 20
                                boss_ativo.iniciar_entrada(destino_y)
                            else:
                                boss_ativo.y = self.posicao_ultimo_boss[1]
                            self.posicao_ultimo_boss = None
                        elif identificador == "boss5":
                            offset_x = -200 if indice_ativo == 0 else 200
                            boss_ativo.x = (
                                LARGURA - sprite.get_width()) // 2 + offset_x
                            if boss_ativo.animacao_entrada_ativa:
                                boss_ativo.y = -sprite.get_height() - 20
                                boss_ativo.iniciar_entrada(destino_y)
                            else:
                                boss_ativo.y = destino_y
                            boss_ativo.ia_ativa = False
                            boss_ativo.movimento_x = 0
                            boss_ativo.movimento_y = 0
                            boss_ativo.esta_se_movendo = False
                            boss_ativo.ataques.clear()
                        else:
                            boss_ativo.x = (LARGURA - sprite.get_width()) // 2
                            if boss_ativo.animacao_entrada_ativa:
                                boss_ativo.y = -sprite.get_height() - 20
                                boss_ativo.iniciar_entrada(destino_y)
                            else:
                                boss_ativo.y = destino_y

                    if identificador == "boss5":
                        self.boss5_vidas = {
                            "boss3": BOSS_DADOS["boss3"]["vida"],
                            "boss4": BOSS_DADOS["boss4"]["vida"]
                        }
                        self.boss5_vivos = {
                            "boss3": True,
                            "boss4": True
                        }
                        self.vida = sum(self.boss5_vidas.values())
                        self.vida_maxima = self.vida
                    else:
                        self.boss5_vidas = {}
                        self.boss5_vivos = {}
                        self.vida = dados["vida"]
                        self.vida_maxima = self.vida

                    if identificador == "boss6":
                        self.boss.iniciar_animacao_boss6()
                        self.boss.configurar_padrao_ataque("boss6")
                    elif identificador == "boss7":
                        self.boss.configurar_padrao_ataque("boss6")
                    if self.indice > 0:
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

    def atualizar(self, interface):
        if not self.iniciado or self.boss is None:
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

        for boss in self.bosses_ativos:
            if self.identificador == "boss5":
                subboss = self._obter_subboss_boss5(boss)
                if subboss is not None and not self.boss5_vivos.get(subboss, False):
                    boss.ataques.clear()
                    boss.ia_ativa = False
                    boss.movimento_x = 0
                    boss.movimento_y = 0
                    boss.esta_se_movendo = False
                    continue
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
            "direcao": self.direcao_disparo.copy()
        })
        self.tempo_ultimo_disparo = agora

    def _obter_subboss_boss5(self, boss):
        for identificador, boss_ativo in zip(("boss3", "boss4"), self.bosses_ativos):
            if boss_ativo is boss:
                return identificador
        return None

    def _processar_drop_boss5(self):
        if self.item_papel is not None or self.documento_ativo:
            return

        for identificador_esperado in ("boss3", "boss4"):
            if identificador_esperado not in self.boss5_drop_fila:
                continue

            self.boss5_drop_fila.remove(identificador_esperado)
            boss_alvo = self.bosses.get(identificador_esperado)
            if boss_alvo is None:
                continue

            self._criar_item_papel(boss_alvo)
            return

    def _registrar_derrota_boss5(self, boss):
        identificador = self._obter_subboss_boss5(boss)
        if identificador is None:
            return False

        if not self.boss5_vivos.get(identificador, False):
            return False

        vida_atual = self.boss5_vidas.get(identificador, 0)
        if vida_atual <= 0:
            return False

        self.boss5_vidas[identificador] = max(0, vida_atual - 1)
        self.vida = max(0, self.vida - 1)

        if self.boss5_vidas[identificador] > 0:
            fase_num = "1" if identificador == "boss3" else "2"
            self.mensagem = (
                f"Boss 5-{fase_num}: {self.boss5_vidas[identificador]} HP"
            )
            self.mensagem_expira = pygame.time.get_ticks() + 700
            return False

        self.boss5_vivos[identificador] = False
        boss.ataques.clear()
        boss.ia_ativa = False
        boss.movimento_x = 0
        boss.movimento_y = 0
        boss.esta_se_movendo = False
        boss.frame = 0
        boss.contador_animacao = 0

        if identificador not in self.boss5_drop_fila:
            self.boss5_drop_fila.append(identificador)

        self.mensagem = f"Boss 5: {identificador.upper()} derrotado"
        self.mensagem_expira = pygame.time.get_ticks() + 1200

        self._processar_drop_boss5()
        return True

    def _iniciar_efeito_derrota(self):
        self.posicao_ultimo_boss = (self.boss.x, self.boss.y)
        self.efeito_derrota = {
            "inicio": pygame.time.get_ticks(),
            "duracao": 1600 if self.identificador == "boss6" else 1200,
            "offset_x": 0.0,
            "offset_y": 0.0,
            "sprite_final": self._obter_sprite_derrota(),
            "brilho": 1.0,
            "drop_papel": self.dados.get("drop_papel", True),
            "aplicar_brilho": self.identificador == "pbrr"
        }

    def _obter_sprite_derrota(self):
        if self.boss is None:
            return None

        for sprites in (
            getattr(self.boss, "direita", None),
            getattr(self.boss, "frente", None),
            getattr(self.boss, "esquerda", None),
            getattr(self.boss, "costas", None)
        ):
            if isinstance(sprites, list) and len(sprites) >= 3:
                return sprites[2]

        return self.boss.pegar_sprite()

    def _atualizar_efeito_derrota(self):
        agora = pygame.time.get_ticks()
        elapsed = agora - self.efeito_derrota["inicio"]
        duracao = self.efeito_derrota["duracao"]

        if elapsed >= duracao:
            boss_anterior = self.boss
            if self.efeito_derrota.get("drop_papel"):
                self._criar_item_papel(boss_anterior)
            self.efeito_derrota = None
            if self.identificador == "boss5":
                if any(self.boss5_vivos.values()):
                    return
                self._proximo_boss()
                return
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
        if self.identificador == "boss5":
            subboss = self._obter_subboss_boss5(
                boss) if boss is not None else None
            if subboss in ("boss3", "boss4"):
                return BOSS_DADOS.get(subboss, self.dados)
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

    def _iniciar_documento(self, documento, texto_documento=None):
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
            "rect": rect_documento
        }
        self.documento_ativo = True

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
                sentido = 1 if self.item_papel["vel_x"] >= 0 else -1
                self.item_papel["rect"].x = self._obter_x_parede_impacto(
                    self.item_papel["rect"],
                    sentido
                )
                self.item_papel["vel_x"] = 0

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
                self._iniciar_documento(
                    self.item_papel["documento"],
                    self.item_papel.get("texto_documento")
                )
                self.item_papel = None
                if self.identificador == "boss5":
                    self._processar_drop_boss5()

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
                if self.identificador == "boss5":
                    if any(self.boss5_vivos.values()):
                        self._processar_drop_boss5()
                        return
                    self._proximo_boss()
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

        if self.identificador == "boss5":
            boss_rects = [
                (boss, boss.obter_rect_alvo())
                for boss in self.bosses_ativos
                if self.boss5_vivos.get(self._obter_subboss_boss5(boss), False)
            ]
        else:
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
                if self.identificador == "boss5":
                    if self._registrar_derrota_boss5(boss_hit):
                        self.balas = []
                        return
                    self.vida = max(0, self.vida - 1)
                    self.mensagem = f"Boss 5: {self.vida} HP restante"
                    self.mensagem_expira = pygame.time.get_ticks() + 900
                else:
                    self.vida = max(0, self.vida - 1)
                    self.mensagem = f"{self.dados['nome']}: {self.vida} HP"
                    self.mensagem_expira = pygame.time.get_ticks() + 900
                    if self.vida == 0:
                        for boss in self.bosses_ativos:
                            boss.ataques.clear()
                        self._iniciar_efeito_derrota()
                        self.balas = []
                        return
                continue

            pontos = [
                (bala_rect.left, bala_rect.top),
                (bala_rect.right - 1, bala_rect.top),
                (bala_rect.left, bala_rect.bottom - 1),
                (bala_rect.right - 1, bala_rect.bottom - 1)
            ]
            if any(eh_parede(x, y) for x, y in pontos):
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
        return self.bosses_ativos

    def desenhar_interface(self, tela):
        if self.boss is None or self.dados is None:
            return

        largura = 360
        altura = 16
        x = (LARGURA - largura) // 2
        y = 18

        if self.identificador == "boss5":
            vida3 = self.boss5_vidas.get("boss3", 0)
            vida4 = self.boss5_vidas.get("boss4", 0)
            vida_maxima3 = BOSS_DADOS["boss3"]["vida"]
            vida_maxima4 = BOSS_DADOS["boss4"]["vida"]

            pygame.draw.rect(tela, (25, 25, 25), (x, y, largura, altura))
            pygame.draw.rect(
                tela,
                (190, 35, 45),
                (x, y, int(largura * (vida3 / max(1, vida_maxima3))), altura)
            )
            pygame.draw.rect(tela, (240, 220, 190), (x, y, largura, altura), 2)

            y2 = y + altura + 12
            pygame.draw.rect(tela, (25, 25, 25), (x, y2, largura, altura))
            pygame.draw.rect(
                tela,
                (190, 35, 45),
                (x, y2, int(largura * (vida4 / max(1, vida_maxima4))), altura)
            )
            pygame.draw.rect(tela, (240, 220, 190),
                             (x, y2, largura, altura), 2)

            fonte = pygame.font.Font(None, 26)
            nome = fonte.render(self.dados["nome"], True, (255, 255, 255))
            tela.blit(nome, (x, y + altura + 4 + altura + 12))
        else:
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
