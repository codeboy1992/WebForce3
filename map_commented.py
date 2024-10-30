# Projet : Voiture autonome

# Importation des bibliothèques nécessaires
import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import time

# Importation des modules Kivy pour créer une interface graphique
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

# Importation de l'objet Dqn depuis le fichier ai.py (qui contient l'IA pour la voiture autonome)
from ai import Dqn

# Configuration pour éviter que le clic droit ajoute un point rouge sur la carte
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Variables globales pour le dessin du sable sur la carte
last_x = 0 # dernière position en x utilisée pour dessiner le sable
last_y = 0 # dernière position en y utilisée pour dessiner le sable
n_points = 0 # nombre total de points dans le dernier dessin
length = 0 # longueur du dernier dessin

# Initialisation de l'IA, appelée "cerveau", qui contient le réseau de neurones
brain = Dqn(5, 3, 0.9) # 5 capteurs, 3 actions, gamma = 0.9
action2rotation = [0, 20, -20] # actions : 0 = pas de rotation, 1 = rotation de 20°, 2 = rotation de -20°
last_reward = 0 # dernière récompense reçue
scores = [] # courbe des scores moyens en fonction du temps

# Initialisation de la carte
first_update = True # flag pour initialiser la carte une seule fois
def init():
    global sand # tableau représentant le sable sur la carte (1 = sable, 0 = pas de sable)
    global goal_x # coordonnée x de l'objectif (par exemple, aéroport ou centre-ville)
    global goal_y # coordonnée y de l'objectif
    sand = np.zeros((longueur, largeur)) # initialisation de la carte sans sable
    goal_x = 20 # position x de l'objectif (près du coin supérieur gauche)
    goal_y = largeur - 20 # position y de l'objectif (près du coin supérieur gauche)
    first_update = False # on désactive l'initialisation unique

# Initialisation de la dernière distance (distance entre la voiture et l'objectif)
last_distance = 0

