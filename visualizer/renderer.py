from sys import setprofile
import pygame
from teams import teams

class Renderer():
    def __init__(self, screen, history, padding=(0, 0, 0, 0), ticks=50) -> None:
        self.screen = screen
        self.chartMaxVal = 50
        self.padding = padding
        self.sw, self.sh = pygame.display.get_surface().get_size()
        self.w, self.h = self.sw - padding[0] - padding[2], self.sw - padding[1] - padding[3]

        self.history = history
        self.matchday = -1

        self.ticks = ticks
        self.tick = 0
        self.pos_delay = 40
        self.delay_tick = 0

        self.team_positions = self.generate_teams_position_object()
        self.set_initial_pos()

        self.running = True

        self.GRID_COLOR = (100, 100, 104)

    def renderChart(self, team_points, lines_at=10):        
        pygame.draw.rect(self.screen, (72, 73, 93), (0, 35, 800, 146))
        pygame.draw.rect(self.screen, (94, 74, 67), (0, 146+35, 800, 35))
        pygame.draw.rect(self.screen, (67, 71, 59), (0, 217, 800, 35))
        pygame.draw.rect(self.screen, (94, 64, 67), (0, 636, 800, 35*3))

        for i in range(11):
            if i % 2 != 0:
                pygame.draw.rect(self.screen, (70, 70, 73), (0, 250 + i*35, 800, 35))

        lines = self.chartMaxVal/lines_at
        for i in range(int(lines)+1):
            pos = self.convertCoords((i*lines_at, 0))
            pygame.draw.rect(self.screen, self.GRID_COLOR, (pos[0], pos[1], 5, self.h))
            self.render_text(str(i*lines_at), (pos[0] + 10, pos[1]), color=(self.GRID_COLOR))

        for i, id in enumerate(self.team_positions):
            self.render_team_pos(id, self.team_positions[id]['pos'])
    
        self.render_text("Match day " + str(self.matchday+1), (10, 10))
    
    def update(self):
        if not self.running: return

        if self.delay_tick > self.pos_delay and self.matchday < len(self.history):
            self.tick += 1
            for id in self.team_positions:
                self.team_positions[id]['pos'][0] += self.team_positions[id]['vel'][0]
                self.team_positions[id]['pos'][1] += self.team_positions[id]['vel'][1]

        if self.tick >= self.ticks:
            self.matchday += 1
            if(self.matchday < len(self.history)):
                self.calculate_targets()
                self.tick = 0
                self.delay_tick = 0
            else:
                self.running = False
        self.delay_tick += 1

    def calculate_targets(self):
        data = self.history[self.matchday]
        sorted_teams = self.sort_teams(data)
        for i, id in enumerate(sorted_teams):
            id = int(id)
            points = data[str(id)]['pts']
            pos = i
            target = self.convertCoords((points, 35*pos + 20))

            curr_pos = self.team_positions[id]['pos']
            self.team_positions[id]['tar'] = [target[0], target[1]]
            vel = [(target[0] - curr_pos[0])/self.ticks, (target[1] - curr_pos[1])/self.ticks]
            self.team_positions[id]['vel'] = vel

    def set_initial_pos(self):
        data = self.history[0]
        sorted_teams = self.sort_teams(data)
        for i, id in enumerate(sorted_teams):
            id = int(id)
            pos = self.convertCoords((0, 35*i + 20))
            self.team_positions[id]['pos'] = [pos[0], pos[1]]



    def render_team_pos(self, id, pos):
        pygame.draw.circle(self.screen, (0, 0, 0), (pos[0]+3, pos[1]), 12)
        pygame.draw.circle(self.screen, teams[int(id)]['color'], (pos[0]+3, pos[1]), 7)
        self.render_text(teams[int(id)]['short'], (pos[0]+22, pos[1]-9))

    def render_team(self, id, points, pos, gd):
        pos = self.convertCoords((points, 35*pos + 20))
        pygame.draw.circle(self.screen, (0, 0, 0), (pos[0]+7, pos[1]), 12)
        pygame.draw.circle(self.screen, teams[int(id)]['color'], (pos[0]+7, pos[1]), 7)
        self.render_text(teams[int(id)]['short'] + " - " + str(points) +
                         "pts - GD: " + str(gd), (pos[0]+22, pos[1]-11))

    def convertCoords(self, pos):
        return (pos[0]*self.w/self.chartMaxVal) + self.padding[0], pos[1] + self.padding[1]

    def render_text(self, text, pos, color=(0, 0, 0), font="Arial Bold", size=30):
        myfont = pygame.font.SysFont(font, size)
        textsurface = myfont.render(text, False, color)
        self.screen.blit(textsurface, pos)
    
    def sort_teams(self, team_points):
        sorted_teams = []
        for i, iid in enumerate(team_points):
            if i == 0:
                sorted_teams.append(iid)
            else:
                found = False
                j = 0
                while j < len(sorted_teams) and not found:
                    jteam = sorted_teams[j]
                    curr_team_pts = team_points[iid]['pts']
                    if curr_team_pts == team_points[jteam]['pts']:
                        curr_team_gd = team_points[iid]['gd']
                        while not found and j < len(sorted_teams) and curr_team_pts == team_points[sorted_teams[j]]['pts']:
                            jteam = sorted_teams[j]
                            if curr_team_gd > team_points[jteam]['gd']:
                               sorted_teams.insert(j, iid)
                               found = True
                            j += 1
                        if not found:
                            sorted_teams.insert(j, iid)
                            found = True
                    elif curr_team_pts > team_points[jteam]['pts']:
                        sorted_teams.insert(j, iid)
                        found = True
                    j += 1
                if not found:
                    sorted_teams.append(iid)
        return sorted_teams


    def generate_teams_position_object(self):
        res = {}
        for id in teams:
            res[id] = {
                'pos': [0, 0],
                'tar': [0, 0],
                'vel': [0, 0]
            }
        return res
