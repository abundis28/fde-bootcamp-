"""
Transaction processor for a freelancer finance tool.

It WORKS. That is not the point. This is a deliberately messy "God class" of the
kind you might inherit on a client site. Your job (see README/assignment) is to
DIAGNOSE its design problems in smells.md — no code changes yet.

Expected behavior is described in BEHAVIOR.md.
"""

import json
import smtplib   # (imagined) email sending
import sqlite3   # (imagined) database


class TransactionProcessor:
    def __init__(self):
        # The class creates its OWN concrete dependencies, inline.
        self.db = sqlite3.connect("transactions.db")
        self.smtp = smtplib.SMTP("smtp.example.com", 587)
        self.transactions = []

    def process(self, tx, customer_type, output_format, notify_channel):
        # 1) validate
        if "amount" not in tx or "description" not in tx:
            raise ValueError("bad transaction")

        # 2) compute the fee based on customer type (pricing rules)
        if customer_type == "free":
            fee = tx["amount"] * 0.03
        elif customer_type == "pro":
            fee = tx["amount"] * 0.02
        elif customer_type == "enterprise":
            fee = tx["amount"] * 0.01
        else:
            fee = tx["amount"] * 0.03

        # 3) compute tax set-aside based on category
        if tx["description"].startswith("INV"):
            tax = tx["amount"] * 0.25   # invoice income
        elif tx["description"].startswith("EXP"):
            tax = 0.0                   # expense
        else:
            tax = tx["amount"] * 0.15

        net = tx["amount"] - fee - tax
        record = {**tx, "fee": fee, "tax": tax, "net": net}
        self.transactions.append(record)

        # 4) persist it
        self.db.execute(
            "INSERT INTO tx (data) VALUES (?)", (json.dumps(record),)
        )
        self.db.commit()

        # 5) format the output for the caller
        if output_format == "json":
            out = json.dumps(record)
        elif output_format == "csv":
            out = f'{record["description"]},{record["amount"]},{record["net"]}'
        elif output_format == "text":
            out = f'{record["description"]}: net {record["net"]}'
        else:
            out = str(record)

        # 6) notify the user through the chosen channel
        if notify_channel == "email":
            self.smtp.sendmail("noreply@app.com", tx.get("email", ""), out)
        elif notify_channel == "sms":
            # pretend we call an SMS gateway here
            print(f"SMS to {tx.get('phone', '')}: {out}")
        elif notify_channel == "slack":
            # pretend we post to Slack here
            print(f"SLACK: {out}")

        return out

    def monthly_report(self, fmt):
        # builds a report; formatting logic duplicated from process()
        total_net = sum(t["net"] for t in self.transactions)
        if fmt == "json":
            return json.dumps({"total_net": total_net})
        elif fmt == "csv":
            return f"total_net,{total_net}"
        elif fmt == "text":
            return f"Total net: {total_net}"
        else:
            return str(total_net)
