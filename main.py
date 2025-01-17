"""
Oscar Gomme
Groupe 403
TP6 - Roche, papier, ciseaux
"""

import arcade
from attack_animation import AttackType, AttackAnimation
from game_state import GameState, RoundWinner
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)
        self.player_attack_type = None
        self.game_state = None
        self.sprite_list = None
        self.player_score = None
        self.ordi_score = None
        self.round_winner = None
        self.rock = None
        self.paper = None
        self.scissor = None
        self.list_sprites = None

        self.setup()

    def setup(self):
        self.reset_player_attacks()
        self.game_state = GameState.NOT_STARTED
        self.sprite_list = arcade.SpriteList()
        self.player_score = 0
        self.ordi_score = 0
        self.rock = AttackAnimation(AttackType.ROCK)
        self.rock.center_x = 80
        self.rock.center_y = 150
        self.paper = AttackAnimation(AttackType.PAPER)
        self.paper.center_x = 220
        self.paper.center_y = 150
        self.scissor = AttackAnimation(AttackType.SCISSORS)
        self.scissor.center_x = 360
        self.scissor.center_y = 150
        self.list_sprites = arcade.SpriteList()
        self.list_sprites.append(self.rock)
        self.list_sprites.append(self.paper)
        self.list_sprites.append(self.scissor)

    def reset_player_attacks(self):
        self.player_attack_type = {
            AttackType.ROCK: False,
            AttackType.PAPER: False,
            AttackType.SCISSORS: False
        }

    def on_draw(self):
        self.clear(arcade.color.BLUE_YONDER)
        self.draw_text_game()
        Game.draw_rectangles()
        self.list_sprites.draw()

    def draw_text_game(self):
        affichage = arcade.Text("ROCHE, PAPIER, CISEAUX", SCREEN_WIDTH / 7, SCREEN_HEIGHT - 70,
                                arcade.color.CARROT_ORANGE, font_size=42, bold=True)
        affichage.draw()

        affichage = arcade.Text(f"Le pointage du joueur est {self.player_score}", SCREEN_WIDTH / 16, SCREEN_HEIGHT*0.05,
                                arcade.color.EMERALD, font_size=16)
        affichage.draw()

        affichage = arcade.Text(f"Le pointage de l'ordinateur est {self.ordi_score}", SCREEN_WIDTH*0.6,
                                SCREEN_HEIGHT * 0.05, arcade.color.EMERALD, font_size=16)
        affichage.draw()

        if self.game_state == GameState.NOT_STARTED:
            affichage = arcade.Text("APPUYEZ SUR 'ESPACE' POUR COMMENCER LE JEU.", SCREEN_WIDTH / 32,
                                    SCREEN_HEIGHT - 120, arcade.color.EMERALD, font_size=28)
            affichage.draw()

        elif self.game_state == GameState.ROUND_ACTIVE:
            affichage = arcade.Text("APPUYEZ SUR UNE IMAGE\nPOUR FAIRE UNE ATTAQUE.", 0,
                                    SCREEN_HEIGHT - 120, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                    multiline=True, align="center")
            affichage.draw()

        elif self.game_state == GameState.ROUND_DONE:
            if self.round_winner == RoundWinner.JOUEUR:
                affichage = arcade.Text("LE JOUEUR À GAGNÉ LA RONDE.", 0,
                                        SCREEN_HEIGHT - 250, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                        align="center")
            if self.round_winner == RoundWinner.ORDINATEUR:
                affichage = arcade.Text("L'ORDINATEUR A GAGNÉ LA RONDE.", 0,
                                        SCREEN_HEIGHT - 250, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                        align="center")

            affichage.draw()

            affichage = arcade.Text("APPUYEZ SUR 'ESPACE' POUR COMMENCER\nUNE NOUVELLE RONDE.", 0,
                                    SCREEN_HEIGHT - 120, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                    multiline=True, align="center")
            affichage.draw()

        elif self.game_state == GameState.GAME_OVER:
            if self.round_winner == RoundWinner.ORDINATEUR:
                affichage = arcade.Text("L'ORDINATEUR A GAGNÉ LA PARTIE.\nLA PARTIE EST TERMINÉ.", 0,
                                        SCREEN_HEIGHT - 120, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                        multiline=True, align="center")
            if self.round_winner == RoundWinner.JOUEUR:
                affichage = arcade.Text("LE JOUEUR A GAGNÉ LA PARTIE.\nLA PARTIE EST TERMINÉ.", 0,
                                        SCREEN_HEIGHT - 120, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                        multiline=True, align="center")
            affichage.draw()

            affichage = arcade.Text("APPUYEZ SUR 'ESPACE' POUR DÉBUTER\nUNE NOUVELLE PARTIE.", 0,
                                    SCREEN_HEIGHT - 250, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                    align="center", multiline=True)

            affichage.draw()

    @staticmethod
    def draw_rectangles():
        r = arcade.rect.LBWH(35, 105, 90, 90)
        arcade.draw.draw_rect_outline(r, arcade.color.AMARANTH)
        r = arcade.rect.LBWH(175, 105, 90, 90)
        arcade.draw.draw_rect_outline(r, arcade.color.AMARANTH)
        r = arcade.rect.LBWH(315, 105, 90, 90)
        arcade.draw.draw_rect_outline(r, arcade.color.AMARANTH)

    def on_update(self, delta_time):
        self.rock.on_update()
        self.paper.on_update()
        self.scissor.on_update()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE and self.game_state == GameState.NOT_STARTED:
            self.game_state = GameState.ROUND_ACTIVE

        elif symbol == arcade.key.SPACE and self.game_state == GameState.ROUND_DONE:
            if self.player_score == 3 or self.ordi_score == 3:
                self.game_state = GameState.GAME_OVER
            else:
                self.game_state = GameState.ROUND_ACTIVE

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.rock.collides_with_point((x, y)):
            self.reset_player_attacks()
            self.player_attack_type[AttackType.ROCK] = True
            self.game_state = GameState.ROUND_DONE

        elif self.paper.collides_with_point((x, y)):
            self.reset_player_attacks()
            self.player_attack_type[AttackType.PAPER] = True
            self.game_state = GameState.ROUND_DONE

        elif self.scissor.collides_with_point((x, y)):
            self.reset_player_attacks()
            self.player_attack_type[AttackType.SCISSORS] = True
            self.game_state = GameState.ROUND_DONE

def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "Roche, Papier, Ciseaux")
    window.run()


if __name__ == "__main__":
    main()
