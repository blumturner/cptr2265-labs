"""
CPTR 2265 - Lab 7, Part A starter: Campus Bookstore Order System
=================================================================

This program runs (try it: `python order_system.py`), but its design is poor.
It violates at least three of the five SOLID principles -- and one of those
violations already causes a crash in the demo at the bottom of the file.

Your tasks (see the Week 7 lab page for full details):
  1. Copy this file to lab07/original/ and annotate it: add a comment such as
         # SOLID VIOLATION (SRP): ...explanation...
     at every place you find a violation. Commit.
  2. Refactor the code (in lab07/refactored/) so it complies with SOLID.
     The program should still produce the same receipts and behavior. Commit.

Hint: look at who is responsible for what, what you would have to edit to add
a new customer type or payment method, whether every subclass can really be
used where its parent is expected, whether every class needs every method it
is forced to implement, and which classes create their own dependencies.
"""

import datetime


# --------------------------------------------------------------------------
# Domain classes
# --------------------------------------------------------------------------

class Item:
    def __init__(self, sku, name, price, quantity):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity


# REFACTOR (OCP): Customer discount rules are separated into classes.
# A new customer type can be added without changing OrderProcessor.
class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def discount(self, subtotal):
        return 0.0


class StudentCustomer(Customer):
    def discount(self, subtotal):
        return subtotal * 0.10


class StaffCustomer(Customer):
    def discount(self, subtotal):
        return subtotal * 0.15


class Order:
    # REFACTOR (OCP): Order now receives customer and payment objects
    # instead of storing types as strings that OrderProcessor must check.
    def __init__(self, order_id, customer, payment_method):
        self.order_id = order_id
        self.customer = customer
        self.payment_method = payment_method
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def subtotal(self):
        return sum(i.price * i.quantity for i in self.items)

    def shipping_cost(self):
        if self.subtotal() >= 50:
            return 0.0
        return 5.99


class DigitalOrder(Order):
    """An order for e-books and access codes. Nothing physical ships."""

    # REFACTOR (LSP): DigitalOrder returns zero shipping instead of
    # raising an exception, so it can safely be used as an Order.
    def shipping_cost(self):
        return 0.0


# --------------------------------------------------------------------------
# Notification
# --------------------------------------------------------------------------

# REFACTOR (ISP): The Notifier interface only requires the operation
# needed to send a notification. It no longer forces every notifier
# to implement unsupported channels such as SMS or push.
class Notifier:
    def send(self, to, subject, body):
        raise NotImplementedError


class EmailNotifier(Notifier):
    def send(self, to, subject, body):
        print(f"[EMAIL to {to}] {subject}")
        print(body)


# --------------------------------------------------------------------------
# Payment
# --------------------------------------------------------------------------

# REFACTOR (OCP): Payment behavior is separated into individual classes.
# New payment methods can be added without modifying OrderProcessor.
class PaymentMethod:
    def pay(self, total):
        raise NotImplementedError


class CardPayment(PaymentMethod):
    def pay(self, total):
        print(f"Charging ${total:.2f} to credit card on file...")
        fee = round(total * 0.029, 2)
        print(f"  Card processing fee recorded: ${fee:.2f}")


class CampusCashPayment(PaymentMethod):
    def pay(self, total):
        print(f"Deducting ${total:.2f} from campus cash account...")


class InvoicePayment(PaymentMethod):
    def pay(self, total):
        print(f"Generating invoice for ${total:.2f}, due in 30 days...")


# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

class TextFileDatabase:
    def __init__(self, filename):
        self.filename = filename

    def save_line(self, line):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# --------------------------------------------------------------------------
# Receipt
# --------------------------------------------------------------------------

# REFACTOR (SRP): Receipt formatting has its own class so OrderProcessor
# does not have to handle receipt formatting itself.
class ReceiptFormatter:
    def format(self, order, subtotal, discount, tax, shipping, total):
        lines = []
        lines.append("=" * 40)
        lines.append("MCTC CAMPUS BOOKSTORE")
        lines.append(f"Order #{order.order_id}   {datetime.date.today()}")
        lines.append(f"Customer: {order.customer.name}")
        lines.append("-" * 40)

        for item in order.items:
            line_total = item.price * item.quantity
            lines.append(
                f"{item.quantity} x {item.name:<26} ${line_total:>8.2f}"
            )

        lines.append("-" * 40)
        lines.append(f"{'Subtotal':<30} ${subtotal:>8.2f}")
        lines.append(f"{'Discount':<29} -${discount:>8.2f}")
        lines.append(f"{'Tax':<30} ${tax:>8.2f}")
        lines.append(f"{'Shipping':<30} ${shipping:>8.2f}")
        lines.append(f"{'TOTAL':<30} ${total:>8.2f}")
        lines.append("=" * 40)

        return "\n".join(lines)

