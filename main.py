import ConwayEngine

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder

from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior

class ControlPanel(BoxLayout):

    simSpeed = NumericProperty(1)
    generationCounter = NumericProperty(0)
    running = False

    def update(self, generationCount):
        self.simSpeed = round(self.ids.speedSlider.value)
        self.generationCounter = generationCount

    def toggleRunning(self):
        self.running = not self.running

class UserInterface(BoxLayout):

    def update(self, world, dt):
        self.ids.worldgrid.update(world)
        self.ids.controlpanel.update(world.generations)

class BackgroundColor(Widget):
    background_color = ListProperty([0, 0, 0, 1])

class GridRenderer(GridLayout, BackgroundColor):
    gridHeight = NumericProperty(1)
    gridWidth = NumericProperty(1)
    CellRenderers = None

    def update(self, world):
        dimensions = world.getDimensions()
        self.gridHeight = dimensions[1]
        self.gridWidth = dimensions[0]

        if not self.CellRenderers:
            self.buildCellRenderers(world.grid.cells)
        else:
            self.updateCellRenderers(world.grid.cells)

    def buildCellRenderers(self, cells):
        self.CellRenderers = {}
        for y in range(0, self.gridHeight):
            for x in range(0, self.gridWidth):
                cell = (x, y)
                #print('Added', cell)
                newRenderer = CellRenderer()
                newRenderer.setCell(cells[cell], cell)
                self.CellRenderers[cell] = newRenderer
                self.add_widget(newRenderer)

    def updateCellRenderers(self, cells):
        for cell in cells.keys():
            if self.parent.ids.controlpanel.ids.coordCheckBox.active:
                self.CellRenderers[cell].update(cells[cell], cell)
            else:
                self.CellRenderers[cell].update(cells[cell])

class CellRenderer(ButtonBehavior, Label, BackgroundColor):
    aliveColour = [1, 1, 1, 1]
    deadColour = [0, 0, 0, 1]
    cellColour = ListProperty(deadColour)
    currentColour = cellColour
    cellString = StringProperty()
    cell = ''

    def update(self, cell, coord=None):
        self.setCell(cell, coord)
        if self.cell.isAlive:
            self.currentColour = self.aliveColour
        else:
            self.currentColour = self.deadColour

    def setCell(self, cell, coord=None):
        self.cell = cell
        if coord:
            self.cellString = str(coord)
        else:
            self.cellString = ''

    def handleClick(self):
        self.cell.toggleAlive()

class KivyConwayApp(App):

    def build(self):
        self.tickTime = 1

        self.world = ConwayEngine.World(50, 30)

        self.gui = UserInterface()

        self.update(0)
        Clock.schedule_interval(self.update, 1.0/30.0)

        return self.gui

    def setTickTime(self):
        self.tickTime = 1/self.gui.ids.controlpanel.simSpeed

    def update(self, dt):
        if self.gui.ids.controlpanel.running:
            self.tickTime -= dt
            if self.tickTime <= 0:
                self.world.update()
                self.setTickTime()
        self.gui.update(self.world, dt)

if __name__ == "__main__":
    KivyConwayApp().run()
