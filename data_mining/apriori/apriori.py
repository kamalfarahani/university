from typing import List, FrozenSet
from transaction_manager import TransactionManager, get_transactions


FrequentItems = FrozenSet[FrozenSet]


def apriori(
    min_support: int, 
    transactionManager: TransactionManager, 
    freq_items: List[FrequentItems] = []) -> List[FrequentItems]:
    
    if freq_items == [] :
        unique_items = transactionManager.get_unique_items()
        first_set_items = [frozenset([frozenset([i]) for i in unique_items])]
        
        return apriori(
            min_support, transactionManager, first_set_items)
    
    sup_validator = lambda tx: transactionManager.get_support_count(tx) >= min_support
    next_freq_items = make_next_freq_items(freq_items[-1], sup_validator)
    if next_freq_items == frozenset() :
        return freq_items
    
    new_freq_items = freq_items + [next_freq_items]
    return apriori(min_support, transactionManager, new_freq_items)


def make_next_freq_items(nth_freq_items: FrequentItems, sup_validator) -> FrequentItems: 
    item = next(iter(nth_freq_items))

    next_freq_items = frozenset(filter(
        lambda s: (len(s) == len(item) + 1) and sup_validator(s), 
        [(item | i) for i in nth_freq_items]))

    if len(nth_freq_items) <= 2:
        return next_freq_items

    return (next_freq_items | 
        make_next_freq_items(
            remove_item_from_frozen_set(nth_freq_items, item), 
            sup_validator))


def remove_item_from_frozen_set(fs: FrozenSet, item) -> FrozenSet:
    return frozenset(
        filter(
            lambda i: i != item, list(fs)))


def print_freq_items(freq_items: List[FrequentItems]):
    for i in range(len(freq_items)):
        print(freq_items[i], '\n__________\n')

def main():
    txs = get_transactions()
    tx_manager = TransactionManager(txs)
    
    sup: int = int(input('Enter min support: '))
    freq_items = apriori(sup, tx_manager)
    print_freq_items(freq_items)



if __name__ == '__main__':
    main()