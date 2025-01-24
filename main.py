"""
Oscar Gomme
Groupe 403
TP6 - Roche, papier, ciseaux
"""

import arcade
from random import choice
from attack_animation import AttackType, AttackAnimation
from game_state import GameState, RoundWinner
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Game(arcade.Window):
    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)
        self.player_attack_type = None
        self.computer_attack_type = None
        self.game_state = None
        self.sprite_list = None
        self.player_score = None
        self.ordi_score = None
        self.round_winner = None
        self.rock = None
        self.paper = None
        self.scissor = None
        self.player_image = None
        self.computer_image = None
        self.list_sprites = None
        self.player_made_choice = None

        self.setup()

    def setup(self):
        self.reset_attacks()
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
        self.player_image = arcade.Sprite("./assets/faceBeard.png", 0.3)
        self.player_image.center_x = 220
        self.player_image.center_y = 250
        self.computer_image = arcade.Sprite("./assets/compy.png", 1.25)
        self.computer_image.center_x = 600
        self.computer_image.center_y = 250
        self.list_sprites = arcade.SpriteList()
        self.reset_sprites()
        self.player_made_choice = False

    def reset_sprites(self):
        self.list_sprites.append(self.rock)
        self.list_sprites.append(self.paper)
        self.list_sprites.append(self.scissor)
        self.list_sprites.append(self.player_image)
        self.list_sprites.append(self.computer_image)

    def reset_attacks(self):
        self.player_attack_type = {
            AttackType.ROCK: False,
            AttackType.PAPER: False,
            AttackType.SCISSORS: False
        }
        self.computer_attack_type = {
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

        affichage = arcade.Text(f"Le pointage du joueur est {self.player_score}", 0, SCREEN_HEIGHT*0.05,
                                arcade.color.EMERALD, font_size=16, width=int(SCREEN_WIDTH/2), multiline=True,
                                align="center")
        affichage.draw()

        affichage = arcade.Text(f"Le pointage de l'ordinateur est {self.ordi_score}", SCREEN_WIDTH/2,
                                SCREEN_HEIGHT * 0.05, arcade.color.EMERALD, font_size=16, width=int(SCREEN_WIDTH/2),
                                multiline=True, align="center")
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
            elif self.round_winner == RoundWinner.ORDINATEUR:
                affichage = arcade.Text("L'ORDINATEUR A GAGNÉ LA RONDE.", 0,
                                        SCREEN_HEIGHT - 250, arcade.color.EMERALD, font_size=28, width=SCREEN_WIDTH,
                                        align="center")

            else:
                affichage = arcade.Text("C'EST UNE ÉGALITÉ.", 0,
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

        r = arcade.rect.LBWH(555, 105, 90, 90)
        arcade.draw.draw_rect_outline(r, arcade.color.AMARANTH)

    def on_update(self, delta_time):
        if self.game_state == GameState.ROUND_DONE or self.player_score == 3 or self.ordi_score == 3:
            self.list_sprites.clear()
            self.list_sprites.append(self.player_image)
            self.list_sprites.append(self.computer_image)
            if self.player_attack_type[AttackType.ROCK]:
                rock = arcade.Sprite("./assets/srock.png", 0.5)
                rock.center_x = 80
                rock.center_y = 150
                self.list_sprites.append(rock)
            elif self.player_attack_type[AttackType.PAPER]:
                paper = arcade.Sprite("./assets/spaper.png", 0.5)
                paper.center_x = 220
                paper.center_y = 150
                self.list_sprites.append(paper)
            else:
                scissors = arcade.Sprite("./assets/scissors.png", 0.5)
                scissors.center_x = 360
                scissors.center_y = 150
                self.list_sprites.append(scissors)

            if self.computer_attack_type[AttackType.ROCK]:
                computer_choice = arcade.Sprite("./assets/srock.png", 0.5)
            elif self.computer_attack_type[AttackType.PAPER]:
                computer_choice = arcade.Sprite("./assets/spaper.png", 0.5)
            else:
                computer_choice = arcade.Sprite("./assets/scissors.png", 0.5)

            computer_choice.center_x = 600
            computer_choice.center_y = 150

            self.list_sprites.append(computer_choice)

        elif self.game_state == GameState.ROUND_ACTIVE:
            if self.player_made_choice:
                self.check_winner()

            else:
                self.rock.on_update()
                self.paper.on_update()
                self.scissor.on_update()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE and (self.game_state == GameState.NOT_STARTED or self.game_state == GameState.GAME_OVER):
            self.setup()
            self.game_state = GameState.ROUND_ACTIVE

        elif symbol == arcade.key.SPACE and self.game_state == GameState.ROUND_DONE:
            self.reset_attacks()
            self.list_sprites.clear()
            self.reset_sprites()
            self.game_state = GameState.ROUND_ACTIVE

    def on_mouse_press(self, x, y, button, key_modifiers):
        if x > 400:
            return
        if self.game_state == GameState.ROUND_ACTIVE:
            if self.rock.collides_with_point((x, y)):
                self.player_attack_type[AttackType.ROCK] = True
                self.player_made_choice = True

            if self.paper.collides_with_point((x, y)):
                self.player_attack_type[AttackType.PAPER] = True
                self.player_made_choice = True

            if self.scissor.collides_with_point((x, y)):
                self.player_attack_type[AttackType.SCISSORS] = True
                self.player_made_choice = True

    def check_winner(self):
        self.computer_choice()

        if self.player_attack_type[AttackType.ROCK] and self.computer_attack_type[AttackType.PAPER]:
            self.round_winner = RoundWinner.ORDINATEUR
            self.ordi_score += 1
        elif self.player_attack_type[AttackType.ROCK] and self.computer_attack_type[AttackType.SCISSORS]:
            self.round_winner = RoundWinner.JOUEUR
            self.player_score += 1
        elif self.player_attack_type[AttackType.PAPER] and self.computer_attack_type[AttackType.ROCK]:
            self.round_winner = RoundWinner.JOUEUR
            self.player_score += 1
        elif self.player_attack_type[AttackType.PAPER] and self.computer_attack_type[AttackType.SCISSORS]:
            self.round_winner = RoundWinner.ORDINATEUR
            self.ordi_score += 1
        elif self.player_attack_type[AttackType.SCISSORS] and self.computer_attack_type[AttackType.ROCK]:
            self.round_winner = RoundWinner.ORDINATEUR
            self.ordi_score += 1
        elif self.player_attack_type[AttackType.SCISSORS] and self.computer_attack_type[AttackType.PAPER]:
            self.round_winner = RoundWinner.JOUEUR
            self.player_score += 1
        else:
            self.round_winner = RoundWinner.EGALITE

        if self.player_score == 3 or self.ordi_score == 3:
            self.game_state = GameState.GAME_OVER
        else:
            self.game_state = GameState.ROUND_DONE

        self.player_made_choice = False

    def computer_choice(self):
        self.computer_attack_type[choice([AttackType.ROCK, AttackType.PAPER, AttackType.SCISSORS])] = True


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, "Roche, Papier, Ciseaux")
    window.run()


if __name__ == "__main__":
    main()
