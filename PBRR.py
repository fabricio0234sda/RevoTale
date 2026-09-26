import math
import random

import pygame
from config import TAMANHO_TILE
from colisao import eh_parede, pode_andar


# =========================================================
# CONFIGURAÇÕES
# =========================================================

VELOCIDADE = 6
VELOCIDADE_IA = 2
VELOCIDADE_ANIMACAO = 8
LARGURA_HITBOX = 24
ALTURA_HITBOX = 16
DESLOCAMENTO_HITBOX_X = 4
TEMPO_MOVIMENTO_ALEATORIO = 60
TEMPO_PERSEGUINDO = 120
INTERVALO_ATAQUE = 90
ALCANCE_ATAQUE = 320
VELOCIDADE_ATAQUE = 7


# =========================================================
# CLASSE PBRR (PERSONAGEM CONTROLÁVEL)
# =========================================================

class PBRR:
    """
    Classe para controlar um personagem com movimento livre,
    animações em 4 direções e colisão com o mapa.
    """

    def __init__(
        self,
        frente,
        costas,
        esquerda,
        direita,
        x,
        y
    ):
        """
        Inicializa o personagem PBRR.

        Args:
            frente: Lista de sprites para andar para frente
            costas: Lista de sprites para andar para trás
            esquerda: Lista de sprites para andar para esquerda
            direita: Lista de sprites para andar para direita
            x: Posição inicial X
            y: Posição inicial Y
        """

        # =================================================
        # SPRITES
        # =================================================

        self.frente = frente
        self.costas = costas
        self.esquerda = esquerda
        self.direita = direita

        # =================================================
        # POSIÇÃO
        # =================================================

        self.x = x
        self.y = y

        # =================================================
        # DIREÇÃO
        # =================================================

        self.direcao = "frente"
        self.direcao_anterior = "frente"

        # =================================================
        # MOVIMENTO
        # =================================================

        self.velocidade = VELOCIDADE
        self.velocidade_ia = VELOCIDADE_IA

        self.movimento_x = 0
        self.movimento_y = 0

        # =================================================
        # ANIMAÇÃO
        # =================================================

        self.frame = 0
        self.contador_animacao = 0
        self.velocidade_animacao = VELOCIDADE_ANIMACAO
        self._primeiro_update = True

        # =================================================
        # PADRÃO DE ATAQUES
        # =================================================

        self.padrao_ataque = "normal"
        self.estado_ataque_boss2 = {
            "fase": "combo_10",
            "tiros_disparados": 0,
            "proximo_tiro_ms": 0,
            "direcao_index": 0,
            "direcoes_8": [
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
                (-1, -1),
                (0, -1),
                (1, -1)
            ]
        }

        # =================================================
        # ESTADO
        # =================================================

        self.esta_se_movendo = False

        # Estado da inteligencia artificial
        self.modo_ia = "aleatorio"
        self.ia_ativa = True
        self.tempo_ia = TEMPO_MOVIMENTO_ALEATORIO
        self.direcao_aleatoria = self._sortear_direcao()

        self.sprite_ataque = pygame.image.load(
            "assets/ataques/ataque1.png"
        ).convert_alpha()
        self.sprite_ataque_2 = pygame.image.load(
            "assets/ataques/ataque2.png"
        ).convert_alpha()
        self.sprite_ataque_3 = pygame.image.load(
            "assets/ataques/ataque3.png"
        ).convert_alpha()
        self.sprite_ataque_4 = pygame.image.load(
            "assets/ataques/ataque4.png"
        ).convert_alpha()
        self.sprite_ataque_5 = pygame.image.load(
            "assets/ataques/ataque5.png"
        ).convert_alpha()
        self.sprite_ataque_5 = pygame.transform.scale(
            self.sprite_ataque_5,
            (
                self.sprite_ataque_5.get_width() * 3,
                self.sprite_ataque_5.get_height() * 3
            )
        )
        self.sprite_ataque_6 = pygame.image.load(
            "assets/ataques/ataque6.png"
        ).convert_alpha()
        self.marcataque = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/ataques/marcataque/marcaataque{i:02d}.png"
                ).convert_alpha(),
                (
                    pygame.image.load(
                        f"assets/ataques/marcataque/marcaataque{i:02d}.png"
                    ).convert_alpha().get_width() * 2,
                    pygame.image.load(
                        f"assets/ataques/marcataque/marcaataque{i:02d}.png"
                    ).convert_alpha().get_height() * 2
                )
            )
            for i in range(10)
        ]
        self.ataques = []
        self.tempo_ataque = 0
        self.animacao_boss6 = None
        self.animacao_entrada_ativa = True
        self.entrando = False
        self.entrada_origem_y = y
        self.entrada_destino_y = y
        self.entrada_inicio_ms = 0
        self.entrada_duracao_ms = 500
        self.entrada_alpha = 255

    def configurar_animacao_boss6(
        self,
        sprite_caindo,
        sprites_entrada,
        sprites_frente
    ):
        self.animacao_boss6 = {
            "fase": "caindo",
            "inicio": pygame.time.get_ticks(),
            "duracao_frame": 120,
            "sprite_caindo": sprite_caindo,
            "entrada": sprites_entrada,
            "frente": sprites_frente
        }

    def boss6_esta_em_entrada(self):
        return self.animacao_boss6 is not None and self.animacao_boss6["fase"] in (
            "caindo", "entrada"
        )

    def iniciar_animacao_boss6(self):
        if self.animacao_boss6 is not None:
            if not self.animacao_entrada_ativa:
                self.animacao_boss6["fase"] = "frente"
                self.animacao_boss6["inicio"] = pygame.time.get_ticks()
                return
            self.animacao_boss6["fase"] = "caindo"
            self.animacao_boss6["inicio"] = pygame.time.get_ticks()
            self.animacao_boss6["y_final"] = self.entrada_destino_y

    def _pegar_sprite_boss6(self):
        animacao = self.animacao_boss6
        if animacao is None:
            return self.frente[0]

        if not self.animacao_entrada_ativa:
            sprites = animacao["frente"]
            elapsed = pygame.time.get_ticks() - animacao["inicio"]
            return sprites[(elapsed // animacao["duracao_frame"]) % len(sprites)]

        fase = animacao["fase"]
        if fase == "caindo":
            return animacao["sprite_caindo"]

        if fase == "entrada":
            sprites = animacao["entrada"]
            elapsed = pygame.time.get_ticks() - animacao["inicio"]
            indice = min(len(sprites) - 1, elapsed //
                         animacao["duracao_frame"])
            return sprites[indice]

        sprites = animacao["frente"]
        elapsed = pygame.time.get_ticks() - animacao["inicio"]
        indice = (elapsed // animacao["duracao_frame"]) % len(sprites)
        return sprites[indice]

    def iniciar_entrada(self, destino_y=None):
        if not self.animacao_entrada_ativa:
            self.entrando = False
            self.entrada_alpha = 255
            if destino_y is not None:
                self.y = destino_y
            return

        if destino_y is None:
            destino_y = self.y

        self.entrada_origem_y = self.y
        self.entrada_destino_y = destino_y
        self.entrada_inicio_ms = pygame.time.get_ticks()
        self.entrada_alpha = 0
        self.entrando = True

    def obter_alpha_entrada(self):
        if not self.animacao_entrada_ativa or not self.entrando:
            return 255

        elapsed = pygame.time.get_ticks() - self.entrada_inicio_ms
        progresso = min(1.0, elapsed / max(1, self.entrada_duracao_ms))
        self.entrada_alpha = int(progresso * 255)
        return self.entrada_alpha

    def atualizar_entrada(self):
        if not self.animacao_entrada_ativa:
            self.entrando = False
            self.entrada_alpha = 255
            return

        if self.animacao_boss6 is not None:
            animacao = self.animacao_boss6
            if animacao["fase"] == "caindo":
                if self.y < self.entrada_destino_y:
                    self.y = min(self.entrada_destino_y, self.y + 12)
                if self.y >= self.entrada_destino_y:
                    animacao["fase"] = "entrada"
                    animacao["inicio"] = pygame.time.get_ticks()
                    self.entrada_alpha = 255
                return

            if animacao["fase"] == "entrada":
                sprites = animacao["entrada"]
                elapsed = pygame.time.get_ticks() - animacao["inicio"]
                if elapsed >= len(sprites) * animacao["duracao_frame"]:
                    animacao["fase"] = "frente"
                    animacao["inicio"] = pygame.time.get_ticks()
                    self.entrando = False
                    self.entrada_alpha = 255
                return

        if not self.entrando:
            return

        elapsed = pygame.time.get_ticks() - self.entrada_inicio_ms
        progresso = min(1.0, elapsed / max(1, self.entrada_duracao_ms))
        self.y = int(
            self.entrada_origem_y
            + (self.entrada_destino_y - self.entrada_origem_y) * progresso
        )
        self.entrada_alpha = int(progresso * 255)
        if progresso >= 1.0:
            self.entrando = False
            self.y = self.entrada_destino_y
            self.entrada_alpha = 255

    def esta_em_entrada(self):
        if not self.animacao_entrada_ativa:
            return False
        return self.entrando or (
            self.animacao_boss6 is not None and self.animacao_boss6["fase"] in (
                "caindo",
                "entrada"
            )
        )

    def boss6_esta_em_entrada(self):
        return self.esta_em_entrada()

    # =====================================================
    # PEGAR SPRITE ATUAL
    # =====================================================

    def pegar_sprite(self):
        """
        Retorna o sprite atual baseado na direção e frame.

        Returns:
            pygame.Surface: Imagem do sprite
        """

        if self.animacao_boss6 is not None:
            if self.animacao_entrada_ativa:
                return self._pegar_sprite_boss6()
            return self._pegar_sprite_boss6()

        # Escolher lista de sprites baseado na direção
        if self.direcao == "costas":
            sprites = self.costas
        elif self.direcao == "frente":
            sprites = self.frente
        elif self.direcao == "esquerda":
            sprites = self.esquerda
        elif self.direcao == "direita":
            sprites = self.direita
        else:
            sprites = self.frente

        # Validar índice do frame
        if self.frame >= len(sprites):
            self.frame = 0
            return sprites[0]

        return sprites[self.frame]

    # =====================================================
    # PROCESSAR ENTRADA DO JOGADOR
    # =====================================================

    def processar_entrada(self):
        """
        Processa as teclas pressionadas para definir movimento.
        Suporta setas ou WASD.
        """

        teclas = pygame.key.get_pressed()

        # Reset de movimento
        self.movimento_x = 0
        self.movimento_y = 0

        # Verificar entradas
        esquerda_pressionado = teclas[pygame.K_LEFT] or teclas[pygame.K_a]
        direita_pressionado = teclas[pygame.K_RIGHT] or teclas[pygame.K_d]
        cima_pressionado = teclas[pygame.K_UP] or teclas[pygame.K_w]
        baixo_pressionado = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        # Movimento horizontal
        if esquerda_pressionado:
            self.movimento_x = -self.velocidade
            self.direcao = "esquerda"

        elif direita_pressionado:
            self.movimento_x = self.velocidade
            self.direcao = "direita"

        # Movimento vertical
        if cima_pressionado:
            self.movimento_y = -self.velocidade
            self.direcao = "costas"

        elif baixo_pressionado:
            self.movimento_y = self.velocidade
            self.direcao = "frente"

        # Determinar se está se movendo
        self.esta_se_movendo = (
            self.movimento_x != 0 or self.movimento_y != 0
        )

    def _sortear_direcao(self):
        """Escolhe uma direcao cardinal aleatoria."""

        return random.choice(
            [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ]
        )

    def processar_ia(self, alvo):
        """Alterna entre andar aleatoriamente e perseguir o alvo."""

        if self._primeiro_update:
            self.movimento_x = 0
            self.movimento_y = 0
            self.esta_se_movendo = False
            self.frame = 0
            self.contador_animacao = 0
            self._primeiro_update = False
            return

        if self.tempo_ia <= 0:
            if self.modo_ia == "aleatorio":
                self.modo_ia = "perseguindo"
                self.tempo_ia = TEMPO_PERSEGUINDO
            else:
                self.modo_ia = "aleatorio"
                self.tempo_ia = TEMPO_MOVIMENTO_ALEATORIO
                self.direcao_aleatoria = self._sortear_direcao()

        if self.modo_ia == "aleatorio":
            direcao_x, direcao_y = self.direcao_aleatoria
            self.movimento_x = direcao_x * self.velocidade_ia
            self.movimento_y = direcao_y * self.velocidade_ia
        else:
            distancia_x = alvo.x - self.x
            distancia_y = alvo.y - self.y
            distancia = math.hypot(distancia_x, distancia_y)

            if distancia <= 40:
                self.movimento_x = 0
                self.movimento_y = 0
            else:
                self.movimento_x = distancia_x / distancia * self.velocidade_ia
                self.movimento_y = distancia_y / distancia * self.velocidade_ia

        self.tempo_ia -= 1
        self.direcao = self._obter_direcao_movimento()
        self.esta_se_movendo = (
            self.movimento_x != 0 or self.movimento_y != 0
        )

    def _obter_direcao_movimento(self):
        if abs(self.movimento_x) > abs(self.movimento_y):
            return "direita" if self.movimento_x > 0 else "esquerda"

        if self.movimento_y < 0:
            return "costas"

        return "frente"

    # =====================================================
    # APLICAR MOVIMENTO COM COLISÃO
    # =====================================================

    def aplicar_movimento(self):
        """
        Atualiza a posição do personagem com detecção de colisão.
        """

        if not self.esta_se_movendo:
            return

        # Calcular nova posição
        novo_x = self.x + self.movimento_x
        novo_y = self.y + self.movimento_y

        # Obter sprite atual para hitbox
        sprite = self.pegar_sprite()

        # Verificar colisão
        if pode_andar(
                novo_x,
                novo_y,
                sprite,
                largura_colisao=LARGURA_HITBOX,
                altura_colisao=ALTURA_HITBOX,
                deslocamento_x=DESLOCAMENTO_HITBOX_X
        ):
            self.x = novo_x
            self.y = novo_y

    def _tentar_contornar_parede(self, alvo):
        """Testa os dois lados perpendiculares ao bloqueio."""

        movimento = pygame.Vector2(self.movimento_x, self.movimento_y)
        if movimento.length_squared() == 0:
            return False

        perpendicular = pygame.Vector2(-movimento.y, movimento.x)
        perpendicular.scale_to_length(self.velocidade_ia)
        tentativas = [perpendicular, -perpendicular]
        tentativas.sort(
            key=lambda tentativa: math.hypot(
                alvo.x - (self.x + tentativa.x),
                alvo.y - (self.y + tentativa.y)
            )
        )

        sprite = self.pegar_sprite()
        for tentativa in tentativas:
            if pode_andar(
                self.x + tentativa.x,
                self.y + tentativa.y,
                sprite,
                largura_colisao=LARGURA_HITBOX,
                altura_colisao=ALTURA_HITBOX,
                deslocamento_x=DESLOCAMENTO_HITBOX_X
            ):
                self.movimento_x = tentativa.x
                self.movimento_y = tentativa.y
                return True

        return False

    def configurar_padrao_ataque(self, padrao):
        self.padrao_ataque = padrao
        if padrao == "boss2":
            self.estado_ataque_boss2 = {
                "fase": "combo_10",
                "tiros_disparados": 0,
                "proximo_tiro_ms": pygame.time.get_ticks(),
                "direcao_index": 0,
                "direcoes_8": [
                    (1, 0),
                    (1, 1),
                    (0, 1),
                    (-1, 1),
                    (-1, 0),
                    (-1, -1),
                    (0, -1),
                    (1, -1)
                ]
            }
        elif padrao == "boss3":
            self.estado_ataque_boss3 = {
                "cooldown": 0,
                "explodindo": False
            }
        elif padrao == "boss4":
            self.estado_ataque_boss4 = {
                "fase": "simetrico",
                "inicio_ms": pygame.time.get_ticks(),
                "ultimo_tiro_ms": 0,
                "ultimo_combo_ms": 0,
                "indice_combo": 0,
                "offsets_combo": [-60, -30, 0, 30, 60],
                "proximo_ataque_especial_ms": pygame.time.get_ticks() + 5000,
                "especial_ativo": False
            }
        elif padrao == "boss6":
            agora = pygame.time.get_ticks()
            self.estado_ataque_boss6 = {
                "fase": "circular",
                "inicio_ms": agora,
                "ultimo_circular_ms": agora - 200,
                "fim_circular_ms": agora + 4000,
                "proximo_grupo_ms": agora + 4000,
                "tiros_no_grupo": 0,
                "ultimo_tiro_grupo_ms": agora,
                "fim_grupo_ms": agora + 9000,
                "proxima_chuva_ms": agora
            }

    def _adicionar_ataque(
        self,
        direcao,
        tipo="normal",
        dano=1,
        sprite=None,
        sprite_seq=None
    ):
        sprite_rect = self.pegar_sprite().get_rect(
            topleft=(self.x, self.y)
        )
        direcao_norm = pygame.Vector2(direcao).normalize()
        origem = pygame.Vector2(sprite_rect.center)

        if tipo == "ataque4":
            origem = origem + direcao_norm * 60

        self.ataques.append({
            "posicao": origem,
            "direcao": direcao_norm,
            "acertou": False,
            "tipo": tipo,
            "dano": dano,
            "sprite": sprite or self.sprite_ataque,
            "sprite_seq": sprite_seq,
            "frame_index": 0,
            "inicio_animacao_ms": pygame.time.get_ticks()
        })

    def _explodir_ataque_2(self, ataque):
        origem = ataque["posicao"].copy()
        for i in range(32):
            angulo = (2 * math.pi * i) / 32
            direcao = pygame.Vector2(
                math.cos(angulo),
                math.sin(angulo)
            )
            self.ataques.append({
                "posicao": origem.copy() + direcao * 12,
                "direcao": direcao,
                "acertou": False,
                "tipo": "ataque2",
                "dano": 1,
                "sprite": self.sprite_ataque_2
            })

    def _explodir_ataque_3(self, ataque):
        origem = ataque["posicao"].copy()
        for i in range(32):
            angulo = (2 * math.pi * i) / 32
            direcao = pygame.Vector2(
                math.cos(angulo),
                math.sin(angulo)
            )
            self.ataques.append({
                "posicao": origem.copy() + direcao * 12,
                "direcao": direcao,
                "acertou": False,
                "tipo": "ataque2",
                "dano": 1,
                "sprite": self.sprite_ataque_2
            })

    def _explodir_ataque_5(self, ataque):
        origem = ataque["posicao"].copy()
        quantidade = 8 + (1 if random.random() < 0.35 else 0)
        for i in range(quantidade):
            angulo = (2 * math.pi * i) / quantidade
            direcao = pygame.Vector2(
                math.cos(angulo),
                math.sin(angulo)
            )
            self.ataques.append({
                "posicao": origem.copy(),
                "direcao": direcao,
                "acertou": False,
                "tipo": "ataque4",
                "dano": 1,
                "sprite": self.sprite_ataque_4
            })

    def _buscar_posicao_livre(self, destino, raio_tiles=6):
        destino = pygame.Vector2(destino)
        melhores = [(0, 0)]
        for raio in range(1, raio_tiles + 1):
            for dx in range(-raio, raio + 1):
                for dy in range(-raio, raio + 1):
                    if abs(dx) + abs(dy) != raio:
                        continue
                    melhores.append((dx, dy))

        for dx, dy in melhores:
            ponto = destino + \
                pygame.Vector2(dx * TAMANHO_TILE, dy * TAMANHO_TILE)
            x = int(ponto.x)
            y = int(ponto.y)
            if not eh_parede(x, y) and not eh_parede(x + 16, y + 16):
                return ponto

        return destino

    def _criar_ataque_5_no_centro(self, destino):
        destino = self._buscar_posicao_livre(destino)
        origem = pygame.Vector2(destino) + pygame.Vector2(0, -150)
        origem.y -= 150
        destino_ajustado = destino + pygame.Vector2(0, -35)
        self.ataques.append({
            "posicao": origem.copy(),
            "direcao": pygame.Vector2(0, 1),
            "acertou": False,
            "tipo": "ataque5",
            "dano": 1,
            "sprite": self.sprite_ataque_5,
            "inicio_ms": pygame.time.get_ticks(),
            "inicio": origem.copy(),
            "destino": pygame.Vector2(destino_ajustado),
            "alpha": 0
        })

    def _disparar_ataque_boss4_especial(self, alvo):
        alvo_rect = alvo.pegar_sprite().get_rect(
            topleft=(alvo.x, alvo.y)
        )
        destino = self._buscar_posicao_livre(alvo_rect.center)
        self.ataques.append({
            "posicao": destino.copy(),
            "direcao": pygame.Vector2(0, 0),
            "acertou": False,
            "tipo": "marca_boss4",
            "dano": 0,
            "sprite": self.marcataque[0],
            "sprite_seq": self.marcataque,
            "inicio_ms": pygame.time.get_ticks(),
            "alvo_posicao": destino.copy(),
            "frame_index": 0,
            "alpha": 0,
            "drop_gerado": False
        })
        self.estado_ataque_boss4["especial_ativo"] = True

    def disparar_ataque(self, alvo):
        if self.padrao_ataque == "boss2":
            self._disparar_ataque_boss2(alvo)
            return

        if self.padrao_ataque == "boss3":
            self._disparar_ataque_boss3(alvo)
            return

        if self.padrao_ataque == "boss4":
            self._disparar_ataque_boss4(alvo)
            return

        if self.padrao_ataque == "boss6":
            self._disparar_ataque_boss6(alvo)
            return

        sprite_rect = self.pegar_sprite().get_rect(
            topleft=(self.x, self.y)
        )
        alvo_rect = alvo.pegar_sprite().get_rect(
            topleft=(alvo.x, alvo.y)
        )
        distancia_x = alvo_rect.centerx - sprite_rect.centerx
        distancia_y = alvo_rect.centery - sprite_rect.centery
        distancia = math.hypot(distancia_x, distancia_y)
        if distancia > ALCANCE_ATAQUE or self.tempo_ataque > 0:
            return

        direcao = pygame.Vector2(distancia_x, distancia_y)
        if direcao.length_squared() == 0:
            return

        direcao.normalize_ip()
        origem = pygame.Vector2(sprite_rect.center)
        self.ataques.append({
            "posicao": origem,
            "direcao": direcao,
            "acertou": False,
            "tipo": "normal",
            "dano": 1,
            "sprite": self.sprite_ataque
        })
        self.tempo_ataque = INTERVALO_ATAQUE

    def _disparar_ataque_boss3(self, alvo):
        sprite_rect = self.pegar_sprite().get_rect(
            topleft=(self.x, self.y)
        )
        alvo_rect = alvo.pegar_sprite().get_rect(
            topleft=(alvo.x, alvo.y)
        )
        distancia_x = alvo_rect.centerx - sprite_rect.centerx
        distancia_y = alvo_rect.centery - sprite_rect.centery
        distancia = math.hypot(distancia_x, distancia_y)
        if distancia > ALCANCE_ATAQUE or self.tempo_ataque > 0:
            return

        direcao = pygame.Vector2(distancia_x, distancia_y)
        if direcao.length_squared() == 0:
            return

        direcao.normalize_ip()
        origem = pygame.Vector2(sprite_rect.center)
        self.ataques.append({
            "posicao": origem,
            "direcao": direcao,
            "acertou": False,
            "tipo": "ataque3",
            "dano": 1,
            "sprite": self.sprite_ataque_3
        })
        self.tempo_ataque = INTERVALO_ATAQUE

    def _disparar_ataque_boss4(self, alvo):
        agora = pygame.time.get_ticks()
        estado = self.estado_ataque_boss4

        if estado.get("especial_ativo"):
            return

        if agora >= estado.get("proximo_ataque_especial_ms", agora + 5000):
            self._disparar_ataque_boss4_especial(alvo)
            estado["proximo_ataque_especial_ms"] = agora + 5000
            return

        if estado["fase"] == "simetrico":
            if agora - estado["inicio_ms"] >= 10000:
                estado["fase"] = "combo_jogador"
                estado["ultimo_combo_ms"] = agora
                estado["indice_combo"] = 0
                return

            if agora - estado["ultimo_tiro_ms"] < 200:
                return

            sprite_rect = self.pegar_sprite().get_rect(
                topleft=(self.x, self.y)
            )
            alvo_rect = alvo.pegar_sprite().get_rect(
                topleft=(alvo.x, alvo.y)
            )
            dx = alvo_rect.centerx - sprite_rect.centerx
            dy = alvo_rect.centery - sprite_rect.centery
            base = pygame.Vector2(dx, dy)
            if base.length_squared() == 0:
                return
            base.normalize_ip()

            angulo_base = math.atan2(base.y, base.x)
            for offset in (-math.radians(35), math.radians(35)):
                angulo = angulo_base + offset
                direcao = pygame.Vector2(math.cos(angulo), math.sin(angulo))
                self._adicionar_ataque(
                    direcao,
                    tipo="ataque4",
                    dano=1,
                    sprite=self.sprite_ataque_4,
                    sprite_seq=self.sprite_ataque_4_seq
                )

            estado["ultimo_tiro_ms"] = agora
            return

        if estado["fase"] == "combo_jogador":
            if agora - estado["ultimo_combo_ms"] < 500:
                return

            if estado["indice_combo"] >= len(estado["offsets_combo"]):
                estado["fase"] = "simetrico"
                estado["inicio_ms"] = agora
                estado["ultimo_tiro_ms"] = 0
                estado["indice_combo"] = 0
                return

            sprite_rect = self.pegar_sprite().get_rect(
                topleft=(self.x, self.y)
            )
            alvo_rect = alvo.pegar_sprite().get_rect(
                topleft=(alvo.x, alvo.y)
            )
            dx = alvo_rect.centerx - sprite_rect.centerx
            dy = alvo_rect.centery - sprite_rect.centery
            base = pygame.Vector2(dx, dy)
            if base.length_squared() == 0:
                return
            base.normalize_ip()

            angulo_base = math.atan2(base.y, base.x)
            offset = math.radians(
                estado["offsets_combo"][estado["indice_combo"]])
            angulo = angulo_base + offset
            direcao = pygame.Vector2(math.cos(angulo), math.sin(angulo))
            self._adicionar_ataque(
                direcao,
                tipo="ataque4",
                dano=1,
                sprite=self.sprite_ataque_4,
                sprite_seq=self.sprite_ataque_4_seq
            )
            estado["indice_combo"] += 1
            estado["ultimo_combo_ms"] = agora

    def _direcao_para_alvo(self, alvo):
        origem = self.pegar_sprite().get_rect(
            topleft=(self.x, self.y)
        ).center
        destino = alvo.obter_rect_dano().center
        direcao = pygame.Vector2(destino) - pygame.Vector2(origem)
        if direcao.length_squared() == 0:
            return pygame.Vector2(0, 1)
        return direcao.normalize()

    def _criar_ataque6_chuva(self):
        largura = self.pegar_sprite().get_width()
        x = random.randint(0, max(0, 640 - largura))
        inicio = pygame.Vector2(x, -self.sprite_ataque_6.get_height())
        destino = pygame.Vector2(x, 640 + self.sprite_ataque_6.get_height())
        self.ataques.append({
            "posicao": inicio.copy(),
            "inicio": inicio,
            "destino": destino,
            "inicio_ms": pygame.time.get_ticks(),
            "duracao_ms": 4000,
            "acertou": False,
            "tipo": "ataque6_chuva",
            "dano": 1,
            "sprite": self.sprite_ataque_6
        })

    def _disparar_ataque_boss6(self, alvo):
        agora = pygame.time.get_ticks()
        estado = self.estado_ataque_boss6

        if agora >= estado["proxima_chuva_ms"]:
            for _ in range(3):
                self._criar_ataque6_chuva()
            estado["proxima_chuva_ms"] = agora + random.randint(200, 300)

        if estado["fase"] == "circular":
            if agora >= estado["fim_circular_ms"]:
                estado["fase"] = "grupos"
                estado["proximo_grupo_ms"] = agora
                estado["tiros_no_grupo"] = 0
                return
            if agora - estado["ultimo_circular_ms"] < 200:
                return

            origem = self.pegar_sprite().get_rect(
                topleft=(self.x, self.y)
            ).center
            alvo_rect = alvo.pegar_sprite().get_rect(topleft=(alvo.x, alvo.y))
            base = pygame.Vector2(
                alvo_rect.centerx - origem[0],
                alvo_rect.centery - origem[1]
            )
            angulo_central = math.atan2(base.y, base.x)
            for indice in range(12):
                angulo = angulo_central + (
                    (2 * math.pi * indice) / 12 - math.pi
                )
                self.ataques.append({
                    "posicao": pygame.Vector2(origem),
                    "direcao": pygame.Vector2(
                        math.cos(angulo), math.sin(angulo)
                    ),
                    "acertou": False,
                    "tipo": "ataque6",
                    "dano": 1,
                    "sprite": self.sprite_ataque_6
                })
            estado["ultimo_circular_ms"] = agora
            return

        if agora >= estado["fim_grupo_ms"]:
            estado["fase"] = "circular"
            estado["inicio_ms"] = agora
            estado["fim_circular_ms"] = agora + 4000
            estado["ultimo_circular_ms"] = agora - 200
            return

        if agora < estado["proximo_grupo_ms"]:
            return

        self._adicionar_ataque(
            self._direcao_para_alvo(alvo),
            tipo="ataque6",
            dano=1,
            sprite=self.sprite_ataque_6
        )
        estado["tiros_no_grupo"] += 1
        if estado["tiros_no_grupo"] >= 3:
            estado["tiros_no_grupo"] = 0
            estado["proximo_grupo_ms"] = agora + 500
        else:
            estado["proximo_grupo_ms"] = agora + 200

    def _disparar_ataque_boss2(self, alvo):
        agora = pygame.time.get_ticks()
        estado = self.estado_ataque_boss2

        if estado["fase"] == "combo_10":
            if agora < estado["proximo_tiro_ms"]:
                return

            sprite_rect = self.pegar_sprite().get_rect(
                topleft=(self.x, self.y)
            )
            alvo_rect = alvo.pegar_sprite().get_rect(
                topleft=(alvo.x, alvo.y)
            )
            distancia_x = alvo_rect.centerx - sprite_rect.centerx
            distancia_y = alvo_rect.centery - sprite_rect.centery
            direcao = pygame.Vector2(distancia_x, distancia_y)
            if direcao.length_squared() == 0:
                return
            direcao.normalize_ip()
            origem = pygame.Vector2(sprite_rect.center)
            self.ataques.append({
                "posicao": origem,
                "direcao": direcao,
                "acertou": False
            })

            estado["tiros_disparados"] += 1
            if estado["tiros_disparados"] >= 10:
                estado["fase"] = "pausa"
                estado["proximo_tiro_ms"] = agora + 1200
            else:
                estado["proximo_tiro_ms"] = agora + 500
            return

        if estado["fase"] == "pausa":
            if agora < estado["proximo_tiro_ms"]:
                return
            estado["fase"] = "direcional"
            estado["direcao_index"] = 0
            estado["proximo_tiro_ms"] = agora
            return

        if estado["fase"] == "direcional":
            if agora < estado["proximo_tiro_ms"]:
                return

            for direcao_tuple in estado["direcoes_8"]:
                direcao = pygame.Vector2(direcao_tuple)
                direcao.normalize_ip()
                self._adicionar_ataque(direcao)

            estado["fase"] = "combo_10"
            estado["tiros_disparados"] = 0
            estado["direcao_index"] = 0
            estado["proximo_tiro_ms"] = agora + 1200
            return

    def atualizar_ataques(self, jogador, interface):
        if self.tempo_ataque > 0:
            self.tempo_ataque -= 1

        jogador_rect = jogador.obter_rect_dano()
        novos_ataques = []
        for ataque in self.ataques:
            tipo = ataque.get("tipo")

            if tipo == "marca_boss4":
                agora = pygame.time.get_ticks()
                tempo = agora - ataque["inicio_ms"]

                if tempo <= 500:
                    indice = int((tempo / 500) * 5)
                    alpha = int((tempo / 500) * 255)
                elif tempo <= 1500:
                    indice = int(5 + ((tempo - 500) / 1000) * 4)
                    alpha = int(255 * (1 - ((tempo - 500) / 1000)))
                    if tempo >= 1000 and not ataque.get("drop_gerado"):
                        self._criar_ataque_5_no_centro(ataque["alvo_posicao"])
                        ataque["drop_gerado"] = True
                else:
                    self.estado_ataque_boss4["especial_ativo"] = False
                    continue

                ataque["frame_index"] = max(0, min(9, indice))
                ataque["alpha"] = max(0, min(255, alpha))
                novos_ataques.append(ataque)
                continue

            if tipo == "ataque5":
                agora = pygame.time.get_ticks()
                progresso = min(1.0, (agora - ataque["inicio_ms"]) / 500)
                ataque["posicao"] = ataque["inicio"].lerp(
                    ataque["destino"],
                    progresso
                )
                ataque["alpha"] = int(progresso * 255)

                if progresso >= 1.0:
                    ponto_impacto = pygame.Vector2(ataque["destino"])
                    dist = jogador_rect.centerx - ponto_impacto.x
                    dist_y = jogador_rect.centery - ponto_impacto.y
                    if abs(dist) <= 10 and abs(dist_y) <= 10:
                        if not ataque["acertou"]:
                            interface.receber_dano(
                                ataque.get("dano", getattr(
                                    self, "dano_ataque", 1)),
                                jogador,
                                ataque["direcao"],
                                ataque["direcao"] * VELOCIDADE_ATAQUE
                            )
                        ataque["acertou"] = True
                    self._explodir_ataque_5(ataque)
                    continue

                sprite_ataque = ataque.get("sprite", self.sprite_ataque_5)
                ataque_rect = self._retangulo_do_sprite(
                    sprite_ataque,
                    ataque["posicao"]
                )
                ponto_impacto = pygame.Vector2(ataque["destino"])
                dist = pygame.Vector2(
                    jogador_rect.centerx, jogador_rect.centery) - ponto_impacto
                if dist.length() <= 10 and not ataque["acertou"]:
                    interface.receber_dano(
                        ataque.get("dano", getattr(self, "dano_ataque", 1)),
                        jogador,
                        ataque["direcao"],
                        ataque["direcao"] * VELOCIDADE_ATAQUE
                    )
                    ataque["acertou"] = True

                novos_ataques.append(ataque)
                continue

            if tipo == "ataque6_chuva":
                agora = pygame.time.get_ticks()
                progresso = min(
                    1.0,
                    (agora - ataque["inicio_ms"]) / ataque["duracao_ms"]
                )
                ataque["posicao"] = ataque["inicio"].lerp(
                    ataque["destino"], progresso
                )
                ataque_rect = self._retangulo_do_sprite(
                    ataque["sprite"],
                    ataque["posicao"]
                )
                if ataque_rect.colliderect(jogador_rect):
                    if not ataque["acertou"]:
                        interface.receber_dano(
                            ataque.get("dano", getattr(
                                self, "dano_ataque", 1)),
                            jogador,
                            pygame.Vector2(0, 1),
                            pygame.Vector2(0, 1) * VELOCIDADE_ATAQUE
                        )
                    ataque["acertou"] = True
                    continue
                if progresso < 1.0:
                    novos_ataques.append(ataque)
                continue

            ataque["posicao"] += ataque["direcao"] * VELOCIDADE_ATAQUE
            posicao = ataque["posicao"]
            sprite_ataque = ataque.get("sprite", self.sprite_ataque)
            ataque_rect = self._retangulo_do_sprite(sprite_ataque, posicao)

            if ataque_rect.colliderect(jogador_rect):
                if not ataque["acertou"]:
                    interface.receber_dano(
                        ataque.get("dano", getattr(self, "dano_ataque", 1)),
                        jogador,
                        ataque["direcao"],
                        ataque["direcao"] * VELOCIDADE_ATAQUE
                    )
                continue

            pontos_ataque = [
                (ataque_rect.left, ataque_rect.top),
                (ataque_rect.right - 1, ataque_rect.top),
                (ataque_rect.left, ataque_rect.bottom - 1),
                (ataque_rect.right - 1, ataque_rect.bottom - 1)
            ]
            if any(eh_parede(x, y) for x, y in pontos_ataque):
                if ataque.get("tipo") == "ataque3":
                    self._explodir_ataque_3(ataque)
                # os projéteis "ataque2" gerados pela explosão não podem
                # explodir de novo ao bater na parede, senão gera cascata
                # infinita e crasha o jogo.
                continue

            if ataque_rect.bottom >= 0 and ataque_rect.top <= 640:
                novos_ataques.append(ataque)

        self.ataques = novos_ataques

    def desenhar_ataques(self, tela):
        for ataque in self.ataques:
            tipo = ataque.get("tipo")

            if tipo == "marca_boss4":
                indice = int(ataque.get("frame_index", 0))
                sprite_ataque = ataque["sprite_seq"][indice]
                sprite = sprite_ataque.copy()
                sprite.set_alpha(ataque.get("alpha", 255))
                tela.blit(
                    sprite,
                    sprite.get_rect(center=ataque["posicao"])
                )
                continue

            if tipo == "ataque5":
                sprite_ataque = ataque.get("sprite", self.sprite_ataque_5)
                sprite = sprite_ataque.copy()
                sprite.set_alpha(ataque.get("alpha", 255))
                tela.blit(
                    sprite,
                    sprite.get_rect(center=ataque["posicao"])
                )
                continue

            if tipo == "ataque6_chuva":
                sprite_ataque = ataque.get("sprite", self.sprite_ataque_6)
                tela.blit(
                    sprite_ataque,
                    sprite_ataque.get_rect(center=ataque["posicao"])
                )
                continue

            if ataque.get("tipo") == "ataque4" and ataque.get("sprite_seq"):
                seq = ataque["sprite_seq"]
                frame = int((pygame.time.get_ticks() -
                            ataque.get("inicio_animacao_ms", 0)) / 80) % len(seq)
                sprite_ataque = seq[frame]
                tela.blit(
                    sprite_ataque,
                    sprite_ataque.get_rect(center=ataque["posicao"])
                )
                continue

            sprite_ataque = ataque.get("sprite", self.sprite_ataque)
            tela.blit(
                sprite_ataque,
                sprite_ataque.get_rect(center=ataque["posicao"])
            )

    # =====================================================
    # ATUALIZAR ANIMAÇÃO
    # =====================================================

    def atualizar_animacao(self):
        """
        Atualiza o frame da animação baseado no movimento.
        """

        # Se não está se movendo, volta ao frame 0
        if not self.esta_se_movendo:
            self.frame = 0
            self.contador_animacao = 0
            return

        # Incrementar contador
        self.contador_animacao += 1

        # Mudar frame quando atinge velocidade de animação
        if self.contador_animacao >= self.velocidade_animacao:
            self.contador_animacao = 0
            self.frame += 1

            # Reset do frame baseado no número de sprites da direção
            sprites = self._pegar_sprites_direcao()
            if self.frame >= len(sprites):
                self.frame = 0

    # =====================================================
    # AUXILIAR: PEGAR SPRITES DA DIREÇÃO ATUAL
    # =====================================================

    def _pegar_sprites_direcao(self):
        """
        Retorna a lista de sprites da direção atual.

        Returns:
            list: Lista de sprites
        """

        if self.direcao == "costas":
            return self.costas
        elif self.direcao == "frente":
            return self.frente
        elif self.direcao == "esquerda":
            return self.esquerda
        elif self.direcao == "direita":
            return self.direita
        else:
            return self.frente

    # =====================================================
    # ATUALIZAR (CHAMAR A CADA FRAME)
    # =====================================================

    def atualizar(self, alvo=None, interface=None):
        """
        Atualiza o personagem (entrada, movimento e animação).
        Deve ser chamado a cada frame do jogo.
        """

        if self._primeiro_update:
            self.frame = 0
            self.contador_animacao = 0
            self.movimento_x = 0
            self.movimento_y = 0
            self.esta_se_movendo = False
            self._primeiro_update = False
            return

        if alvo is None:
            self.processar_entrada()
        elif self.ia_ativa:
            self.processar_ia(alvo)
        else:
            self.movimento_x = 0
            self.movimento_y = 0
            self.esta_se_movendo = False
            self.frame = 0
            self.contador_animacao = 0
        if alvo is not None:
            if not pode_andar(
                self.x + self.movimento_x,
                self.y + self.movimento_y,
                self.pegar_sprite(),
                largura_colisao=LARGURA_HITBOX,
                altura_colisao=ALTURA_HITBOX,
                deslocamento_x=DESLOCAMENTO_HITBOX_X
            ):
                self._tentar_contornar_parede(alvo)
        self.aplicar_movimento()
        if alvo is not None and interface is not None:
            self.disparar_ataque(alvo)
            self.atualizar_ataques(alvo, interface)
        self.atualizar_animacao()

    # =====================================================
    # DESENHAR
    # =====================================================

    def desenhar(self, tela):
        """
        Desenha o personagem na tela.

        Args:
            tela: pygame.Surface para desenhar
        """

        sprite = self.pegar_sprite().copy()
        alpha = self.obter_alpha_entrada()
        if alpha < 255:
            sprite.set_alpha(alpha)
        tela.blit(sprite, (self.x, self.y))

    # =====================================================
    # OBTER RECT (HITBOX)
    # =====================================================

    def obter_rect(self):
        """
        Retorna o retângulo (hitbox) do personagem.

        Returns:
            pygame.Rect: Hitbox de colisão na base do sprite
        """

        sprite = self.pegar_sprite()
        sprite_rect = sprite.get_rect(topleft=(self.x, self.y))
        hitbox = pygame.Rect(
            0,
            0,
            LARGURA_HITBOX,
            ALTURA_HITBOX
        )
        hitbox.midbottom = (
            sprite_rect.centerx + DESLOCAMENTO_HITBOX_X,
            sprite_rect.bottom
        )
        return hitbox

    def _retangulo_do_sprite(self, sprite, centro):
        if sprite is None:
            return pygame.Rect(0, 0, 0, 0)

        rect = sprite.get_bounding_rect().copy()
        rect.center = centro
        return rect

    def obter_rect_alvo(self):
        """Retorna a área visível do sprite para ataques do jogador."""

        sprite = self.pegar_sprite()
        rect = sprite.get_bounding_rect().copy()
        rect.topleft = (
            self.x + rect.left,
            self.y + rect.top
        )
        return rect
