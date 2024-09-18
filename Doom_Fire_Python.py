import random
import pygame

# Configurações de fogo e janela
FIRE_WIDTH = 320
FIRE_HEIGHT = 200
SCALE = 3
SLIDER_HEIGHT = 20

# Paleta de cores para o efeito de fogo
FIRE_COLOR_PALETTE = [
    (7, 7, 7), (31, 7, 7), (47, 15, 7), (71, 15, 7), (87, 23, 7), (103, 31, 7), (119, 31, 7),
    (143, 39, 7), (159, 47, 7), (175, 63, 7), (191, 71, 7), (199, 71, 7), (223, 79, 7),
    (223, 87, 7), (223, 87, 7), (215, 95, 7), (215, 95, 7), (215, 103, 15), (207, 111, 15),
    (207, 119, 15), (207, 127, 15), (207, 135, 23), (199, 135, 23), (199, 143, 23),
    (199, 151, 31), (191, 159, 31), (191, 159, 31), (191, 167, 39), (191, 167, 39),
    (191, 175, 47), (183, 175, 47), (183, 183, 47), (183, 183, 55), (207, 207, 111),
    (223, 223, 159), (239, 239, 199), (255, 255, 255)
]

class Slider:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = 0.5
        self.grabbed = False

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pos = (self.rect.x + int(self.value * self.rect.w), self.rect.y + self.rect.h // 2)
        pygame.draw.circle(screen, (200, 200, 200), pos, self.rect.h // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            self.value = (event.pos[0] - self.rect.x) / self.rect.w
            self.value = max(0, min(1, self.value))

class DoomFire:
    def __init__(self):
        self.fire_pixels = [0] * (FIRE_WIDTH * FIRE_HEIGHT)
        
        pygame.init()
        self.screen = pygame.display.set_mode((FIRE_WIDTH * SCALE, FIRE_HEIGHT * SCALE + SLIDER_HEIGHT))
        pygame.display.set_caption("Doom Fire Effect")
        
        self.slider = Slider(10, 5, FIRE_WIDTH * SCALE - 20, 10)
        
        # Carregar o logo .png
        self.logo = pygame.image.load('amazdoom/doom_logo.png').convert_alpha()
        # Calcular a nova altura mantendo a proporção
        logo_width = FIRE_WIDTH * SCALE
        logo_height = int((logo_width / self.logo.get_width()) * self.logo.get_height())
        self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        
        # Criar superfície para o fundo preto
        self.background = pygame.Surface((FIRE_WIDTH * SCALE, FIRE_HEIGHT * SCALE))
        self.background.fill((0, 0, 0))

    def create_fire_source(self):
        for x in range(FIRE_WIDTH):
            self.fire_pixels[(FIRE_HEIGHT - 1) * FIRE_WIDTH + x] = len(FIRE_COLOR_PALETTE) - 1

    def update_fire_intensity(self):
        # Ajustando a intensidade para ser controlada pelo slider
        min_intensity = int(FIRE_HEIGHT * 0.1)  # 10% da altura
        max_intensity = int(FIRE_HEIGHT * 0.7)  # 70% da altura
        intensity_range = max_intensity - min_intensity
        intensity = self.slider.value * intensity_range + min_intensity
        
        decay_factor = max(1, int(3 * (1 - self.slider.value)))
        
        for y in range(FIRE_HEIGHT - 1, 0, -1):
            for x in range(FIRE_WIDTH):
                from_index = y * FIRE_WIDTH + x
                decay = random.randint(0, decay_factor)
                wind = random.randint(-1, 1)
                to_index = ((y - 1) * FIRE_WIDTH + (x + wind) % FIRE_WIDTH)
                
                new_intensity = max(0, min(len(FIRE_COLOR_PALETTE) - 1, self.fire_pixels[from_index] - decay))
                self.fire_pixels[to_index] = new_intensity

        if random.random() < 0.5 + (self.slider.value * 0.5):
            for x in range(FIRE_WIDTH):
                self.fire_pixels[(FIRE_HEIGHT - 1) * FIRE_WIDTH + x] = len(FIRE_COLOR_PALETTE) - 1

    def render_fire(self):
        fire_surface = pygame.Surface((FIRE_WIDTH, FIRE_HEIGHT), pygame.SRCALPHA)

        for y in range(FIRE_HEIGHT):
            for x in range(FIRE_WIDTH):
                pixel_index = y * FIRE_WIDTH + x
                fire_intensity = self.fire_pixels[pixel_index]
                color = FIRE_COLOR_PALETTE[fire_intensity]
                fire_surface.set_at((x, y), (*color, 150))  # Reduzido a opacidade para 150

        scaled_fire = pygame.transform.scale(fire_surface, (FIRE_WIDTH * SCALE, FIRE_HEIGHT * SCALE))
        
        # Desenhar o fundo preto primeiro
        self.screen.blit(self.background, (0, SLIDER_HEIGHT))
        
        # Centralizar o logo
        logo_x = (FIRE_WIDTH * SCALE - self.logo.get_width()) // 2
        logo_y = SLIDER_HEIGHT + (FIRE_HEIGHT * SCALE - self.logo.get_height()) // 2
        self.screen.blit(self.logo, (logo_x, logo_y))
        
        # Desenhar o fogo sobre o logo
        self.screen.blit(scaled_fire, (0, SLIDER_HEIGHT))
        
        # Desenhar o slider
        self.slider.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.create_fire_source()
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.slider.handle_event(event)

            self.update_fire_intensity()
            self.render_fire()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    doom_fire = DoomFire()
    doom_fire.run()

