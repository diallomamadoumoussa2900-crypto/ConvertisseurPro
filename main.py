from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast
import os


class Accueil(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = MDBoxLayout(
            orientation="vertical",
            padding=40,
            spacing=30
        )

        box.add_widget(MDLabel(
            text="💱\nConvertisseur Pro",
            halign="center",
            font_style="H3"
        ))

        btn = MDRaisedButton(
            text="COMMENCER",
            pos_hint={"center_x":0.5}
        )

        btn.bind(on_press=self.start)

        box.add_widget(btn)
        self.add_widget(box)


    def start(self, instance):
        self.manager.current = "convertisseur"



class Convertisseur(MDScreen):

    def on_enter(self):

        if hasattr(self, "deja"):
            return

        self.deja = True

        self.taux = {
            "Euro → GNF": 9500,
            "Dollar → GNF": 8700,
            "GNF → Euro": 1/9500,
            "GNF → Dollar": 1/8700
        }

        self.fichier = "historique.txt"

        if os.path.exists(self.fichier):
            with open(self.fichier,"r",encoding="utf-8") as f:
                self.historique = f.read().splitlines()
        else:
            self.historique = []


        page = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )


        page.add_widget(MDLabel(
            text="Convertisseur Pro",
            halign="center",
            font_style="H4"
        ))


        self.montant = MDTextField(
            hint_text="Entrer le montant",
            input_filter="float"
        )


        self.choix = MDRaisedButton(
            text="Choisir conversion",
            pos_hint={"center_x":0.5}
        )

        self.choix.bind(
            on_release=self.menu
        )


        convertir = MDRaisedButton(
            text="CONVERTIR",
            pos_hint={"center_x":0.5}
        )

        convertir.bind(
            on_press=self.convertir
        )


        effacer = MDRaisedButton(
            text="Effacer montant",
            pos_hint={"center_x":0.5}
        )

        effacer.bind(
            on_press=self.effacer_montant
        )


        copier = MDRaisedButton(
            text="Copier résultat",
            pos_hint={"center_x":0.5}
        )

        copier.bind(
            on_press=self.copier
        )


        self.resultat = MDLabel(
            text="Résultat ici",
            halign="center"
        )


        self.histo = MDLabel(
            text=self.afficher(),
            halign="center"
        )


        page.add_widget(self.montant)
        page.add_widget(self.choix)
        page.add_widget(convertir)
        page.add_widget(effacer)
        page.add_widget(copier)
        page.add_widget(self.resultat)
        page.add_widget(self.histo)

        self.add_widget(page)



    def menu(self, instance):

        items=[]

        for m in self.taux:
            items.append({
                "text":m,
                "viewclass":"OneLineListItem",
                "on_release":lambda x=m:self.selection(x)
            })


        self.menu_obj=MDDropdownMenu(
            caller=self.choix,
            items=items,
            width_mult=4
        )

        self.menu_obj.open()



    def selection(self, choix):

        self.choix.text=choix
        self.menu_obj.dismiss()



    def convertir(self, instance):

        try:

            valeur=float(self.montant.text)

            resultat=valeur*self.taux[self.choix.text]

            texte=f"{valeur} {self.choix.text} = {round(resultat,2)}"

            self.resultat.text="✅ "+texte

            self.historique.append(texte)

            with open(self.fichier,"w",encoding="utf-8") as f:
                f.write("\n".join(self.historique))

            self.histo.text=self.afficher()

            toast("Conversion réussie")

        except:

            toast("Choisis une conversion")



    def effacer_montant(self, instance):

        self.montant.text=""



    def copier(self, instance):

        MDApp.get_running_app().clipboard.copy(
            self.resultat.text
        )

        toast("Résultat copié")



    def afficher(self):

        if self.historique:
            return "\n".join(self.historique[-5:])

        return "Historique vide"



class Application(MDApp):

    def build(self):

        sm=MDScreenManager()

        sm.add_widget(
            Accueil(name="accueil")
        )

        sm.add_widget(
            Convertisseur(name="convertisseur")
        )

        return sm



Application().run()
