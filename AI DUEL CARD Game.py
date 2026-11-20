import pygame
import random
import math
import sys
from collections import deque
pygame.init()

# CONFIG size

WIDTH = 1400
HEIGHT = 900
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(&quot;AI Card Duel - The Family&quot;)
CLOCK = pygame.time.Clock()
# COLORS
TABLE_BURGUNDY = (128, 0, 32)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 40, 40)
GOLD = (230, 180, 40)
LIGHT_GOLD = (255, 215, 80)
BLUE = (80, 140, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (70, 70, 70)
SHADOW = (0, 0, 0, 60)
# FONTS
TITLE_FONT = pygame.font.SysFont(&quot;georgia,timesnewroman,serif&quot;, 72,
bold=True)
TAGLINE_FONT = pygame.font.SysFont(&quot;georgia,timesnewroman,serif&quot;, 26,
italic=True)
BIG_FONT = pygame.font.SysFont(&quot;arial&quot;, 42, bold=True)
MEDIUM_FONT = pygame.font.SysFont(&quot;arial&quot;, 30)
SMALL_FONT = pygame.font.SysFont(&quot;arial&quot;, 22)
# MAFIA ATMOSPHERE (vignette + gold frame)

def build_vignette():
surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
depth = 170
for i in range(depth):
alpha = int(150 * (1 - i / depth) ** 2)
pygame.draw.rect(
surf,
(0, 0, 0, alpha),
(i, i, WIDTH - 2 * i, HEIGHT - 2 * i),
1
)
return surf
VIGNETTE = build_vignette()
def draw_table_frame(screen):
screen.blit(VIGNETTE, (0, 0))
pygame.draw.rect(
screen,
GOLD,
(8, 8, WIDTH - 16, HEIGHT - 16),
3,
border_radius=10
)
pygame.draw.rect(
screen,
GOLD,
(15, 15, WIDTH - 30, HEIGHT - 30),
1,
border_radius=6
)
# CARD SETTINGS
CARD_WIDTH = 120
CARD_HEIGHT = 170
SUITS = [&quot;♠&quot;, &quot;♥&quot;, &quot;♦&quot;, &quot;♣&quot;]
VALUES = [
&quot;2&quot;, &quot;3&quot;, &quot;4&quot;, &quot;5&quot;, &quot;6&quot;,
&quot;7&quot;, &quot;8&quot;, &quot;9&quot;, &quot;10&quot;,
&quot;J&quot;, &quot;Q&quot;, &quot;K&quot;, &quot;A&quot;
]
CARD_VALUE_MAP = {
&quot;2&quot;: 2,
&quot;3&quot;: 3,
&quot;4&quot;: 4,
&quot;5&quot;: 5,
&quot;6&quot;: 6,
&quot;7&quot;: 7,
&quot;8&quot;: 8,
&quot;9&quot;: 9,

&quot;10&quot;: 10,
&quot;J&quot;: 11,
&quot;Q&quot;: 12,
&quot;K&quot;: 13,
&quot;A&quot;: 14
}
# CARD CLASS
class Card:
def __init__(self, suit, rank):
self.suit = suit
self.rank = rank
self.value = CARD_VALUE_MAP[rank]
def is_red(self):
return self.suit in [&quot;♥&quot;, &quot;♦&quot;]
def draw(
self,
surface,
x,
y,
hovered=False
):
scale = 1.08 if hovered else 1.0
w = int(CARD_WIDTH * scale)
h = int(CARD_HEIGHT * scale)
shadow_rect = pygame.Rect(
x + 6,
y + 6,
w,
h
)
pygame.draw.rect(
surface,
(30, 30, 30),
shadow_rect,
border_radius=12
)
card_rect = pygame.Rect(
x,
y,
w,
h
)
pygame.draw.rect(
surface,
WHITE,
card_rect,
border_radius=12

)
pygame.draw.rect(
surface,
BLACK,
card_rect,
2,
border_radius=12
)
color = RED if self.is_red() else BLACK
rank_text = MEDIUM_FONT.render(
self.rank,
True,
color
)
suit_text = BIG_FONT.render(
self.suit,
True,
color
)
surface.blit(
rank_text,
(x + 10, y + 8)
)
surface.blit(
suit_text,
(
x + w // 2 - suit_text.get_width() // 2,
y + h // 2 - suit_text.get_height() // 2
)
)
def draw_back(
self,
surface,
x,
y
):
rect = pygame.Rect(
x,
y,
CARD_WIDTH,
CARD_HEIGHT
)
pygame.draw.rect(
surface,
(25, 25, 25),
rect,
border_radius=12
)

pygame.draw.rect(
surface,
GOLD,
rect,
3,
border_radius=12
)
inner = rect.inflate(-22, -22)
pygame.draw.rect(
surface,
GOLD,
inner,
1,
border_radius=8
)
cx, cy = rect.center
pygame.draw.polygon(
surface,
GOLD,
[
(cx, cy - 34),
(cx + 24, cy),
(cx, cy + 34),
(cx - 24, cy)
],
2
)
pygame.draw.polygon(
surface,
(120, 0, 32),
[
(cx, cy - 18),
(cx + 13, cy),
(cx, cy + 18),
(cx - 13, cy)
]
)
# DECK

class Deck:
def __init__(self):
self.cards = []
for suit in SUITS:
for rank in VALUES:
self.cards.append(

Card(
suit,
rank
)
)
random.shuffle(self.cards)
def deal(self, count):
hand = []
for _ in range(count):
if self.cards:
hand.append(
self.cards.pop()
)
return hand
# BUTTON
class Button:
def __init__(
self,
x,
y,
w,
h,
text
):
self.rect = pygame.Rect(
x,
y,
w,
h
)
self.text = text
def draw(self, surface):
mouse = pygame.mouse.get_pos()
hover = self.rect.collidepoint(mouse)
color = LIGHT_GOLD if hover else GOLD
pygame.draw.rect(
surface,
color,
self.rect,
border_radius=14
)
pygame.draw.rect(
surface,
BLACK,

self.rect,
2,
border_radius=14
)
txt = MEDIUM_FONT.render(
self.text,
True,
BLACK
)
surface.blit(
txt,
(
self.rect.centerx -
txt.get_width() // 2,
self.rect.centery -
txt.get_height() // 2
)
)
def clicked(self, event):
return (
event.type == pygame.MOUSEBUTTONDOWN
and event.button == 1
and self.rect.collidepoint(event.pos)
)
# MENU
class MainMenu:
def __init__(self):
self.easy_btn = Button(
WIDTH // 2 - 180,
300,
360,
70,
&quot;ASSOCIATE (EASY)&quot;
)
self.medium_btn = Button(
WIDTH // 2 - 180,
400,
360,
70,
&quot;CAPO (MEDIUM)&quot;
)
self.hard_btn = Button(
WIDTH // 2 - 180,
500,
360,
70,

&quot;DON (HARD)&quot;
)
self.quit_btn = Button(
WIDTH // 2 - 180,
620,
360,
70,
&quot;WALK AWAY&quot;
)
def draw(self, screen):
screen.fill(TABLE_BURGUNDY)
draw_table_frame(screen)
title = TITLE_FONT.render(
&quot;AI CARD DUEL&quot;,
True,
GOLD
)
screen.blit(
title,
(
WIDTH // 2 -
title.get_width() // 2,
120
)
)
sub = TAGLINE_FONT.render(
&quot;A game of honor, respect and bluffing&quot;,
True,
LIGHT_GOLD
)
screen.blit(
sub,
(WIDTH // 2 - sub.get_width() // 2, 215)
)
self.easy_btn.draw(screen)
self.medium_btn.draw(screen)
self.hard_btn.draw(screen)
self.quit_btn.draw(screen)
tip = SMALL_FONT.render(
&quot;Tip: press Ctrl+H during a game to ask the Consigliere&quot;,
True,
LIGHT_GOLD
)
screen.blit(
tip,
(WIDTH // 2 - tip.get_width() // 2, HEIGHT - 70)
)

# GAME STATE
class GameState:
def __init__(self, difficulty):
self.difficulty = difficulty
self.deck = Deck()
self.player_hand = self.deck.deal(5)
self.ai_hand = self.deck.deal(5)
self.player_score = 0
self.ai_score = 0
self.round_number = 1
self.selected_card = None
self.ai_selected = None
self.reveal_phase = False
self.game_over = False
self.show_hint = False
self.hints_used = 0
self.played_cards = []
# GAMEPLAY UI
class GameplayUI:
def __init__(self):
self.next_button = Button(
WIDTH // 2 - 120,
HEIGHT - 120,
240,
60,
&quot;NEXT ROUND&quot;
)
def draw_background(self, screen):
screen.fill(TABLE_BURGUNDY)
draw_table_frame(screen)
# Decorative felt lines
pygame.draw.line(
screen,
(150, 20, 50),
(0, 120),
(WIDTH, 120),
2
)
pygame.draw.line(
screen,
(150, 20, 50),
(0, HEIGHT - 180),
(WIDTH, HEIGHT - 180),
2
)
def draw_scoreboard(self, screen, game):

player_title = BIG_FONT.render(
&quot;YOU&quot;,
True,
WHITE
)
ai_title = BIG_FONT.render(
&quot;THE DON&quot;,
True,
WHITE
)
player_score = BIG_FONT.render(
str(game.player_score),
True,
GOLD
)
ai_score = BIG_FONT.render(
str(game.ai_score),
True,
GOLD
)
screen.blit(player_title, (60, 20))
screen.blit(
player_score,
(60 + player_title.get_width() // 2 - player_score.get_width() //
2, 65)
)
screen.blit(ai_title, (WIDTH - ai_title.get_width() - 60, 20))
screen.blit(
ai_score,
(WIDTH - 60 - ai_title.get_width() // 2 - ai_score.get_width() //
2, 65)
)
def draw_round_tracker(self, screen, game):
text = MEDIUM_FONT.render(
f&quot;Round {min(game.round_number, 5)}/5&quot;,
True,
WHITE
)
screen.blit(
text,
(
WIDTH // 2 - text.get_width() // 2,
20
)
)
start_x = WIDTH // 2 - 70
for i in range(5):
color = GOLD if i &lt; game.round_number - 1 else DARK_GRAY

pygame.draw.circle(
screen,
color,
(
start_x + i * 35,
80
),
10
)
def draw_ai_area(self, screen, game):
title = MEDIUM_FONT.render(
&quot;THE DON&#39;S HAND&quot;,
True,
WHITE
)
screen.blit(
title,
(
WIDTH // 2 -
title.get_width() // 2,
140
)
)
spacing = 140
start_x = (
WIDTH // 2
- (len(game.ai_hand) * spacing) // 2
)
y = 180
for i, card in enumerate(game.ai_hand):
x = start_x + i * spacing
if game.reveal_phase:
if card == game.ai_selected:
card.draw(screen, x, y)
else:
card.draw_back(screen, x, y)
else:
card.draw_back(screen, x, y)
def draw_center_area(self, screen, game):
center_y = HEIGHT // 2 - 40
if game.selected_card:
label = MEDIUM_FONT.render(
&quot;You Played&quot;,
True,
WHITE
)
screen.blit(
label,
(

WIDTH // 2 - 250,
center_y - 40
)
)
game.selected_card.draw(
screen,
WIDTH // 2 - 320,
center_y
)
if game.ai_selected:
label = MEDIUM_FONT.render(
&quot;The Don Played&quot;,
True,
WHITE
)
screen.blit(
label,
(
WIDTH // 2 + 130,
center_y - 40
)
)
game.ai_selected.draw(
screen,
WIDTH // 2 + 120,
center_y
)
if game.reveal_phase:
if game.selected_card and game.ai_selected:
if game.selected_card.value &gt; game.ai_selected.value:
result = &quot;YOU TAKE THE HAND&quot;
color = GOLD
elif game.selected_card.value &lt; game.ai_selected.value:
result = &quot;THE DON TAKES IT&quot;
color = (255, 120, 120)
else:
result = &quot;A STANDOFF&quot;
color = WHITE
text = BIG_FONT.render(
result,
True,
color
)
screen.blit(
text,
(
WIDTH // 2 -
text.get_width() // 2,
center_y + 172

)
)
def draw_player_hand(self, screen, game):
title = MEDIUM_FONT.render(
&quot;YOUR HAND&quot;,
True,
WHITE
)
screen.blit(
title,
(
WIDTH // 2 -
title.get_width() // 2,
HEIGHT - 272
)
)
mouse = pygame.mouse.get_pos()
spacing = 140
start_x = (
WIDTH // 2
- (len(game.player_hand) * spacing) // 2
)
y = HEIGHT - 240
hovered_card = None
hint = (
get_hint(game)
if game.show_hint and not game.reveal_phase
else None
)
for i, card in enumerate(game.player_hand):
x = start_x + i * spacing
rect = pygame.Rect(
x,
y,
CARD_WIDTH,
CARD_HEIGHT
)
if rect.collidepoint(mouse):
hovered_card = card
for i, card in enumerate(game.player_hand):
x = start_x + i * spacing
hover = card == hovered_card
draw_y = y - 15 if hover else y
card.draw(
screen,
x,
draw_y,
hover
)

if hint and card == hint[0]:
glow = pygame.Rect(
x,
draw_y,
CARD_WIDTH,
CARD_HEIGHT
).inflate(14, 14)
pygame.draw.rect(
screen,
LIGHT_GOLD,
glow,
4,
border_radius=14
)
def draw_hint_bar(self, screen, game):
footer = SMALL_FONT.render(
&quot;Ctrl+H : Ask the Consigliere Advice taken: &quot;
+ str(game.hints_used),
True,
GRAY
)
screen.blit(footer, (32, HEIGHT - 44))
if (
not game.show_hint
or game.reveal_phase
or game.game_over
):
return
hint = get_hint(game)
if not hint:
return
card, prob, reason = hint
message = SMALL_FONT.render(
&quot;THE CONSIGLIERE SAYS: play &quot;
+ card.rank + card.suit
+ &quot; (&quot; + str(int(prob * 100)) + &quot;% win chance) - &quot;
+ reason,
True,
WHITE
)
panel = pygame.Rect(
0,
0,
message.get_width() + 40,
44
)
panel.center = (WIDTH // 2, HEIGHT // 2 + 60)
pygame.draw.rect(
screen,

(70, 0, 18),
panel,
border_radius=12
)
pygame.draw.rect(
screen,
LIGHT_GOLD,
panel,
2,
border_radius=12
)
screen.blit(
message,
(panel.x + 20, panel.y + 11)
)
def draw_game_over(self, screen, game):
overlay = pygame.Surface(
(WIDTH, HEIGHT)
)
overlay.set_alpha(180)
overlay.fill((0, 0, 0))
screen.blit(overlay, (0, 0))
if game.player_score &gt; game.ai_score:
title = &quot;YOU RUN THE TABLE&quot;
quote = &quot;Respect earned.&quot;
color = GOLD
elif game.player_score &lt; game.ai_score:
title = &quot;YOU SLEEP WITH THE FISHES&quot;
quote = &quot;Nothing personal. It&#39;s just business.&quot;
color = RED
else:
title = &quot;A STANDOFF&quot;
quote = &quot;We settle this another time.&quot;
color = WHITE
text = TITLE_FONT.render(
title,
True,
color
)
screen.blit(
text,
(
WIDTH // 2 -
text.get_width() // 2,
250
)
)
score_text = BIG_FONT.render(
f&quot;{game.player_score} - {game.ai_score}&quot;,

True,
WHITE
)
screen.blit(
score_text,
(
WIDTH // 2 -
score_text.get_width() // 2,
380
)
)
quote_text = TAGLINE_FONT.render(
quote,
True,
LIGHT_GOLD
)
screen.blit(
quote_text,
(
WIDTH // 2 -
quote_text.get_width() // 2,
440
)
)
# =====================================================
# PLAYER INPUT
# =====================================================
def get_clicked_player_card(game, mouse_pos):
spacing = 140
start_x = (
WIDTH // 2
- (len(game.player_hand) * spacing) // 2
)
y = HEIGHT - 240
for i, card in enumerate(game.player_hand):
x = start_x + i * spacing
rect = pygame.Rect(
x,
y,
CARD_WIDTH,
CARD_HEIGHT
)
if rect.collidepoint(mouse_pos):
return card
return None
# =====================================================
# HINT SYSTEM (Ctrl + H)
# =====================================================
def get_hint(game):

&quot;&quot;&quot;
Suggest a card using only information the player could know:
the player&#39;s own hand and the cards already played.
Every other card could be in the AI&#39;s hand, so the win chance
of a card is estimated against all unseen cards.
&quot;&quot;&quot;
if not game.player_hand:
return None
known = set(
(c.suit, c.rank)
for c in game.player_hand + game.played_cards
if c
)
unseen = [
CARD_VALUE_MAP[r]
for s in SUITS
for r in VALUES
if (s, r) not in known
]
if not unseen:
return None
odds = {}
for card in game.player_hand:
wins = sum(1 for v in unseen if card.value &gt; v)
ties = sum(1 for v in unseen if card.value == v)
odds[card] = (wins + 0.5 * ties) / len(unseen)
strong = [c for c in game.player_hand if odds[c] &gt;= 0.60]
if strong:
best = min(strong, key=lambda c: c.value)
reason = &quot;wins cheaply and saves your higher cards&quot;
else:
best = max(game.player_hand, key=lambda c: odds[c])
if odds[best] &gt;= 0.45:
reason = &quot;your best chance this round&quot;
else:
best = min(game.player_hand, key=lambda c: c.value)
reason = &quot;sacrifice your weakest card, keep the strong ones&quot;
return best, odds[best], reason
# =====================================================
# ROUND RESOLUTION
# =====================================================
def resolve_round(game):
game.played_cards.extend(
[game.selected_card, game.ai_selected]
)
if game.selected_card.value &gt; game.ai_selected.value:
game.player_score += 1
elif game.selected_card.value &lt; game.ai_selected.value:
game.ai_score += 1

game.reveal_phase = True
# =====================================================
# NEXT ROUND
# =====================================================
def start_next_round(game):
game.selected_card = None
game.ai_selected = None
game.reveal_phase = False
game.round_number += 1
if (
game.round_number &gt; 5
or
len(game.player_hand) == 0
or
len(game.ai_hand) == 0
):
game.game_over = True
# AI UTILITIES
def evaluate_card(card):
return card.value
# EASY AI (BFS)
class BFSAI:
def choose_card(self, ai_hand):
if not ai_hand:
return None
queue = deque()
for card in ai_hand:
queue.append(card)
best_card = queue[0]
best_score = evaluate_card(best_card)
while queue:
current = queue.popleft()
score = evaluate_card(current)
if score &gt; best_score:
best_score = score
best_card = current
return best_card
# MEDIUM AI (DFS)
class DFSAI:
def __init__(self):
self.best_card = None
self.best_score = -999
def dfs(self, cards, index):

if index &gt;= len(cards):
return
card = cards[index]
score = card.value
if score &gt; self.best_score:
self.best_score = score
self.best_card = card
self.dfs(cards, index + 1)
def choose_card(self, ai_hand):
self.best_card = None
self.best_score = -999
self.dfs(ai_hand, 0)
return self.best_card
# HARD AI MINIMAX
class MinimaxAI:
def minimax(
self,
ai_cards,
player_cards,
maximizing
):
if not ai_cards:
return 0
if maximizing:
best = -999
for card in ai_cards:
remaining = ai_cards.copy()
remaining.remove(card)
score = card.value + self.minimax(
remaining,
player_cards,
False
)
best = max(best, score)
return best
else:
worst = 999
for card in player_cards:
remaining = player_cards.copy()
remaining.remove(card)
score = -card.value
worst = min(worst, score)
return worst
def choose_card(
self,
ai_hand,
player_hand

):
best_move = None
best_score = -999
for card in ai_hand:
remaining = ai_hand.copy()
remaining.remove(card)
score = (
card.value
+
self.minimax(
remaining,
player_hand,
False
)
)
if score &gt; best_score:
best_score = score
best_move = card
return best_move
# HARD AI EXPECTIMAX
class ExpectimaxAI:
def expectimax(
self,
ai_cards,
player_cards,
maximizing
):
if not ai_cards:
return 0
if maximizing:
best = -999
for card in ai_cards:
remaining = ai_cards.copy()
remaining.remove(card)
value = (
card.value
+
self.expectimax(
remaining,
player_cards,
False
)
)
best = max(best, value)
return best
else:
if not player_cards:

return 0
total = 0
for card in player_cards:
total += card.value
return total / len(player_cards)
def choose_card(
self,
ai_hand,
player_hand
):
best_card = None
best_score = -999
for card in ai_hand:
remaining = ai_hand.copy()
remaining.remove(card)
score = (
card.value
+
self.expectimax(
remaining,
player_hand,
False
)
)
if score &gt; best_score:
best_score = score
best_card = card
return best_card
# DIFFICULTY MANAGER
class AIManager:
def __init__(self, difficulty):
self.difficulty = difficulty
if difficulty == &quot;easy&quot;:
self.ai = BFSAI()
elif difficulty == &quot;medium&quot;:
self.ai = DFSAI()
else:
self.minimax_ai = MinimaxAI()
self.expectimax_ai = ExpectimaxAI()
def choose_card(
self,
ai_hand,
player_hand
):
if self.difficulty == &quot;easy&quot;:
return self.ai.choose_card(

ai_hand
)
elif self.difficulty == &quot;medium&quot;:
return self.ai.choose_card(
ai_hand
)
else:
minimax_card = (
self.minimax_ai.choose_card(
ai_hand,
player_hand
)
)
expectimax_card = (
self.expectimax_ai.choose_card(
ai_hand,
player_hand
)
)
if (
minimax_card
and
expectimax_card
):
if (
minimax_card.value
&gt;=
expectimax_card.value
):
return minimax_card
return expectimax_card
return minimax_card
# AI PLAY
def ai_take_turn(game, ai_manager):
chosen = ai_manager.choose_card(
game.ai_hand,
game.player_hand
)
if chosen:
game.ai_hand.remove(chosen)
return chosen
# PLAYER PLAY
def player_play_card(
game,

card
):
if card in game.player_hand:
game.player_hand.remove(card)
return card
return None
# MAIN APPLICATION
def main():
menu = MainMenu()
gameplay_ui = GameplayUI()
game = None
ai_manager = None
state = &quot;menu&quot;
running = True
while running:
CLOCK.tick(FPS)
for event in pygame.event.get():
if event.type == pygame.QUIT:
running = False
# MENU EVENTS
if state == &quot;menu&quot;:
if menu.easy_btn.clicked(event):
game = GameState(&quot;easy&quot;)
ai_manager = AIManager(&quot;easy&quot;)
state = &quot;game&quot;
elif menu.medium_btn.clicked(event):
game = GameState(&quot;medium&quot;)
ai_manager = AIManager(&quot;medium&quot;)
state = &quot;game&quot;
elif menu.hard_btn.clicked(event):
game = GameState(&quot;hard&quot;)
ai_manager = AIManager(&quot;hard&quot;)
state = &quot;game&quot;
elif menu.quit_btn.clicked(event):
running = False
# GAME EVENTS
elif state == &quot;game&quot;:
if not game.game_over:
# Card Selection
if (

event.type == pygame.MOUSEBUTTONDOWN
and event.button == 1
and not game.reveal_phase
):
clicked_card = (
get_clicked_player_card(
game,
event.pos
)
)
if clicked_card:
game.selected_card = (
player_play_card(
game,
clicked_card
)
)
game.ai_selected = (
ai_take_turn(
game,
ai_manager
)
)
resolve_round(game)
# Hint Toggle (Ctrl + H)
if (
event.type == pygame.KEYDOWN
and event.key == pygame.K_h
and event.mod &amp; pygame.KMOD_CTRL
and not game.reveal_phase
):
game.show_hint = not game.show_hint
if game.show_hint:
game.hints_used += 1
# Next Round

if (
game.reveal_phase
and gameplay_ui.next_button.clicked(event)
):
start_next_round(game)

else:
if (
event.type
== pygame.KEYDOWN
):
if event.key == pygame.K_r:
state = &quot;menu&quot;
# DRAWING
if state == &quot;menu&quot;:
menu.draw(SCREEN)
elif state == &quot;game&quot;:
gameplay_ui.draw_background(
SCREEN
)
gameplay_ui.draw_scoreboard(
SCREEN,
game
)
gameplay_ui.draw_round_tracker(
SCREEN,
game
)
gameplay_ui.draw_ai_area(
SCREEN,
game
)
gameplay_ui.draw_center_area(
SCREEN,
game
)
gameplay_ui.draw_player_hand(
SCREEN,
game
)
gameplay_ui.draw_hint_bar(
SCREEN,
game
)
# Next Round Button

if (
game.reveal_phase
and
not game.game_over
):
gameplay_ui.next_button.draw(
SCREEN
)
# Game Over Overlay
if game.game_over:
gameplay_ui.draw_game_over(
SCREEN,
game
)
restart_text = MEDIUM_FONT.render(
&quot;Press R to return to Menu&quot;,
True,
WHITE
)
SCREEN.blit(
restart_text,
(
WIDTH // 2
- restart_text.get_width() // 2,
500
)
)
pygame.display.flip()
pygame.quit()
sys.exit()

if __name__ == &quot;__main__&quot;:
main()