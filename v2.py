import pygame
import sys
import math

# ==============================================================================
# CONFIGURATION & THEME
# Modern Cyber-Robotics Lab Aesthetics
# ==============================================================================
FPS_DISPLAY = 60
DEFAULT_SIM_SPEED = 5 # simulation steps per second

# Palette (Tailored Modern Dark Sci-Fi)
BG_MAIN       = (11, 15, 25)      # Deep space slate
ARENA_BG      = (17, 24, 39)      # Grid arena dark viewport
GRID_LINE     = (30, 41, 59)      # Subtle arena grid lines
GRID_DOT      = (51, 65, 85)      # Grid intersection dots

WALL_BG       = (30, 58, 138)     # Tech cobalt blue wall
WALL_ACCENT   = (56, 189, 248)    # Neon sky blue border
WALL_INNER    = (15, 23, 42)      # Wall inset core

ROBOT_SHELL   = (241, 245, 249)   # Rover alloy white
ROBOT_ACCENT  = (14, 165, 233)    # Electric cyan trim
ROBOT_CORE    = (16, 185, 129)    # Emerald pulse core
SENSOR_BEAM   = (56, 189, 248, 65)# Transparent sensor cone

PANEL_BG      = (15, 23, 42)      # Dashboard background
CARD_BG       = (23, 32, 51)      # Glassy dark card
CARD_BORDER   = (38, 50, 72)      # Card border

TEXT_PRIMARY   = (248, 250, 252)  # Bright white/silver
TEXT_MUTED     = (148, 163, 184)  # Muted slate
TEXT_CYAN      = (56, 189, 248)   # Cyan telemetry
TEXT_EMERALD   = (52, 211, 153)   # Active/Green
TEXT_AMBER     = (251, 191, 36)   # Warning amber
TEXT_ROSE      = (244, 63, 94)    # Wall alert rose

BTN_BG         = (30, 41, 59)
BTN_HOVER      = (51, 65, 85)
BTN_ACTIVE     = (14, 165, 233)
BTN_TEXT       = (241, 245, 249)

TRAIL_COLOR    = (168, 85, 247)   # Neon purple trajectory trail

