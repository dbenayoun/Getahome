"""
Budget Simulator - Calculateur de frais d'acquisition immobilière en Israël
Basé sur simalator_rules.txt

Module simple et réutilisable pour calculer tous les frais associés à une acquisition immobilière.
"""


class BudgetSimulator:
    """
    Calcule tous les frais d'acquisition immobilière en Israël
    selon les règles fiscales en vigueur.
    """
    
    # Constantes
    TVA = 0.18  # 18%
    
    # Grilles de taxation Mas Rechisha
    # Format: [(min, max, taux), ...]
    
    # Résidence principale - Non Olé Hadach
    GRILLE_RESIDENCE_NON_OLE = [
        (0, 1919155, 0.00),
        (1919155, 2276360, 0.035),
        (2276360, 5872725, 0.05),
        (5872725, 19575755, 0.08),
        (19575755, float('inf'), 0.10)
    ]
    
    # Résidence principale - Olé Hadach
    GRILLE_RESIDENCE_OLE = [
        (0, 1978745, 0.00),
        (1978745, 5872725, 0.005),
        (5872725, 19575755, 0.05),
        (19575755, float('inf'), 0.08)
    ]
    
    # Investissement / 2e bien
    GRILLE_INVESTISSEMENT = [
        (0, 5872725, 0.08),
        (5872725, float('inf'), 0.10)
    ]
    
    @staticmethod
    def calculate_mas_rechisha(prix_achat, type_achat='residence', is_ole_hadach=False):
        """
        Calcule la taxe d'acquisition (Mas Rechisha) par tranches progressives.
        
        Args:
            prix_achat (float): Prix d'achat en ILS
            type_achat (str): 'residence' ou 'investissement'
            is_ole_hadach (bool): Statut Olé Hadach (seulement si type_achat='residence')
            
        Returns:
            float: Montant de la taxe d'acquisition
        """
        # Sélection de la grille appropriée
        if type_achat == 'investissement':
            grille = BudgetSimulator.GRILLE_INVESTISSEMENT
        elif is_ole_hadach:
            grille = BudgetSimulator.GRILLE_RESIDENCE_OLE
        else:
            grille = BudgetSimulator.GRILLE_RESIDENCE_NON_OLE
        
        total_tax = 0
        
        for min_val, max_val, taux in grille:
            if prix_achat <= min_val:
                break
            
            # Calculer la portion du prix dans cette tranche
            montant_tranche = min(prix_achat, max_val) - min_val
            
            if montant_tranche > 0:
                total_tax += montant_tranche * taux
        
        return total_tax
    
    @staticmethod
    def calculate_agent_fee(prix_achat, avec_agent=True):
        """
        Calcule la commission de l'agent immobilier.
        
        Args:
            prix_achat (float): Prix d'achat en ILS
            avec_agent (bool): Utilisation d'un agent
            
        Returns:
            float: Commission TTC (0 si pas d'agent)
        """
        if not avec_agent:
            return 0
        
        commission_ht = prix_achat * 0.02  # 2% HT
        commission_ttc = commission_ht * (1 + BudgetSimulator.TVA)
        return commission_ttc
    
    @staticmethod
    def calculate_lawyer_fee(prix_achat, achat_neuf=False):
        """
        Calcule les frais d'avocat.
        
        Args:
            prix_achat (float): Prix d'achat en ILS
            achat_neuf (bool): Achat neuf auprès d'un promoteur (kablan)
            
        Returns:
            float: Frais d'avocat TTC
        """
        # Avocat acheteur : 1% HT
        avocat_ht = prix_achat * 0.01
        avocat_ttc = avocat_ht * (1 + BudgetSimulator.TVA)
        
        # Si achat neuf, ajouter avocat promoteur : 0.5% HT
        if achat_neuf:
            avocat_kablan_ht = prix_achat * 0.005
            avocat_kablan_ttc = avocat_kablan_ht * (1 + BudgetSimulator.TVA)
            return avocat_ttc + avocat_kablan_ttc
        
        return avocat_ttc
    
    @staticmethod
    def calculate_shammai_fee(montant_forfaitaire=3_500):
        """
        Frais du Shammai (expert immobilier).
        
        Args:
            montant_forfaitaire (float): Montant forfaitaire (défaut: 3,500 ILS)
            
        Returns:
            float: Frais du Shammai
        """
        return montant_forfaitaire
    
    @staticmethod
    def calculate_broker_fee(montant_pret, avec_courtier=False):
        """
        Calcule la commission du courtier en crédit.
        
        Args:
            montant_pret (float): Montant du prêt en ILS
            avec_courtier (bool): Utilisation d'un courtier
            
        Returns:
            float: Commission TTC (0 si pas de courtier ou pas de prêt)
        """
        if not avec_courtier or montant_pret == 0:
            return 0
        
        commission_ht = montant_pret * 0.01  # 1% HT du montant du prêt
        commission_ttc = commission_ht * (1 + BudgetSimulator.TVA)
        return commission_ttc
    
    @staticmethod
    def calculate_cadastre_fees():
        """
        Frais de cadastre / enregistrement (Tabu, Minhal, etc.).
        
        Returns:
            float: Frais forfaitaires
        """
        return 1_500
    
    @staticmethod
    def calculate_bank_dossier_fee(montant_pret):
        """
        Calcule les frais de dossier bancaire.
        
        Args:
            montant_pret (float): Montant du prêt en ILS
            
        Returns:
            float: Frais de dossier (0 si pas de prêt)
        """
        if montant_pret == 0:
            return 0
        
        return montant_pret * 0.0035  # 0.35% du prêt
    
    @staticmethod
    def calculate_hypotheque_fee(montant_pret):
        """
        Calcule les frais d'enregistrement de l'hypothèque.
        
        Args:
            montant_pret (float): Montant du prêt en ILS
            
        Returns:
            float: Frais d'enregistrement (0 si pas de prêt)
        """
        if montant_pret == 0:
            return 0
        
        return 1_500
    
    @staticmethod
    def calculate_translation_fees(avec_traductions=True):
        """
        Frais de traductions / notaire / procuration.
        
        Args:
            avec_traductions (bool): Nécessite des traductions
            
        Returns:
            float: Frais forfaitaires (0 si non nécessaire)
        """
        return 500 if avec_traductions else 0
    
    @staticmethod
    def calculate_fx_fees(montant_transfert, taux_fx=0.005):
        """
        Frais de change / transferts internationaux.
        
        Args:
            montant_transfert (float): Montant transféré depuis l'étranger
            taux_fx (float): Taux de frais (défaut: 0.5%)
            
        Returns:
            float: Frais de change (0 si pas de transfert)
        """
        if montant_transfert == 0:
            return 0
        
        return montant_transfert * taux_fx
    
    @staticmethod
    def calculate_all_fees(prix_achat,
                          type_achat='residence',
                          is_ole_hadach=False,
                          apport_pourcent=0.30,
                          avec_agent=True,
                          achat_neuf=False,
                          shammai_montant=3_500,
                          avec_courtier=False,
                          avec_traductions=True,
                          montant_transfert_fx=0,
                          taux_eur_ils=None):
        """
        Calcule tous les frais d'acquisition et retourne un dictionnaire complet.
        
        Args:
            prix_achat (float): Prix d'achat en ILS
            type_achat (str): 'residence' ou 'investissement'
            is_ole_hadach (bool): Statut Olé Hadach
            apport_pourcent (float): Pourcentage d'apport (ex: 0.30 pour 30%)
            avec_agent (bool): Utilise un agent immobilier
            achat_neuf (bool): Achat neuf (kablan)
            shammai_montant (float): Montant forfaitaire Shammai
            avec_courtier (bool): Utilise un courtier en crédit
            avec_traductions (bool): Nécessite traductions
            montant_transfert_fx (float): Montant des transferts internationaux
            taux_eur_ils (float): Taux EUR/ILS pour conversion (optionnel)
            
        Returns:
            dict: Dictionnaire complet avec tous les calculs
        """
        # Calcul du prêt et de l'apport
        montant_pret = prix_achat * (1 - apport_pourcent)
        apport = prix_achat * apport_pourcent
        
        # Calcul de chaque frais
        mas_rechisha = BudgetSimulator.calculate_mas_rechisha(
            prix_achat, type_achat, is_ole_hadach
        )
        
        frais_agent = BudgetSimulator.calculate_agent_fee(prix_achat, avec_agent)
        frais_avocat = BudgetSimulator.calculate_lawyer_fee(prix_achat, achat_neuf)
        frais_shammai = BudgetSimulator.calculate_shammai_fee(shammai_montant)
        frais_courtier = BudgetSimulator.calculate_broker_fee(montant_pret, avec_courtier)
        frais_cadastre = BudgetSimulator.calculate_cadastre_fees()
        frais_dossier = BudgetSimulator.calculate_bank_dossier_fee(montant_pret)
        frais_hypotheque = BudgetSimulator.calculate_hypotheque_fee(montant_pret)
        frais_traductions = BudgetSimulator.calculate_translation_fees(avec_traductions)
        frais_fx = BudgetSimulator.calculate_fx_fees(montant_transfert_fx)
        
        # Total des frais
        total_frais = (
            mas_rechisha +
            frais_agent +
            frais_avocat +
            frais_shammai +
            frais_courtier +
            frais_cadastre +
            frais_dossier +
            frais_hypotheque +
            frais_traductions +
            frais_fx
        )
        
        # Budget total et cash nécessaire
        budget_total = prix_achat + total_frais
        cash_necessaire = apport + total_frais
        
        # Comparaison Olé Hadach (seulement si résidence principale)
        comparaison_ole = None
        if type_achat == 'residence':
            mas_non_ole = BudgetSimulator.calculate_mas_rechisha(
                prix_achat, 'residence', False
            )
            mas_ole = BudgetSimulator.calculate_mas_rechisha(
                prix_achat, 'residence', True
            )
            economie = mas_non_ole - mas_ole
            
            comparaison_ole = {
                'mas_rechisha_non_ole': mas_non_ole,
                'mas_rechisha_ole': mas_ole,
                'economie': economie
            }
        
        # Construction du résultat
        resultat = {
            'prix_achat': prix_achat,
            'type_achat': type_achat,
            'achat_neuf': achat_neuf,
            'is_ole_hadach': is_ole_hadach,
            'apport': apport,
            'apport_pourcent': apport_pourcent * 100,
            'montant_pret': montant_pret,
            'frais_detail': {
                'mas_rechisha': mas_rechisha,
                'agent': frais_agent,
                'avocat': frais_avocat,
                'shammai': frais_shammai,
                'courtier': frais_courtier,
                'cadastre': frais_cadastre,
                'dossier_banque': frais_dossier,
                'hypotheque': frais_hypotheque,
                'traductions': frais_traductions,
                'change_fx': frais_fx
            },
            'total_frais': total_frais,
            'frais_pourcent': (total_frais / prix_achat) * 100,
            'budget_total': budget_total,
            'cash_necessaire': cash_necessaire,
            'comparaison_ole': comparaison_ole
        }
        
        # Ajout de la conversion EUR si taux fourni
        if taux_eur_ils:
            resultat['conversion_eur'] = {
                'prix_achat': prix_achat / taux_eur_ils,
                'total_frais': total_frais / taux_eur_ils,
                'budget_total': budget_total / taux_eur_ils,
                'cash_necessaire': cash_necessaire / taux_eur_ils,
                'taux': taux_eur_ils
            }
        
        return resultat
    
    @staticmethod
    def format_currency(montant, devise='ILS'):
        """
        Formate un montant en devise.
        
        Args:
            montant (float): Montant à formater
            devise (str): 'ILS' ou 'EUR'
            
        Returns:
            str: Montant formaté
        """
        symbole = '₪' if devise == 'ILS' else '€'
        return f"{symbole}{montant:,.0f}"
    
    @staticmethod
    def print_summary(resultat):
        """
        Affiche un résumé formaté des calculs.
        
        Args:
            resultat (dict): Dictionnaire retourné par calculate_all_fees()
        """
        print("\n" + "="*70)
        print("SIMULATEUR DE BUDGET TOTAL - ACHAT IMMOBILIER EN ISRAËL")
        print("="*70)
        
        # Prix d'achat
        print(f"\n📍 PRIX D'ACHAT: {BudgetSimulator.format_currency(resultat['prix_achat'])}")
        if 'conversion_eur' in resultat:
            print(f"              {BudgetSimulator.format_currency(resultat['conversion_eur']['prix_achat'], 'EUR')}")
        
        # Type d'achat
        print(f"\n🏢 TYPE D'ACHAT:")
        type_bien = "Résidence principale" if resultat['type_achat'] == 'residence' else "Investissement / 2e bien"
        print(f"   Nature du bien: {type_bien}")
        print(f"   État du bien: {'Neuf (promoteur)' if resultat['achat_neuf'] else 'Ancien (particulier)'}")
        if resultat['type_achat'] == 'residence':
            statut_ole = "Oui ✅" if resultat['is_ole_hadach'] else "Non"
            print(f"   Statut Olé Hadach: {statut_ole}")
        
        # Financement
        print(f"\n💰 FINANCEMENT:")
        print(f"   Apport: {BudgetSimulator.format_currency(resultat['apport'])} ({resultat['apport_pourcent']:.0f}%)")
        print(f"   Prêt:   {BudgetSimulator.format_currency(resultat['montant_pret'])} ({100-resultat['apport_pourcent']:.0f}%)")
        
        # Détail des frais
        print(f"\n📋 DÉTAIL DES FRAIS:")
        frais = resultat['frais_detail']
        
        print(f"   Taxe d'acquisition (Mas Rechisha): {BudgetSimulator.format_currency(frais['mas_rechisha'])}")
        
        if frais['agent'] > 0:
            print(f"   Agent immobilier (2% TTC):         {BudgetSimulator.format_currency(frais['agent'])}")
        
        print(f"   Avocat:                             {BudgetSimulator.format_currency(frais['avocat'])}")
        
        if frais['shammai'] > 0:
            print(f"   Shammai (expert):                   {BudgetSimulator.format_currency(frais['shammai'])}")
        
        if frais['courtier'] > 0:
            print(f"   Courtier crédit (1% TTC):           {BudgetSimulator.format_currency(frais['courtier'])}")
        
        print(f"   Cadastre / Enregistrement:          {BudgetSimulator.format_currency(frais['cadastre'])}")
        
        if frais['dossier_banque'] > 0:
            print(f"   Frais dossier bancaire:             {BudgetSimulator.format_currency(frais['dossier_banque'])}")
        
        if frais['hypotheque'] > 0:
            print(f"   Enregistrement hypothèque:          {BudgetSimulator.format_currency(frais['hypotheque'])}")
        
        if frais['traductions'] > 0:
            print(f"   Traductions / Notaire:              {BudgetSimulator.format_currency(frais['traductions'])}")
        
        if frais['change_fx'] > 0:
            print(f"   Frais de change:                    {BudgetSimulator.format_currency(frais['change_fx'])}")
        
        # Total des frais
        print(f"\n💵 TOTAL DES FRAIS: {BudgetSimulator.format_currency(resultat['total_frais'])}")
        print(f"   ({resultat['frais_pourcent']:.1f}% du prix d'achat)")
        if 'conversion_eur' in resultat:
            print(f"                    {BudgetSimulator.format_currency(resultat['conversion_eur']['total_frais'], 'EUR')}")
        
        # Budget total
        print(f"\n🏠 BUDGET TOTAL DU PROJET: {BudgetSimulator.format_currency(resultat['budget_total'])}")
        if 'conversion_eur' in resultat:
            print(f"                           {BudgetSimulator.format_currency(resultat['conversion_eur']['budget_total'], 'EUR')}")
        
        # Cash nécessaire
        print(f"\n💸 CASH NÉCESSAIRE: {BudgetSimulator.format_currency(resultat['cash_necessaire'])}")
        if 'conversion_eur' in resultat:
            print(f"                    {BudgetSimulator.format_currency(resultat['conversion_eur']['cash_necessaire'], 'EUR')}")
        
        # Comparaison Olé
        if resultat['comparaison_ole']:
            comp = resultat['comparaison_ole']
            print(f"\n🎯 COMPARAISON OLÉ HADACH:")
            print(f"   Sans statut Olé: {BudgetSimulator.format_currency(comp['mas_rechisha_non_ole'])}")
            print(f"   Avec statut Olé: {BudgetSimulator.format_currency(comp['mas_rechisha_ole'])}")
            print(f"   💡 ÉCONOMIE: {BudgetSimulator.format_currency(comp['economie'])}")
        
        print("\n" + "="*70)
        print("⚠️  Cette estimation est indicative et ne remplace pas")
        print("   un conseil juridique ou fiscal personnalisé.")
        print("="*70 + "\n")


