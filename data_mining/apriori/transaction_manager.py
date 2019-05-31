from typing import List, Set
from functools import reduce

class TransactionManager:

    def __init__(self, transactions: List[Set]):
        self.transactions = transactions
    
    def get_unique_items(self) -> List:
        return list(reduce(
            lambda acc, tx: acc | tx, 
            self.transactions))
        
    
    def get_support_count(self, tx: Set) -> int:
        return reduce(
            lambda acc, t: 1 + acc if tx.issubset(t) else acc,
            self.transactions,
            0)


def get_transactions() -> List[Set]:
    tx_number = int(input('Enter transactions number: '))
    input_msg = 'Enter transaction {}-th: '
    
    return [
        set(input(input_msg.format(i + 1)).split(',')) for i in range(tx_number)
    ]    
    