# ==============================================================================
# LEVEL DEFINITIONS (0: Empty, 1: Wall, 2: Start Position)
# Exactly matching original WFR specifications
# ==============================================================================
LEVELS = [
    # Level 1: Simple straight wall
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # Level 2: Internal Room
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    # Level 3: External Object (Island)
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # Level 4: Complex Maze (U-shapes and dead ends)
    [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 2, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    # Level 5: Open environment with sparse obstacles
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
]

# ==============================================================================
# ROBOT MODEL
# Implements the identical Nilsson WFR Logic with smooth animation interpolation
# ==============================================================================
class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visual_x = float(x)
        self.visual_y = float(y)
        self.direction = 'N' # 'N', 'E', 'S', 'W'
        self.last_rule_idx = None
        self.last_rule_desc = "Initialized"
        self.path_history = [(x, y)]
        self.step_count = 0

    def get_sensors(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        
        def is_wall(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return 1 # Boundaries act as walls
            return 1 if grid[r][c] == 1 else 0

        r, c = self.y, self.x
        
        # 8-Neighborhood sensor cells relative to the robot
        s1 = is_wall(r - 1, c - 1) # NW
        s2 = is_wall(r - 1, c)     # N
        s3 = is_wall(r - 1, c + 1) # NE
        s4 = is_wall(r, c + 1)     # E
        s5 = is_wall(r + 1, c + 1) # SE
        s6 = is_wall(r + 1, c)     # S
        s7 = is_wall(r + 1, c - 1) # SW
        s8 = is_wall(r, c - 1)     # W

        # User logic: Composite binary variables
        x1 = 1 if (s2 or s3) else 0 # North obstacle ahead
        x2 = 1 if (s4 or s5) else 0 # East obstacle
        x3 = 1 if (s6 or s7) else 0 # South obstacle
        x4 = 1 if (s8 or s1) else 0 # West obstacle
        
        raw_sensors = {'s1': s1, 's2': s2, 's3': s3, 's4': s4,
                       's5': s5, 's6': s6, 's7': s7, 's8': s8}
        return (x1, x2, x3, x4), raw_sensors

    def update(self, grid):
        (x1, x2, x3, x4), _ = self.get_sensors(grid)
        
        # The Robot's Action rules (ordered set) - Exactly as defined in original WFR
        if x1 == 0 and x2 == 0 and x3 == 0 and x4 == 0:
            self.y -= 1  # move north
            self.direction = 'N'
            self.last_rule_idx = 1
            self.last_rule_desc = "Rule 1: Open space -> Advance North"
        elif x1 == 1 and x2 == 0:
            self.x += 1  # move east
            self.direction = 'E'
            self.last_rule_idx = 2
            self.last_rule_desc = "Rule 2: Wall ahead -> Follow East"
        elif x2 == 1 and x3 == 0:
            self.y += 1  # move south
            self.direction = 'S'
            self.last_rule_idx = 3
            self.last_rule_desc = "Rule 3: Wall on right -> Follow South"
        elif x3 == 1 and x4 == 0:
            self.x -= 1  # move west
            self.direction = 'W'
            self.last_rule_idx = 4
            self.last_rule_desc = "Rule 4: Wall behind -> Follow West"
        elif x4 == 1 and x1 == 0:
            self.y -= 1  # move north
            self.direction = 'N'
            self.last_rule_idx = 5
            self.last_rule_desc = "Rule 5: Wall on left -> Follow North"
        else:
            self.last_rule_idx = 0
            self.last_rule_desc = "No rule matched (Corner trap / Stalled)"

        self.step_count += 1
        self.path_history.append((self.x, self.y))
        if len(self.path_history) > 300: # Limit history to keep memory clean
            self.path_history.pop(0)

    def interpolate(self, dt):
        # Smooth visual glide between grid cells
        lerp_speed = 18.0 * (dt / 1000.0)
        self.visual_x += (self.x - self.visual_x) * min(1.0, lerp_speed)
        self.visual_y += (self.y - self.visual_y) * min(1.0, lerp_speed)

# ==============================================================================
# UI COMPONENTS (Interactive Buttons & Cards)
# ==============================================================================
class Button:
    def __init__(self, rect, text, callback, font, bg_color=BTN_BG, active_color=BTN_ACTIVE):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.bg_color = bg_color
        self.active_color = active_color
        self.hovered = False
        self.is_active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    def draw(self, screen):
        color = self.active_color if self.is_active else (BTN_HOVER if self.hovered else self.bg_color)
        border_color = TEXT_CYAN if (self.hovered or self.is_active) else CARD_BORDER
        
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, border_color, self.rect, width=1, border_radius=6)
        
        text_surf = self.font.render(self.text, True, BTN_TEXT if not self.is_active else (15, 23, 42))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

# ==============================================================================
# MAIN SIMULATOR APPLICATION
# ==============================================================================
class ModernWFRSimulator:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("WFR Autonomous Rover - Cybernetics Laboratory")
        
        # Fixed pleasant window layout: Left Grid Arena (700px), Right Telemetry Panel (380px)
        self.arena_w = 700
        self.panel_w = 380
        self.win_w = self.arena_w + self.panel_w
        self.win_h = 670
        
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        self.clock = pygame.time.Clock()
        
        # Load modern typography
        self.font_title = pygame.font.SysFont('consolas', 20, bold=True)
        self.font_bold = pygame.font.SysFont('consolas', 15, bold=True)
        self.font_med = pygame.font.SysFont('consolas', 14)
        self.font_small = pygame.font.SysFont('consolas', 12)
        self.font_mini = pygame.font.SysFont('consolas', 10, bold=True)

        self.level_idx = 0
        self.sim_speed = DEFAULT_SIM_SPEED # Steps per second
        self.paused = True
        self.show_trail = True
        self.step_timer = 0
        self.pulse_timer = 0.0
        
        self.buttons = []
        self.init_buttons()
        self.load_level(self.level_idx)
        self.running = True

    def init_buttons(self):
        self.buttons.clear()
        bx = self.arena_w + 20
        
        # Control Action Buttons
        self.btn_play = Button((bx, 530, 105, 34), "PLAY", self.toggle_pause, self.font_bold)
        self.btn_step = Button((bx + 115, 530, 105, 34), "STEP", self.step_sim, self.font_bold)
        self.btn_reset = Button((bx + 230, 530, 110, 34), "RESET", self.reset_level, self.font_bold)
        
        # Secondary Controls: Speed & Trail
        self.btn_spd_down = Button((bx, 575, 50, 30), "- SPD", self.decrease_speed, self.font_small)
        self.btn_spd_up = Button((bx + 55, 575, 50, 30), "+ SPD", self.increase_speed, self.font_small)
        self.btn_trail = Button((bx + 115, 575, 105, 30), "TRAIL: ON", self.toggle_trail, self.font_small)
        self.btn_trail.is_active = True
        
        self.buttons.extend([self.btn_play, self.btn_step, self.btn_reset,
                             self.btn_spd_down, self.btn_spd_up, self.btn_trail])
        
        # Level selector buttons (1 to 5)
        self.lvl_buttons = []
        lvl_w = 64
        for i in range(5):
            b = Button((bx + i * (lvl_w + 6), 615, lvl_w, 32), f"LVL {i+1}", lambda idx=i: self.load_level(idx), self.font_bold)
            self.lvl_buttons.append(b)
            self.buttons.append(b)

    def load_level(self, idx):
        if idx < 0 or idx >= len(LEVELS):
            return
        self.level_idx = idx
        self.grid = [row[:] for row in LEVELS[idx]]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        
        # Calculate dynamic cell size to perfectly fill the arena viewport
        margin = 35
        avail_w = self.arena_w - 2 * margin
        avail_h = self.win_h - 2 * margin
        self.cell_size = min(avail_w // self.cols, avail_h // self.rows, 46)
        
        # Arena grid offsets for center alignment
        self.grid_origin_x = margin + (avail_w - self.cols * self.cell_size) // 2
        self.grid_origin_y = margin + (avail_h - self.rows * self.cell_size) // 2
        
        # Locate robot spawn
        self.robot = None
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 2:
                    self.robot = Robot(c, r)
                    self.grid[r][c] = 0 # Replace start marker with empty space
                    
        self.paused = True
        self.btn_play.text = "PLAY"
        self.btn_play.bg_color = BTN_BG
        
        # Update active state of level buttons
        for i, b in enumerate(self.lvl_buttons):
            b.is_active = (i == self.level_idx)

    def toggle_pause(self):
        self.paused = not self.paused
        self.btn_play.text = "PAUSE" if not self.paused else "PLAY"
        self.btn_play.bg_color = (22, 101, 52) if not self.paused else BTN_BG

    def step_sim(self):
        if self.robot:
            self.robot.update(self.grid)

    def reset_level(self):
        self.load_level(self.level_idx)

    def increase_speed(self):
        self.sim_speed = min(25, self.sim_speed + 2)

    def decrease_speed(self):
        self.sim_speed = max(1, self.sim_speed - 2)

    def toggle_trail(self):
        self.show_trail = not self.show_trail
        self.btn_trail.text = f"TRAIL: {'ON' if self.show_trail else 'OFF'}"
        self.btn_trail.is_active = self.show_trail

    # ==========================================================================
    # RENDERING METHODS
    # ==========================================================================
    def draw_arena(self):
        # Draw arena frame container
        arena_rect = pygame.Rect(15, 15, self.arena_w - 20, self.win_h - 30)
        pygame.draw.rect(self.screen, ARENA_BG, arena_rect, border_radius=10)
        pygame.draw.rect(self.screen, CARD_BORDER, arena_rect, width=2, border_radius=10)
        
        ox = self.grid_origin_x
        oy = self.grid_origin_y
        cs = self.cell_size
        
        # Draw grid cells & background
        for r in range(self.rows):
            for c in range(self.cols):
                rx = ox + c * cs
                ry = oy + r * cs
                cell_rect = pygame.Rect(rx, ry, cs, cs)
                
                if self.grid[r][c] == 1:
                    # Futuristic Wall Block
                    pygame.draw.rect(self.screen, WALL_BG, cell_rect, border_radius=4)
                    pygame.draw.rect(self.screen, WALL_ACCENT, cell_rect, width=1, border_radius=4)
                    # Inner tech detail
                    inner = cell_rect.inflate(-cs * 0.4, -cs * 0.4)
                    pygame.draw.rect(self.screen, WALL_INNER, inner, border_radius=2)
                else:
                    # Empty space with subtle grid line
                    pygame.draw.rect(self.screen, GRID_LINE, cell_rect, width=1)
                    # Crosshair dot at cell center
                    pygame.draw.circle(self.screen, GRID_DOT, cell_rect.center, 1)

        # Draw trajectory breadcrumbs trail
        if self.show_trail and self.robot and len(self.robot.path_history) > 1:
            points = []
            for px, py in self.robot.path_history:
                pt_x = ox + px * cs + cs // 2
                pt_y = oy + py * cs + cs // 2
                points.append((pt_x, pt_y))
            
            if len(points) >= 2:
                pygame.draw.lines(self.screen, TRAIL_COLOR, False, points, 2)
            for pt in points[-15:]: # Draw glowing dots on recent path
                pygame.draw.circle(self.screen, (216, 180, 254), pt, 3)

        # Draw Robot Rover
        if self.robot:
            cx = ox + self.robot.visual_x * cs + cs // 2
            cy = oy + self.robot.visual_y * cs + cs // 2
            radius = cs // 2 - 3
            
            # 1. Directional Sensor Scan Cone / Headlights
            cone_len = cs * 1.2
            dir_angles = {'N': -math.pi/2, 'E': 0, 'S': math.pi/2, 'W': math.pi}
            angle = dir_angles.get(self.robot.direction, -math.pi/2)
            
            cone_surface = pygame.Surface((self.win_w, self.win_h), pygame.SRCALPHA)
            spread = 0.45
            p1 = (cx + cone_len * math.cos(angle - spread), cy + cone_len * math.sin(angle - spread))
            p2 = (cx + cone_len * math.cos(angle + spread), cy + cone_len * math.sin(angle + spread))
            pygame.draw.polygon(cone_surface, SENSOR_BEAM, [(cx, cy), p1, p2])
            self.screen.blit(cone_surface, (0, 0))
            
            # 2. Outer Armor Ring
            pygame.draw.circle(self.screen, ROBOT_SHELL, (cx, cy), radius)
            pygame.draw.circle(self.screen, ROBOT_ACCENT, (cx, cy), radius, width=2)
            
            # 3. Inner Chassis
            pygame.draw.circle(self.screen, (15, 23, 42), (cx, cy), int(radius * 0.72))
            
            # 4. Pulsing Sensor Core
            pulse_scale = 0.8 + 0.2 * math.sin(self.pulse_timer * 6)
            core_r = max(2, int(radius * 0.38 * pulse_scale))
            pygame.draw.circle(self.screen, ROBOT_CORE, (cx, cy), core_r)
            
            # 5. Front Pointer / Direction Visor
            tip_x = cx + (radius - 1) * math.cos(angle)
            tip_y = cy + (radius - 1) * math.sin(angle)
            left_x = cx + (radius * 0.5) * math.cos(angle + 2.3)
            left_y = cy + (radius * 0.5) * math.sin(angle + 2.3)
            right_x = cx + (radius * 0.5) * math.cos(angle - 2.3)
            right_y = cy + (radius * 0.5) * math.sin(angle - 2.3)
            pygame.draw.polygon(self.screen, ROBOT_ACCENT, [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)])

    def draw_telemetry_panel(self):
        px = self.arena_w + 10
        pw = self.panel_w - 20
        
        # 1. Header Card
        header_rect = pygame.Rect(px, 15, pw, 72)
        pygame.draw.rect(self.screen, CARD_BG, header_rect, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER, header_rect, width=1, border_radius=8)
        
        title_surf = self.font_title.render("WFR ROVER TELEMETRY", True, TEXT_CYAN)
        sub_surf = self.font_med.render(f"LEVEL {self.level_idx + 1} | GRID {self.cols}x{self.rows}", True, TEXT_MUTED)
        self.screen.blit(title_surf, (px + 14, 25))
        self.screen.blit(sub_surf, (px + 14, 52))
        
        # Status Pill Badge
        status_text = "PAUSED" if self.paused else "ACTIVE"
        status_bg = (127, 29, 29) if self.paused else (6, 95, 70)
        status_fg = TEXT_ROSE if self.paused else TEXT_EMERALD
        badge_w, badge_h = 75, 24
        badge_rect = pygame.Rect(px + pw - badge_w - 14, 25, badge_w, badge_h)
        pygame.draw.rect(self.screen, status_bg, badge_rect, border_radius=12)
        pygame.draw.rect(self.screen, status_fg, badge_rect, width=1, border_radius=12)
        b_txt = self.font_mini.render(status_text, True, status_fg)
        self.screen.blit(b_txt, b_txt.get_rect(center=badge_rect.center))

        # 2. Mission Statistics Card
        stats_rect = pygame.Rect(px, 95, pw, 60)
        pygame.draw.rect(self.screen, CARD_BG, stats_rect, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER, stats_rect, width=1, border_radius=8)
        
        steps = self.robot.step_count if self.robot else 0
        pos_str = f"({self.robot.x}, {self.robot.y})" if self.robot else "(0,0)"
        dir_str = self.robot.direction if self.robot else "N"
        
        self.screen.blit(self.font_small.render("STEPS", True, TEXT_MUTED), (px + 20, 105))
        self.screen.blit(self.font_bold.render(str(steps), True, TEXT_PRIMARY), (px + 20, 125))
        
        self.screen.blit(self.font_small.render("COORDINATES", True, TEXT_MUTED), (px + 110, 105))
        self.screen.blit(self.font_bold.render(pos_str, True, TEXT_CYAN), (px + 110, 125))
        
        self.screen.blit(self.font_small.render("HEADING", True, TEXT_MUTED), (px + 230, 105))
        self.screen.blit(self.font_bold.render(f"{dir_str}", True, TEXT_EMERALD), (px + 230, 125))
        
        self.screen.blit(self.font_small.render("SPEED", True, TEXT_MUTED), (px + 300, 105))
        self.screen.blit(self.font_bold.render(f"{self.sim_speed} Hz", True, TEXT_AMBER), (px + 300, 125))

        # 3. Live 3x3 Proximity Sensor Radar
        radar_rect = pygame.Rect(px, 163, pw, 185)
        pygame.draw.rect(self.screen, CARD_BG, radar_rect, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER, radar_rect, width=1, border_radius=8)
        
        self.screen.blit(self.font_bold.render("PROXIMITY SENSOR ARRAY (s1..s8)", True, TEXT_PRIMARY), (px + 14, 172))
        
        (x1, x2, x3, x4), raw = self.robot.get_sensors(self.grid) if self.robot else ((0,0,0,0), {})
        
        # Draw 3x3 Radar Grid
        radar_ox = px + 25
        radar_oy = 200
        box_sz = 38
        
        sensor_layout = [
            [('s1', 'NW'), ('s2', 'N'), ('s3', 'NE')],
            [('s8', 'W'),  ('R', 'ROVER'), ('s4', 'E')],
            [('s7', 'SW'), ('s6', 'S'), ('s5', 'SE')]
        ]
        
        for r_idx in range(3):
            for c_idx in range(3):
                key, label = sensor_layout[r_idx][c_idx]
                sb_rect = pygame.Rect(radar_ox + c_idx * (box_sz + 6), radar_oy + r_idx * (box_sz + 6), box_sz, box_sz)
                
                if key == 'R':
                    # Center Rover
                    pygame.draw.rect(self.screen, ROBOT_ACCENT, sb_rect, border_radius=4)
                    r_lbl = self.font_mini.render("BOT", True, (15, 23, 42))
                    self.screen.blit(r_lbl, r_lbl.get_rect(center=sb_rect.center))
                else:
                    is_detected = raw.get(key, 0) == 1
                    s_color = (185, 28, 28) if is_detected else (30, 41, 59)
                    b_color = TEXT_ROSE if is_detected else CARD_BORDER
                    
                    pygame.draw.rect(self.screen, s_color, sb_rect, border_radius=4)
                    pygame.draw.rect(self.screen, b_color, sb_rect, width=1, border_radius=4)
                    
                    # Label
                    t1 = self.font_mini.render(key, True, TEXT_PRIMARY if is_detected else TEXT_MUTED)
                    t2 = self.font_mini.render("1" if is_detected else "0", True, TEXT_ROSE if is_detected else TEXT_MUTED)
                    self.screen.blit(t1, (sb_rect.x + 4, sb_rect.y + 4))
                    self.screen.blit(t2, (sb_rect.right - 12, sb_rect.bottom - 15))

        # Composite Boolean Variables (x1, x2, x3, x4)
        cv_ox = px + 175
        cv_oy = 202
        cv_items = [
            ("x1 (N/NE)", x1, "s2 | s3"),
            ("x2 (E/SE)", x2, "s4 | s5"),
            ("x3 (S/SW)", x3, "s6 | s7"),
            ("x4 (W/NW)", x4, "s8 | s1")
        ]
        
        for idx, (name, val, formula) in enumerate(cv_items):
            item_y = cv_oy + idx * 31
            # Pill indicator
            pill_rect = pygame.Rect(cv_ox, item_y, 160, 26)
            p_bg = (127, 29, 29) if val == 1 else (19, 78, 74)
            p_border = TEXT_ROSE if val == 1 else TEXT_EMERALD
            
            pygame.draw.rect(self.screen, p_bg, pill_rect, border_radius=4)
            pygame.draw.rect(self.screen, p_border, pill_rect, width=1, border_radius=4)
            
            name_surf = self.font_mini.render(name, True, TEXT_PRIMARY)
            val_surf = self.font_bold.render(str(val), True, TEXT_ROSE if val == 1 else TEXT_EMERALD)
            self.screen.blit(name_surf, (cv_ox + 8, item_y + 6))
            self.screen.blit(val_surf, (cv_ox + 140, item_y + 5))

        # 4. Decision Engine & Active Rule Card
        rule_rect = pygame.Rect(px, 356, pw, 160)
        pygame.draw.rect(self.screen, CARD_BG, rule_rect, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER, rule_rect, width=1, border_radius=8)
        
        self.screen.blit(self.font_bold.render("ACTION SELECTION ENGINE", True, TEXT_PRIMARY), (px + 14, 366))
        
        active_idx = self.robot.last_rule_idx if self.robot else None
        rules_text = [
            (1, "R1: x1=0 & x2=0 & x3=0 & x4=0 -> NORTH"),
            (2, "R2: x1=1 & x2=0               -> EAST"),
            (3, "R3: x2=1 & x3=0               -> SOUTH"),
            (4, "R4: x3=1 & x4=0               -> WEST"),
            (5, "R5: x4=1 & x1=0               -> NORTH")
        ]
        
        for i, (r_num, r_str) in enumerate(rules_text):
            ry = 390 + i * 23
            is_active = (active_idx == r_num)
            
            if is_active:
                hl_rect = pygame.Rect(px + 8, ry - 2, pw - 16, 21)
                pygame.draw.rect(self.screen, (30, 58, 138), hl_rect, border_radius=4)
                pygame.draw.rect(self.screen, TEXT_CYAN, hl_rect, width=1, border_radius=4)
                txt_surf = self.font_small.render(f"▶ {r_str}", True, TEXT_CYAN)
            else:
                txt_surf = self.font_small.render(f"  {r_str}", True, TEXT_MUTED)
                
            self.screen.blit(txt_surf, (px + 12, ry))

        # Draw Interactive Control Buttons
        for btn in self.buttons:
            btn.draw(self.screen)

    def draw(self):
        self.screen.fill(BG_MAIN)
        self.draw_arena()
        self.draw_telemetry_panel()
        pygame.display.flip()

    # ==========================================================================
    # MAIN EVENT & UPDATE LOOP
    # ==========================================================================
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS_DISPLAY)
            self.pulse_timer += dt / 1000.0
            
            # Event processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # Handle button clicks
                btn_handled = False
                for btn in self.buttons:
                    if btn.handle_event(event):
                        btn_handled = True
                        break
                        
                # Handle keyboard controls
                if not btn_handled and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toggle_pause()
                    elif event.key in (pygame.K_RIGHT, pygame.K_s):
                        self.step_sim()
                    elif event.key == pygame.K_r:
                        self.reset_level()
                    elif event.key == pygame.K_t:
                        self.toggle_trail()
                    elif event.key == pygame.K_UP:
                        self.increase_speed()
                    elif event.key == pygame.K_DOWN:
                        self.decrease_speed()
                    elif pygame.K_1 <= event.key <= pygame.K_5:
                        self.load_level(event.key - pygame.K_1)

            # Simulation update step (tied to sim_speed)
            if not self.paused and self.robot:
                self.step_timer += dt
                step_interval_ms = 1000.0 / self.sim_speed
                if self.step_timer >= step_interval_ms:
                    self.robot.update(self.grid)
                    self.step_timer = 0
            
            # Smooth position interpolation for high-refresh visual fluidity
            if self.robot:
                self.robot.interpolate(dt)

            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        app = ModernWFRSimulator()
        app.run()
    except Exception as e:
        print(f"Error in WFR Simulator v2: {e}")
        pygame.quit()
