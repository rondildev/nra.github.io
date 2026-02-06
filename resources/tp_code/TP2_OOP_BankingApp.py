"""
TP 2: Programmation OOP Python - Application Bancaire
EST Guelmim - Programmation Python
Auteur: Nour Eddine AIT ABDALLAH

Objectif: Créer une application bancaire utilisant les principes OOP
(héritage, polymorphisme, encapsulation)
"""

from datetime import datetime
from abc import ABC, abstractmethod
from typing import List

class Account(ABC):
    """Classe abstraite pour les types de comptes"""
    
    _accounts_count = 0  # Variable de classe
    
    def __init__(self, owner: str, initial_balance: float = 0):
        """Initialise un compte bancaire"""
        self.owner = owner
        self._balance = initial_balance
        self._transactions = []
        self.account_number = f"ACC{Account._accounts_count:05d}"
        Account._accounts_count += 1
        
        if initial_balance > 0:
            self._transactions.append(
                Transaction("Dépôt initial", initial_balance, datetime.now())
            )
    
    @property
    def balance(self):
        """Getter pour le solde"""
        return self._balance
    
    @abstractmethod
    def apply_interest(self):
        """Méthode abstraite pour appliquer les intérêts"""
        pass
    
    def deposit(self, amount: float):
        """Effectue un dépôt"""
        if amount <= 0:
            raise ValueError("Le montant doit être positif")
        
        self._balance += amount
        self._transactions.append(
            Transaction("Dépôt", amount, datetime.now())
        )
        print(f"✓ Dépôt de {amount}€ effectué. Nouveau solde: {self._balance}€")
    
    def withdraw(self, amount: float):
        """Effectue un retrait"""
        if amount <= 0:
            raise ValueError("Le montant doit être positif")
        
        if amount > self._balance:
            raise ValueError("Solde insuffisant")
        
        self._balance -= amount
        self._transactions.append(
            Transaction("Retrait", -amount, datetime.now())
        )
        print(f"✓ Retrait de {amount}€ effectué. Nouveau solde: {self._balance}€")
    
    def transfer_to(self, recipient, amount: float):
        """Effectue un virement vers un autre compte"""
        if amount <= 0:
            raise ValueError("Le montant doit être positif")
        
        if amount > self._balance:
            raise ValueError("Solde insuffisant")
        
        self._balance -= amount
        recipient._balance += amount
        
        self._transactions.append(
            Transaction(f"Virement vers {recipient.account_number}", -amount, datetime.now())
        )
        recipient._transactions.append(
            Transaction(f"Virement de {self.account_number}", amount, datetime.now())
        )
        print(f"✓ Virement de {amount}€ vers {recipient.owner} effectué")
    
    def print_statement(self):
        """Affiche l'historique des transactions"""
        print("\n" + "="*50)
        print(f"RELEVÉ DE COMPTE - {self.account_number}")
        print(f"Titulaire: {self.owner}")
        print(f"Solde actuel: {self._balance}€")
        print("="*50)
        print(f"{'Date':<20} {'Description':<25} {'Montant':<10}")
        print("-"*50)
        
        for transaction in self._transactions:
            date_str = transaction.date.strftime("%d/%m/%Y %H:%M")
            print(f"{date_str:<20} {transaction.description:<25} {transaction.amount:>8.2f}€")
        print("-"*50)


class SavingsAccount(Account):
    """Compte épargne avec intérêts"""
    
    INTEREST_RATE = 0.03  # 3% d'intérêts annuels
    
    def __init__(self, owner: str, initial_balance: float = 0):
        super().__init__(owner, initial_balance)
        self.account_type = "Compte Épargne"
    
    def apply_interest(self):
        """Applique les intérêts annuels"""
        interest = self._balance * self.INTEREST_RATE
        self._balance += interest
        self._transactions.append(
            Transaction("Intérêts annuels", interest, datetime.now())
        )
        print(f"✓ Intérêts appliqués: {interest:.2f}€. Nouveau solde: {self._balance}€")
    
    def __str__(self):
        return f"{self.account_type} de {self.owner} - Solde: {self._balance}€"


class CheckingAccount(Account):
    """Compte chèques avec découvert autorisé"""
    
    OVERDRAFT_LIMIT = 500  # Découvert autorisé
    
    def __init__(self, owner: str, initial_balance: float = 0):
        super().__init__(owner, initial_balance)
        self.account_type = "Compte Chèques"
    
    def apply_interest(self):
        """Les comptes chèques n'ont pas d'intérêts"""
        print("ⓘ Les comptes chèques ne génèrent pas d'intérêts")
    
    def withdraw(self, amount: float):
        """Permet un découvert jusqu'à la limite"""
        if amount <= 0:
            raise ValueError("Le montant doit être positif")
        
        if amount > self._balance + self.OVERDRAFT_LIMIT:
            raise ValueError(f"Dépassement de la limite de découvert ({self.OVERDRAFT_LIMIT}€)")
        
        self._balance -= amount
        self._transactions.append(
            Transaction("Retrait", -amount, datetime.now())
        )
        print(f"✓ Retrait de {amount}€ effectué. Nouveau solde: {self._balance}€")
    
    def __str__(self):
        return f"{self.account_type} de {self.owner} - Solde: {self._balance}€"


class Transaction:
    """Représente une transaction bancaire"""
    
    def __init__(self, description: str, amount: float, date: datetime):
        self.description = description
        self.amount = amount
        self.date = date


class Bank:
    """Gère les clients et leurs comptes"""
    
    def __init__(self, name: str):
        self.name = name
        self.accounts: List[Account] = []
    
    def create_savings_account(self, owner: str, initial_balance: float = 0) -> SavingsAccount:
        """Crée un compte épargne"""
        account = SavingsAccount(owner, initial_balance)
        self.accounts.append(account)
        print(f"✓ Compte épargne créé pour {owner} ({account.account_number})")
        return account
    
    def create_checking_account(self, owner: str, initial_balance: float = 0) -> CheckingAccount:
        """Crée un compte chèques"""
        account = CheckingAccount(owner, initial_balance)
        self.accounts.append(account)
        print(f"✓ Compte chèques créé pour {owner} ({account.account_number})")
        return account
    
    def display_all_accounts(self):
        """Affiche tous les comptes"""
        print(f"\n{'='*50}")
        print(f"Clients de {self.name}")
        print("="*50)
        for i, account in enumerate(self.accounts, 1):
            print(f"{i}. {account}")


def main():
    """Démonstration de l'application bancaire"""
    
    print("="*50)
    print("APPLICATION BANCAIRE - OOP Python")
    print("="*50)
    
    # Créer une banque
    bank = Bank("Banque du Maroc")
    
    # Créer des comptes
    print("\n1. Création des comptes...")
    account1 = bank.create_savings_account("Ahmed Ben Ali", 1000)
    account2 = bank.create_checking_account("Fatima Zahra", 500)
    account3 = bank.create_savings_account("Mohamed Karim", 2000)
    
    # Effectuer des opérations
    print("\n2. Opérations bancaires...")
    account1.deposit(500)
    account1.withdraw(200)
    account1.apply_interest()
    
    account2.deposit(300)
    account2.withdraw(600)  # Utilise le découvert autorisé
    
    # Virement entre comptes
    print("\n3. Virements...")
    account1.transfer_to(account2, 300)
    
    # Afficher les relevés
    print("\n4. Relevés de compte...")
    account1.print_statement()
    account2.print_statement()
    
    # Afficher tous les comptes
    bank.display_all_accounts()


if __name__ == "__main__":
    main()
