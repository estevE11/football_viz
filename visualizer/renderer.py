from sys import setprofile
import pygame
from teams import teams

class Renderer():
    def __init__(self, screen, padding=(0, 0, 0, 0)) -> None:
        self.screen = screen
        self.chartMaxVal = 50
        self.padding = padding
        self.sw, self.sh = pygame.display.get_surface().get_size()
        self.w, self.h = self.sw - padding[0] - padding[2], self.sw - padding[1] - padding[3]

        self.GRID_COLOR = (100, 100, 104)

    def renderChart(self, team_points, lines_at=10):
        lines = self.chartMaxVal/lines_at
        for i in range(int(lines)+1):
            pos = self.convertCoords((i*lines_at, 0))
            pygame.draw.rect(self.screen, self.GRID_COLOR, (pos[0], pos[1], 5, self.h))
            self.render_text(str(i*lines_at), (pos[0] + 10, pos[1]), color=(self.GRID_COLOR))

        #sort teams
        sorted_teams = self.sort_teams(team_points)

        for i, id in enumerate(sorted_teams):
            self.render_team(
                id, team_points[id]['pts'], i, team_points[id]['gd'])

    def render_team(self, id, points, pos, gd):
        pos = self.convertCoords((points, 35*pos + 20))
        pygame.draw.circle(self.screen, (0, 0, 0), (pos[0]+7, pos[1]), 12)
        pygame.draw.circle(self.screen, teams[int(id)]['color'], (pos[0]+7, pos[1]), 7)
        self.render_text(teams[int(id)]['short'] + " - " + str(points) +
                         "pts - GD: " + str(gd), (pos[0]+22, pos[1]-11))

    def convertCoords(self, pos):
        return (pos[0]*self.w/self.chartMaxVal) + self.padding[0], pos[1] + self.padding[1]

    def render_text(self, text, pos, color=(0, 0, 0), font="Arial", size=20):
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

