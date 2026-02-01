class CompteBancaire :
    def __init__ (self, titulaire, solde=1000) :
        self.titulaire = titulaire
        self.solde = solde
    def deposer(self, montant_plus) : 
        self.solde = self.solde + montant_plus
    def retirer(self, montant_moins) : 
        if montant_moins > self.solde :
            print("Vous n'avez pas assez d'argent")
        else :
            self.solde = self.solde - montant_moins
    def afficher_solde(self) :
        print(f"Le solde du compte de {self.titulaire} est de {self.solde} CHF.")
    def transactions(self, montant_echange, compte_recevant) :
       if montant_echange > self.solde :
           print("Transaction impossible car le solde est insufisant")
       else : 
           self.retirer(montant_echange)
           compte_recevant.deposer(montant_echange)
           print("Transaction réussie")

class Banque :
    def __init__(self,nom) :
        self.nom = nom
        self.liste_compte = []
    def ajouter(self, compte) : 
        for i in self.liste_compte :
            if i.titulaire == compte.titulaire :
                print("Ce compte est déjà dans la base de donnée.")
                return
        self.liste_compte.append(compte)
    def afficher(self) :
        for i in self.liste_compte :
            print(f"{i.titulaire} : {i.solde} CHF")
    def trouver_compte(self, titulaire) :
        for i in self.liste_compte :
            if i.titulaire == titulaire :
                return i
        return None
    def transfert (self, nom1, nom2, montant) :
        c1 = self.trouver_compte(nom1)
        c2 = self.trouver_compte(nom2)
        if not c1 or not c2 :
            print("L'un des comptes n'existe pas, transfert impossible")
            return
        c1.transactions(montant,c2)
    def transfert_inter(self, titulaire1, titulaire2, autre_banque, montant):
        c1 = self.trouver_compte(titulaire1)
        c2 = autre_banque.trouver_compte(titulaire2)

        if not c1 :
            print(f"Le compte de {titulaire1} n'existe pas chez {self.nom}")
            return
        if not c2 : 
            print(f"Le compte de {titulaire2} n'existe pas chez {autre_banque.nom}")
            return
        if montant>c1.solde :
            print(f"{titulaire1} n'a pas assez d'argent. Transfert non validé.")
            return
        c1.retirer(montant)
        c2.deposer(montant)
        print(f"Transfert de {montant} CHF réussi du compte de {titulaire1} au compte de {titulaire2}.")
        
compte1 = CompteBancaire("Joachim Ischi")
compte2 = CompteBancaire("Gabriel Perez")
compte3 = CompteBancaire("Alice Ischi")
compte4 = CompteBancaire("Jessica Krueger")
compte5 = CompteBancaire("Yann Ischi")
ubs = Banque("ubs")
credit_suisse = Banque("crédit suisse")
credit_suisse.ajouter(compte3)
credit_suisse.ajouter(compte4)
ubs.ajouter(compte5)
ubs.ajouter(compte1)
ubs.ajouter(compte2)
ubs.transfert_inter("Joachim Ischi", "Jessica Krueger", credit_suisse, 500 )
ubs.afficher()