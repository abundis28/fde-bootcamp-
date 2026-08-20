# Design Smells from TransactionProcessor Class

## Single Responsibility Principle

The TransactionProcessor class does 6 different actions: validate, compute fee, compute tax set-aside, persist the transaction, format output for the caller and notify through chosen channel.
I would create different classes for those that should not be grouped.

## Open/Closed Principle

All 6 behaviors use if/elif statements to decide which behavior to use. This will add complexity when new costumer tiers, output formats and notification channels are added.
I would use the Strategy design pattern.

## Dependency inversion

This application level code is creating its own concrete instances for db and email service. To use unit tests would be impossible because it is directly modifying the db.
I would use the dependency injection design pattern to avoid relying directly on the db class/methods.

## Interface Segregation Principle

The process interface specifies all the parameters and forces every caller to specify all the data even if is not in their interest.
I 