# --------------------------------------------------------------------------
# Order validation
# --------------------------------------------------------------------------

# REFACTOR (SRP): Validation has its own responsibility instead of being
# mixed together with payment, receipts, storage, and notifications.
class OrderValidator:
    def validate(self, order):
        if not order.items:
            print(f"Order {order.order_id} rejected: no items")
            return False

        if "@" not in order.customer.email:
            print(f"Order {order.order_id} rejected: bad email")
            return False

        for item in order.items:
            if item.quantity <= 0 or item.price < 0:
                print(
                    f"Order {order.order_id} rejected: bad item {item.sku}"
                )
                return False

        return True

# --------------------------------------------------------------------------
# The order processor
# --------------------------------------------------------------------------

# REFACTOR (SRP): OrderProcessor now coordinates the order process
# instead of handling every responsibility itself.
class OrderProcessor:

    # REFACTOR (DIP): Dependencies are passed into OrderProcessor
    # instead of being created inside the class.
    def __init__(self, database, notifier, receipt_formatter):
        self.database = database
        self.notifier = notifier
        self.receipt_formatter = receipt_formatter

    def process(self, order):
        # ---- validate ----
        if not order.items:
            print(f"Order {order.order_id} rejected: no items")
            return False

        if "@" not in order.customer.email:
            print(f"Order {order.order_id} rejected: bad email")
            return False

        for item in order.items:
            if item.quantity <= 0 or item.price < 0:
                print(f"Order {order.order_id} rejected: bad item {item.sku}")
                return False

        # ---- discounts ----
        # REFACTOR (OCP): The customer object determines its own discount
        # instead of OrderProcessor using an if/elif chain.
        subtotal = order.subtotal()
        discount = order.customer.discount(subtotal)

        # ---- shipping & tax ----
        shipping = order.shipping_cost()
        tax = round((subtotal - discount) * 0.07875, 2)
        total = round(subtotal - discount + tax + shipping, 2)

        # ---- payment ----
        # REFACTOR (OCP): The payment object handles its own behavior.
        # New payment methods do not require changes to OrderProcessor.
        order.payment_method.pay(total)

        # ---- receipt formatting ----
        # REFACTOR (SRP): ReceiptFormatter handles creating the receipt.
        receipt = self.receipt_formatter.format(
            order,
            subtotal,
            discount,
            tax,
            shipping,
            total
        )

        # ---- persist ----
        self.database.save_line(
            f"{order.order_id}|{order.customer.email}|"
            f"{type(order.payment_method).__name__}|{total:.2f}"
        )

        # ---- notify ----
        # REFACTOR (ISP): The notifier uses the general send() operation.
        self.notifier.send(
            order.customer.email,
            f"Your bookstore order #{order.order_id}",
            receipt
        )

        return True


# --------------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------------

def main():
    # REFACTOR (DIP): Dependencies are created outside OrderProcessor
    # and passed into it.
    processor = OrderProcessor(
        TextFileDatabase("orders.txt"),
        EmailNotifier(),
        ReceiptFormatter()
    )

    order1 = Order(
        1001,
        StudentCustomer("Ana Lopez", "ana@student.mctc.edu"),
        CardPayment()
    )
    order1.add_item(Item("TXT-2265", "Software Engineering 10e", 89.99, 1))
    order1.add_item(Item("SUP-0042", "Engineering notebook", 6.50, 2))
    processor.process(order1)

    print()

    order2 = Order(
        1002,
        StaffCustomer("Dr. Kim", "kim@mctc.edu"),
        InvoicePayment()
    )
    order2.add_item(Item("SUP-0007", "Whiteboard markers", 12.00, 1))
    processor.process(order2)

    print()

    order3 = DigitalOrder(
        1003,
        StudentCustomer("Sam Ortiz", "sam@student.mctc.edu"),
        CampusCashPayment()
    )
    order3.add_item(Item("EBK-2265", "Software Engineering e-book", 54.00, 1))
    processor.process(order3)


if __name__ == "__main__":
    main()