# ==============================================================================
# EXEMPLE D'UTILISATION
# ==============================================================================

if __name__ == "__main__":
    # Exemple 1: Résidence principale - Non Olé
    print("\n🏡 EXEMPLE 1: Résidence principale - Tel Aviv 4 pièces")
    print("-" * 70)
    
    resultat1 = BudgetSimulator.calculate_all_fees(
        prix_achat=4_020_000,
        type_achat='residence',
        is_ole_hadach=False,
        apport_pourcent=0.30,
        avec_agent=True,
        achat_neuf=False,
        avec_courtier=True,
        avec_traductions=True,
        taux_eur_ils=3.85
    )
    
    BudgetSimulator.print_summary(resultat1)
    
    
    # Exemple 2: Résidence principale - Olé Hadach
    print("\n🏡 EXEMPLE 2: Résidence principale - Olé Hadach")
    print("-" * 70)
    
    resultat2 = BudgetSimulator.calculate_all_fees(
        prix_achat=4_020_000,
        type_achat='residence',
        is_ole_hadach=True,
        apport_pourcent=0.30,
        avec_agent=True,
        avec_courtier=True,
        taux_eur_ils=3.85
    )
    
    BudgetSimulator.print_summary(resultat2)
    
    
    # Exemple 3: Investissement
    print("\n🏡 EXEMPLE 3: Investissement / 2e bien")
    print("-" * 70)
    
    resultat3 = BudgetSimulator.calculate_all_fees(
        prix_achat=3_000_000,
        type_achat='investissement',
        apport_pourcent=0.40,
        avec_agent=False,
        avec_courtier=False,
        avec_traductions=False,
        taux_eur_ils=3.85
    )
    
    BudgetSimulator.print_summary(resultat3)
