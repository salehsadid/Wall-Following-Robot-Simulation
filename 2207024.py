import pygame
import sys
import math

# ==============================================================================
# CONFIGURATION & THEME
# High-Tech Emerald Green & Crisp White Theme (Glassmorphism & Neon Mint Glow)
# ==============================================================================
CELL_SIZE = 42
FPS = 5               # Logical simulation steps per second
RENDER_FPS = 60       # Smooth 60 FPS visual interpolation

# Palette (Curated Emerald Green & Crisp White Theme)
BG_COLOR         = (8, 20, 16)         # Deep emerald obsidian
ARENA_BG         = (12, 30, 24)        # Dark mint grid viewport
ARENA_BORDER     = (16, 185, 129)      # Neon emerald arena border
ARENA_GLOW       = (52, 211, 153, 60)  # Soft mint frame glow
GRID_DOT         = (30, 75, 55)        # Floor intersection dots
CELL_FLOOR       = (15, 36, 28)        # Floor cell tile

WALL_BG          = (6, 78, 59)         # Deep emerald jade wall block
WALL_OUTLINE     = (52, 211, 153)      # Electric mint neon outline
WALL_INNER       = (4, 47, 46)         # Dark forest inner core
WALL_CORE_DOT    = (255, 255, 255)     # Crisp white center rivet

PACMAN_COLOR     = (255, 255, 255)     # Crisp brilliant white body
PACMAN_OUTLINE   = (167, 243, 208)     # Soft mint border
PACMAN_GLOW      = (52, 211, 153, 65)  # Radiant emerald halo aura
PACMAN_EYE       = (6, 78, 59)         # Deep emerald expressive eye
PACMAN_PUPIL     = (255, 255, 255)     # Eye sparkle reflection

TRAIL_COLOR      = (52, 211, 153)      # Neon mint trajectory line
TRAIL_GLOW       = (255, 255, 255)     # Pure white breadcrumb beads

HUD_MASTER_BG    = (10, 26, 20)        # Master HUD panel background
HUD_CARD_BG      = (13, 34, 27)        # Dark emerald glass card
HUD_CARD_BORDER  = (22, 101, 52)       # Emerald card border
HUD_CARD_HEADER  = (18, 50, 38)        # Card header strip

TEXT_WHITE       = (255, 255, 255)     # Pure crisp white
TEXT_MUTED       = (167, 243, 208)     # Soft sage / mint text
TEXT_CYAN        = (110, 231, 183)     # Vibrant mint telemetry
TEXT_YELLOW      = (255, 255, 255)     # Bright white highlight
TEXT_GREEN       = (52, 211, 153)      # Emerald active
TEXT_RED         = (248, 113, 113)     # Coral wall warning

SENSOR_WALL_BG   = (185, 28, 28)       # Red detected cell
SENSOR_WALL_FG   = (255, 255, 255)     # White text on red
SENSOR_FREE_BG   = (16, 44, 35)        # Inactive sensor cell (dark emerald)
SENSOR_FREE_FG   = (167, 243, 208)     # Mint text