# Classe pour créer et gérer la voiture
class Car(Widget):

    angle = NumericProperty(0) # angle de la voiture par rapport à l'axe x de la carte
    rotation = NumericProperty(0) # rotation appliquée sur la voiture
    velocity_x = NumericProperty(0) # coordonnée x de la vitesse de la voiture
    velocity_y = NumericProperty(0) # coordonnée y de la vitesse de la voiture
    velocity = ReferenceListProperty(velocity_x, velocity_y) # vecteur vitesse
    sensor1_x = NumericProperty(0) # position x du premier capteur (avant de la voiture)
    sensor1_y = NumericProperty(0) # position y du premier capteur
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y) # vecteur du premier capteur
    sensor2_x = NumericProperty(0) # position x du second capteur (à 30° à gauche)
    sensor2_y = NumericProperty(0) # position y du second capteur
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y) # vecteur du second capteur
    sensor3_x = NumericProperty(0) # position x du troisième capteur (à 30° à droite)
    sensor3_y = NumericProperty(0) # position y du troisième capteur
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y) # vecteur du troisième capteur
    signal1 = NumericProperty(0) # signal reçu par le premier capteur
    signal2 = NumericProperty(0) # signal reçu par le second capteur
    signal3 = NumericProperty(0) # signal reçu par le troisième capteur

    def move(self, rotation):
        # Mise à jour de la position et de l'orientation de la voiture
        self.pos = Vector(*self.velocity) + self.pos # position mise à jour avec la vitesse
        self.rotation = rotation # mise à jour de la rotation
        self.angle = self.angle + self.rotation # mise à jour de l'angle
        # Mise à jour des positions des capteurs après rotation
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos 
        self.sensor2 = Vector(30, 0).rotate((self.angle+30)%360) + self.pos 
        self.sensor3 = Vector(30, 0).rotate((self.angle-30)%360) + self.pos 
        # Lecture des signaux de sable captés par chaque capteur
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-10:int(self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-10:int(self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-10:int(self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.
        # Détection des bords de la carte pour chaque capteur
        if self.sensor1_x > longueur-10 or self.sensor1_x<10 or self.sensor1_y>largeur-10 or self.sensor1_y<10:
            self.signal1 = 1. # capteur 1 détecte plein de sable
        if self.sensor2_x > longueur-10 or self.sensor2_x<10 or self.sensor2_y>largeur-10 or self.sensor2_y<10:
            self.signal2 = 1. # capteur 2 détecte plein de sable
        if self.sensor3_x > longueur-10 or self.sensor3_x<10 or self.sensor3_y>largeur-10 or self.sensor3_y<10:
            self.signal3 = 1. # capteur 3 détecte plein de sable

# Création des capteurs en tant que classes
class Ball1(Widget): 
    pass
class Ball2(Widget): 
    pass
class Ball3(Widget): 
    pass

# Classe principale du jeu
class Game(Widget):

    car = ObjectProperty(None) # obtention de la voiture
    ball1 = ObjectProperty(None) # obtention du capteur 1
    ball2 = ObjectProperty(None) # obtention du capteur 2
    ball3 = ObjectProperty(None) # obtention du capteur 3

    def serve_car(self): # initialisation de la voiture au centre
        self.car.center = self.center # positionnement de la voiture au centre de la carte
        self.car.velocity = Vector(6, 0) # vitesse initiale de la voiture (6 unités vers la droite)

    def update(self, dt): # fonction d'actualisation principale

        global brain, last_reward, scores, last_distance, goal_x, goal_y, longueur, largeur

        longueur = self.width # largeur de la carte
        largeur = self.height # hauteur de la carte
        if first_update: # initialisation unique de la carte
            init()

        xx = goal_x - self.car.x # différence en x entre objectif et voiture
        yy = goal_y - self.car.y # différence en y entre objectif et voiture
        orientation = Vector(*self.car.velocity).angle((xx,yy))/180. # direction par rapport à l'objectif
        last_signal = [self.car.signal1, self.car.signal2, self.car.signal3, orientation, -orientation] # vecteur d'état d'entrée pour l'IA
        action = brain.update(last_reward, last_signal) # action déterminée par l'IA
        scores.append(brain.score()) # ajout du score (moyenne des récompenses récentes)
        rotation = action2rotation[action] # conversion de l'action en rotation
        self.car.move(rotation) # déplacement de la voiture
        distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2) # calcul de la distance à l'objectif
        self.ball1.pos = self.car.sensor1 # mise à jour de la position du capteur 1
        self.ball2.pos = self.car.sensor2 # mise à jour de la position du capteur 2
        self.ball3.pos = self.car.sensor3 # mise à jour de la position du capteur 3

        if sand[int(self.car.x),int(self.car.y)] > 0: # détection de sable
            self.car.velocity = Vector(1, 0).rotate(self.car.angle) # ralentissement de la voiture
            last_reward = -1 # pénalité pour sable
        else: # sol normal
            self.car.velocity = Vector(6, 0).rotate(self.car.angle) # vitesse normale
            last_reward = -0.2 # légère pénalité pour éloignement
            if distance < last_distance: # si la voiture se rapproche de l'objectif
                last_reward = 0.1 # récompense positive

        # Détection des limites de la carte pour la voiture
        if self.car.x < 10: 
            self.car.x = 10
            last_reward = -1
        if self.car.x > self.width-10: 
            self.car.x = self.width-10
            last_reward = -1
        if self.car.y < 10: 
            self.car.y = 10
            last_reward = -1
        if self.car.y > self.height-10: 
            self.car.y = self.height-10
            last_reward = -1

        if distance < 100: # si la voiture atteint l'objectif
            goal_x = self.width - goal_x # l'objectif devient l'autre coin de la carte
            goal_y = self.height - goal_y 

        # Mise à jour de la dernière distance
        last_distance = distance

# Classe pour dessiner le sable dans l'interface graphique
class MyPaintWidget(Widget):

    def on_touch_down(self, touch): # dessin de sable avec un clic
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8, 0.7, 0)
            d = 10.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            sand[int(touch.x), int(touch.y)] = 1

    def on_touch_move(self, touch): # dessin de sable en déplaçant la souris
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - last_x)**2 + (y - last_y)**2, 2))
            n_points += 1.
            density = n_points / (length)
            touch.ud['line'].width = int(20 * density + 1)
            sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1
            last_x = x
            last_y = y

# Classe de l'application principale avec boutons de contrôle
class CarApp(App):

    def build(self): # construction de l'application
        parent = Game()
        parent.serve_car()
        Clock.schedule_interval(parent.update, 1.0 / 60.0) # rafraîchissement de l'application toutes les 60 ms
        self.painter = MyPaintWidget() # widget pour dessiner le sable
        clearbtn = Button(text='clear')
        savebtn = Button(text='save', pos=(parent.width, 0))
        loadbtn = Button(text='load', pos=(2 * parent.width, 0))
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        return parent

    def clear_canvas(self, obj): # effacer la carte
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((longueur, largeur))

    def save(self, obj): # sauvegarder l'IA
        print("saving brain...")
        brain.save()
        plt.plot(scores)
        plt.show()

    def load(self, obj): # charger l'IA sauvegardée
        print("loading last saved brain...")
        brain.load()

# Exécution de l'application
if __name__ == '__main__':
    CarApp().run()