# ==============================================================================
# LEVEL DEFINITIONS (0: Empty, 1: Wall, 2: Start Position)
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
# ==============================================================================
class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visual_x = float(x)
        self.visual_y = float(y)
        self.direction = 'N'
        
        self.raw_sensors = (0, 0, 0, 0, 0, 0, 0, 0)
        self.states = (0, 0, 0, 0)
        self.active_rule_idx = 1
        self.active_rule_name = "Rule 1"
        self.active_condition = "All Clear (0,0,0,0)"
        self.active_action = "Move North (Open Space)"
        self.step_count = 0
        self.path_history = [(x, y)]

    def get_sensors(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        
        def is_wall(r, c):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                return 1 # Boundaries act as walls
            return 1 if grid[r][c] == 1 else 0

        r, c = self.y, self.x
        
        # 8 Proximity sensors relative to robot
        s1 = is_wall(r - 1, c - 1) # NW
        s2 = is_wall(r - 1, c)     # N
        s3 = is_wall(r - 1, c + 1) # NE
        s4 = is_wall(r, c + 1)     # E
        s5 = is_wall(r + 1, c + 1) # SE
        s6 = is_wall(r + 1, c)     # S
        s7 = is_wall(r + 1, c - 1) # SW
        s8 = is_wall(r, c - 1)     # W

        # User logic: Composite binary variables
        x1 = 1 if (s2 or s3) else 0 # North
        x2 = 1 if (s4 or s5) else 0 # East
        x3 = 1 if (s6 or s7) else 0 # South
        x4 = 1 if (s8 or s1) else 0 # West
        
        self.raw_sensors = (s1, s2, s3, s4, s5, s6, s7, s8)
        self.states = (x1, x2, x3, x4)
        
        # Action selection rules
        if x1 == 0 and x2 == 0 and x3 == 0 and x4 == 0:
            self.active_rule_idx = 1
            self.active_rule_name = "Rule 1"
            self.active_condition = "x1=0, x2=0, x3=0, x4=0"
            self.active_action = "Move NORTH (Advance / Search)"
        elif x1 == 1 and x2 == 0:
            self.active_rule_idx = 2
            self.active_rule_name = "Rule 2"
            self.active_condition = "x1=1, x2=0"
            self.active_action = "Move EAST (Turn Along Wall)"
        elif x2 == 1 and x3 == 0:
            self.active_rule_idx = 3
            self.active_rule_name = "Rule 3"
            self.active_condition = "x2=1, x3=0"
            self.active_action = "Move SOUTH (Follow Wall Right)"
        elif x3 == 1 and x4 == 0:
            self.active_rule_idx = 4
            self.active_rule_name = "Rule 4"
            self.active_condition = "x3=1, x4=0"
            self.active_action = "Move WEST (Follow Wall Behind)"
        elif x4 == 1 and x1 == 0:
            self.active_rule_idx = 5
            self.active_rule_name = "Rule 5"
            self.active_condition = "x4=1, x1=0"
            self.active_action = "Move NORTH (Follow Wall Left)"
        else:
            self.active_rule_idx = 0
            self.active_rule_name = "Trap"
            self.active_condition = "Corner / Enclosed"
            self.active_action = "Halt (No Rule Matched)"

        return x1, x2, x3, x4

    def update(self, grid):
        x1, x2, x3, x4 = self.get_sensors(grid)
        
        # The Robot's Action rules (ordered set)
        if x1 == 0 and x2 == 0 and x3 == 0 and x4 == 0:
            self.y -= 1  # move north
            self.direction = 'N'
        elif x1 == 1 and x2 == 0:
            self.x += 1  # move east
            self.direction = 'E'
        elif x2 == 1 and x3 == 0:
            self.y += 1  # move south
            self.direction = 'S'
        elif x3 == 1 and x4 == 0:
            self.x -= 1  # move west
            self.direction = 'W'
        elif x4 == 1 and x1 == 0:
            self.y -= 1  # move north
            self.direction = 'N'
            
        self.step_count += 1
        self.path_history.append((self.x, self.y))
        if len(self.path_history) > 250:
            self.path_history.pop(0)

    def interpolate(self, dt):
        # Smooth gliding movement between grid cells (60 FPS fluidity)
        lerp_speed = 18.0 * (dt / 1000.0)
        self.visual_x += (self.x - self.visual_x) * min(1.0, lerp_speed)
        self.visual_y += (self.y - self.visual_y) * min(1.0, lerp_speed)

# ==============================================================================
# MAIN SIMULATOR APPLICATION
# ==============================================================================
class Game:
    def __init__(self):
        pygame.init()
        # High quality system typography
        self.font_title = pygame.font.SysFont('segoeui', 14, bold=True)
        self.font_bold  = pygame.font.SysFont('segoeui', 12, bold=True)
        self.font_med   = pygame.font.SysFont('segoeui', 11)
        self.font_code  = pygame.font.SysFont('consolas', 12, bold=True)
        self.font_mini  = pygame.font.SysFont('consolas', 10, bold=True)
        self.font_lg    = pygame.font.SysFont('segoeui', 15, bold=True)

        self.level_idx = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = True
        self.mouth_timer = 0
        self.show_trail = True
        self.pulse_timer = 0.0

        self.load_level(self.level_idx)

    def load_level(self, idx):
        if idx < 0 or idx >= len(LEVELS):
            return
        
        self.level_idx = idx
        self.grid = [row[:] for row in LEVELS[idx]]
        
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        
        self.hud_height = 200
        # Proportional window dimensions
        self.width = max(self.cols * CELL_SIZE + 60, 880)
        self.arena_y = 20
        self.arena_h = self.rows * CELL_SIZE
        self.height = self.arena_y + self.arena_h + self.hud_height + 25
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"WFR Wall-Following Robot Simulator - Level {idx + 1}")
        
        # Locate robot spawn position
        self.robot = None
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 2:
                    self.robot = Robot(c, r)
                    self.grid[r][c] = 0

    def draw_arena(self):
        offset_x = (self.width - self.cols * CELL_SIZE) // 2
        
        # Arena Glass Container Frame (Emerald & Mint)
        frame_rect = pygame.Rect(offset_x - 10, self.arena_y - 10, self.cols * CELL_SIZE + 20, self.arena_h + 20)
        pygame.draw.rect(self.screen, ARENA_BG, frame_rect, border_radius=10)
        pygame.draw.rect(self.screen, ARENA_BORDER, frame_rect, width=2, border_radius=10)

        # Draw Cells & Walls
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(offset_x + c * CELL_SIZE, self.arena_y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if self.grid[r][c] == 1:
                    # High-Tech Beveled Emerald Wall
                    pygame.draw.rect(self.screen, WALL_BG, rect, border_radius=5)
                    pygame.draw.rect(self.screen, WALL_OUTLINE, rect, width=1, border_radius=5)
                    
                    # Inner dark forest core with crisp white center rivet
                    inner_rect = rect.inflate(-CELL_SIZE * 0.38, -CELL_SIZE * 0.38)
                    pygame.draw.rect(self.screen, WALL_INNER, inner_rect, border_radius=3)
                    pygame.draw.circle(self.screen, WALL_CORE_DOT, inner_rect.center, 2)
                else:
                    # Empty space with subtle mint floor tile and center dot
                    pygame.draw.rect(self.screen, CELL_FLOOR, rect, border_radius=2)
                    pygame.draw.circle(self.screen, GRID_DOT, rect.center, 2)

        # Trajectory Trail (Neon Mint with Pure White Beads)
        if self.show_trail and self.robot and len(self.robot.path_history) > 1:
            points = []
            for px, py in self.robot.path_history:
                pt_x = offset_x + px * CELL_SIZE + CELL_SIZE // 2
                pt_y = self.arena_y + py * CELL_SIZE + CELL_SIZE // 2
                points.append((pt_x, pt_y))
            if len(points) >= 2:
                pygame.draw.lines(self.screen, TRAIL_COLOR, False, points, 2)
            for pt in points[-15:]:
                pygame.draw.circle(self.screen, TRAIL_GLOW, pt, 3)

        # Active Sensor Ray Visualizers on the Maze
        if self.robot:
            cx = offset_x + self.robot.visual_x * CELL_SIZE + CELL_SIZE // 2
            cy = self.arena_y + self.robot.visual_y * CELL_SIZE + CELL_SIZE // 2
            
            # Draw subtle proximity sensor pings to 8 neighbor cells
            dirs = [
                (-1, -1, 's1'), (-1, 0, 's2'), (-1, 1, 's3'),
                (0, 1, 's4'), (1, 1, 's5'), (1, 0, 's6'),
                (1, -1, 's7'), (0, -1, 's8')
            ]
            
            (x1, x2, x3, x4) = self.robot.states
            s_vals = self.robot.raw_sensors
            
            for idx, (dr, dc, s_name) in enumerate(dirs):
                val = s_vals[idx]
                target_x = cx + dc * CELL_SIZE
                target_y = cy + dr * CELL_SIZE
                
                if val == 1:
                    # Wall detection ray (soft coral red ping)
                    pygame.draw.circle(self.screen, (248, 113, 113, 140), (int(target_x), int(target_y)), 4)
                else:
                    # Clear sensor ray (soft mint green ping)
                    pygame.draw.circle(self.screen, (52, 211, 153, 75), (int(target_x), int(target_y)), 2)

            # Draw Pac-Man with Crisp White Body & Emerald Halo Aura
            radius = CELL_SIZE // 2 - 3
            
            # Radiant Emerald Halo Glow
            halo_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(halo_surf, PACMAN_GLOW, (radius * 2, radius * 2), radius + 5)
            self.screen.blit(halo_surf, (cx - radius * 2, cy - radius * 2))
            
            # Crisp White Pac-Man Body
            pygame.draw.circle(self.screen, PACMAN_COLOR, (int(cx), int(cy)), radius)
            pygame.draw.circle(self.screen, PACMAN_OUTLINE, (int(cx), int(cy)), radius, width=1)
            
            # Smooth Sinusoidal Chomping Mouth Animation
            cycle = (self.mouth_timer % 400) / 400.0
            if cycle > 0.5: cycle = 1.0 - cycle
            mouth_angle = (math.pi / 4) * (cycle * 2) # 0 to 45 deg
            
            if mouth_angle > 0.05:
                if self.robot.direction == 'N':
                    start_angle = -math.pi / 2 - mouth_angle
                    end_angle   = -math.pi / 2 + mouth_angle
                elif self.robot.direction == 'S':
                    start_angle = math.pi / 2 - mouth_angle
                    end_angle   = math.pi / 2 + mouth_angle
                elif self.robot.direction == 'W':
                    start_angle = math.pi - mouth_angle
                    end_angle   = math.pi + mouth_angle
                else: # 'E'
                    start_angle = -mouth_angle
                    end_angle   = mouth_angle

                cut_radius = radius + 3
                pt1 = (cx + cut_radius * math.cos(start_angle), cy + cut_radius * math.sin(start_angle))
                pt2 = (cx + cut_radius * math.cos(end_angle), cy + cut_radius * math.sin(end_angle))
                pygame.draw.polygon(self.screen, ARENA_BG, [(cx, cy), pt1, pt2])
            
            # Deep Emerald Expressive Eye Looking Forward
            eye_offsets = {
                'N': (-4, -6),
                'S': (-4, 6),
                'E': (3, -7),
                'W': (-3, -7)
            }
            ex, ey = eye_offsets.get(self.robot.direction, (3, -7))
            eye_center = (int(cx + ex), int(cy + ey))
            pygame.draw.circle(self.screen, PACMAN_EYE, eye_center, 3)
            pygame.draw.circle(self.screen, PACMAN_PUPIL, (eye_center[0] - 1, eye_center[1] - 1), 1)

    def draw_hud(self):
        hud_y = self.arena_y + self.arena_h + 15
        hud_w = self.width - 30
        hud_x = 15
        
        # Master HUD Container Panel (Deep Emerald Theme)
        master_rect = pygame.Rect(hud_x, hud_y, hud_w, self.hud_height)
        pygame.draw.rect(self.screen, HUD_MASTER_BG, master_rect, border_radius=10)
        pygame.draw.rect(self.screen, HUD_CARD_BORDER, master_rect, width=1, border_radius=10)

        # Refresh robot sensors
        if self.robot:
            self.robot.get_sensors(self.grid)

        # ----------------------------------------------------------------------
        # Top Header Bar (Level, Mission Telemetry, Status Badge)
        # ----------------------------------------------------------------------
        bar_y = hud_y + 10
        title_surf = self.font_lg.render(f"WFR SIMULATOR  |  LEVEL {self.level_idx + 1}", True, TEXT_WHITE)
        self.screen.blit(title_surf, (hud_x + 14, bar_y))
        
        # Telemetry in header (Clean White & Mint)
        if self.robot:
            tele_str = f"POS: ({self.robot.x}, {self.robot.y})   HEADING: {self.robot.direction}   STEPS: {self.robot.step_count}"
            tele_surf = self.font_bold.render(tele_str, True, TEXT_CYAN)
            self.screen.blit(tele_surf, (hud_x + 280, bar_y + 2))
        
        # Status Pill Badge (Running / Paused)
        status_text = "● RUNNING" if not self.paused else "❚❚ PAUSED"
        status_bg = (6, 95, 70) if not self.paused else (127, 29, 29)
        status_fg = TEXT_WHITE if not self.paused else (254, 202, 202)
        badge_w, badge_h = 95, 24
        badge_rect = pygame.Rect(hud_x + hud_w - badge_w - 14, bar_y - 2, badge_w, badge_h)
        pygame.draw.rect(self.screen, status_bg, badge_rect, border_radius=12)
        pygame.draw.rect(self.screen, (52, 211, 153) if not self.paused else TEXT_RED, badge_rect, width=1, border_radius=12)
        b_txt = self.font_bold.render(status_text, True, status_fg)
        self.screen.blit(b_txt, b_txt.get_rect(center=badge_rect.center))

        # Thin Divider Line
        pygame.draw.line(self.screen, (22, 101, 52), (hud_x + 10, hud_y + 38), (hud_x + hud_w - 10, hud_y + 38), 1)

        # ----------------------------------------------------------------------
        # THREE MODERN GLASS CARDS
        # ----------------------------------------------------------------------
        card_top = hud_y + 46
        card_h = 115
        
        # Card 1: 3x3 Sensor Radar
        c1_w = 205
        c1_x = hud_x + 12
        c1_rect = pygame.Rect(c1_x, card_top, c1_w, card_h)
        pygame.draw.rect(self.screen, HUD_CARD_BG, c1_rect, border_radius=8)
        pygame.draw.rect(self.screen, HUD_CARD_BORDER, c1_rect, width=1, border_radius=8)
        
        pygame.draw.rect(self.screen, HUD_CARD_HEADER, pygame.Rect(c1_x, card_top, c1_w, 22), border_top_left_radius=8, border_top_right_radius=8)
        c1_title = self.font_bold.render("3x3 SENSOR RADAR (s1..s8)", True, TEXT_WHITE)
        self.screen.blit(c1_title, (c1_x + 8, card_top + 4))

        if self.robot:
            s1, s2, s3, s4, s5, s6, s7, s8 = self.robot.raw_sensors
            radar_ox = c1_x + 15
            radar_oy = card_top + 28
            box_sz = 26
            
            matrix = [
                [(s1, 's1'), (s2, 's2'), (s3, 's3')],
                [(s8, 's8'), ('P', 'BOT'), (s4, 's4')],
                [(s7, 's7'), (s6, 's6'), (s5, 's5')]
            ]
            for r_i in range(3):
                for c_i in range(3):
                    val, name = matrix[r_i][c_i]
                    sb_rect = pygame.Rect(radar_ox + c_i * (box_sz + 4), radar_oy + r_i * (box_sz + 3), box_sz, box_sz)
                    
                    if name == 'BOT':
                        # Crisp White Bot Center
                        pygame.draw.rect(self.screen, PACMAN_COLOR, sb_rect, border_radius=4)
                        p_t = self.font_mini.render("P", True, (6, 78, 59))
                        self.screen.blit(p_t, p_t.get_rect(center=sb_rect.center))
                    else:
                        is_wall = (val == 1)
                        b_col = SENSOR_WALL_BG if is_wall else SENSOR_FREE_BG
                        o_col = (248, 113, 113) if is_wall else (22, 101, 52)
                        t_col = SENSOR_WALL_FG if is_wall else SENSOR_FREE_FG
                        
                        pygame.draw.rect(self.screen, b_col, sb_rect, border_radius=4)
                        pygame.draw.rect(self.screen, o_col, sb_rect, width=1, border_radius=4)
                        t_surf = self.font_mini.render(f"{name}:{val}", True, t_col)
                        self.screen.blit(t_surf, t_surf.get_rect(center=sb_rect.center))

        # Card 2: Derived Boolean States (x1..x4)
        c2_w = 265
        c2_x = c1_x + c1_w + 12
        c2_rect = pygame.Rect(c2_x, card_top, c2_w, card_h)
        pygame.draw.rect(self.screen, HUD_CARD_BG, c2_rect, border_radius=8)
        pygame.draw.rect(self.screen, HUD_CARD_BORDER, c2_rect, width=1, border_radius=8)
        
        pygame.draw.rect(self.screen, HUD_CARD_HEADER, pygame.Rect(c2_x, card_top, c2_w, 22), border_top_left_radius=8, border_top_right_radius=8)
        c2_title = self.font_bold.render("DERIVED SENSING STATES (x1..x4)", True, TEXT_WHITE)
        self.screen.blit(c2_title, (c2_x + 8, card_top + 4))

        if self.robot:
            x1, x2, x3, x4 = self.robot.states
            items = [
                ("x1 (North)", x1, "s2 | s3"),
                ("x2 (East)",  x2, "s4 | s5"),
                ("x3 (South)", x3, "s6 | s7"),
                ("x4 (West)",  x4, "s8 | s1")
            ]
            for idx, (label, val, formula) in enumerate(items):
                item_y = card_top + 28 + idx * 21
                lbl_surf = self.font_med.render(f"{label} [{formula}]:", True, TEXT_MUTED)
                self.screen.blit(lbl_surf, (c2_x + 10, item_y))
                
                # Pill Badge (Blocked vs Clear)
                is_on = (val == 1)
                b_text = "1: BLOCKED" if is_on else "0: CLEAR"
                b_bg = (127, 29, 29) if is_on else (6, 95, 70)
                b_fg = (254, 202, 202) if is_on else TEXT_WHITE
                border_c = TEXT_RED if is_on else (52, 211, 153)
                
                p_rect = pygame.Rect(c2_x + 175, item_y - 1, 80, 18)
                pygame.draw.rect(self.screen, b_bg, p_rect, border_radius=4)
                pygame.draw.rect(self.screen, border_c, p_rect, width=1, border_radius=4)
                p_txt = self.font_mini.render(b_text, True, b_fg)
                self.screen.blit(p_txt, p_txt.get_rect(center=p_rect.center))

        # Card 3: Decision Engine & Implemented Logic
        c3_x = c2_x + c2_w + 12
        c3_w = hud_w - (c3_x - hud_x) - 12
        c3_rect = pygame.Rect(c3_x, card_top, c3_w, card_h)
        pygame.draw.rect(self.screen, HUD_CARD_BG, c3_rect, border_radius=8)
        pygame.draw.rect(self.screen, HUD_CARD_BORDER, c3_rect, width=1, border_radius=8)
        
        pygame.draw.rect(self.screen, HUD_CARD_HEADER, pygame.Rect(c3_x, card_top, c3_w, 22), border_top_left_radius=8, border_top_right_radius=8)
        c3_title = self.font_bold.render("ACTION SELECTION ENGINE", True, TEXT_WHITE)
        self.screen.blit(c3_title, (c3_x + 8, card_top + 4))

        if self.robot:
            # Active Rule Emerald Banner
            active_box = pygame.Rect(c3_x + 8, card_top + 28, c3_w - 16, 36)
            pygame.draw.rect(self.screen, (6, 78, 59), active_box, border_radius=6)
            pygame.draw.rect(self.screen, (52, 211, 153), active_box, width=1, border_radius=6)
            
            rule_header = f"⚡ TRIGGERED: {self.robot.active_rule_name}  ({self.robot.active_condition})"
            action_desc = f"➔ {self.robot.active_action}"
            
            self.screen.blit(self.font_bold.render(rule_header, True, TEXT_WHITE), (c3_x + 14, card_top + 31))
            self.screen.blit(self.font_code.render(action_desc, True, TEXT_CYAN), (c3_x + 14, card_top + 48))

            # Ordered Priority Rules Preview
            rules_summary = [
                (1, "R1: All Clear -> Move N"),
                (2, "R2: Wall Ahead -> Move E"),
                (3, "R3: Wall Right -> Move S"),
                (4, "R4: Wall Behind -> Move W"),
                (5, "R5: Wall Left  -> Move N")
            ]
            
            r_str1 = " | ".join([f"{'▶' if self.robot.active_rule_idx==r_num else ''}{text}" for r_num, text in rules_summary[:3]])
            r_str2 = " | ".join([f"{'▶' if self.robot.active_rule_idx==r_num else ''}{text}" for r_num, text in rules_summary[3:]])
            self.screen.blit(self.font_mini.render(r_str1, True, TEXT_MUTED), (c3_x + 12, card_top + 72))
            self.screen.blit(self.font_mini.render(r_str2, True, TEXT_MUTED), (c3_x + 12, card_top + 88))

        # ----------------------------------------------------------------------
        # Bottom Controls Strip (Crisp White & Emerald Key Pills)
        # ----------------------------------------------------------------------
        ctrl_y = hud_y + 168
        controls = [
            ("SPACE", "PLAY / PAUSE"),
            ("RIGHT / S", "STEP"),
            ("1 - 5", "LEVEL"),
            ("R", "RESET"),
            ("T", "TRAIL")
        ]
        
        cx = hud_x + 14
        for key, desc in controls:
            k_surf = self.font_mini.render(key, True, TEXT_WHITE)
            k_rect = pygame.Rect(cx, ctrl_y, k_surf.get_width() + 10, 20)
            pygame.draw.rect(self.screen, (18, 50, 38), k_rect, border_radius=4)
            pygame.draw.rect(self.screen, (52, 211, 153), k_rect, width=1, border_radius=4)
            self.screen.blit(k_surf, (cx + 5, ctrl_y + 3))
            
            d_surf = self.font_med.render(desc, True, TEXT_MUTED)
            self.screen.blit(d_surf, (cx + k_rect.width + 6, ctrl_y + 2))
            
            cx += k_rect.width + d_surf.get_width() + 20

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_arena()
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        step_timer = 0
        while self.running:
            dt = self.clock.tick(RENDER_FPS)
            self.pulse_timer += dt / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key in (pygame.K_RIGHT, pygame.K_s) and self.paused:
                        self.robot.update(self.grid)
                        self.mouth_timer += 200
                    elif event.key == pygame.K_r:
                        self.load_level(self.level_idx)
                        self.paused = True
                    elif event.key == pygame.K_t:
                        self.show_trail = not self.show_trail
                    elif pygame.K_1 <= event.key <= pygame.K_5:
                        self.load_level(event.key - pygame.K_1)
                        self.paused = True
                        
            if not self.paused:
                step_timer += dt
                self.mouth_timer += dt
                if step_timer > 1000 / FPS: # Step every 200ms
                    self.robot.update(self.grid)
                    step_timer = 0
            
            # Smooth position interpolation for high-refresh visual fluidity
            if self.robot:
                self.robot.interpolate(dt)

            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        Game().run()
    except Exception as e:
        print(f"Error running game: {e}")
        pygame.quit()
