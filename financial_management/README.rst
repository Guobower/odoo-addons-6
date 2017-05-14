=========================
Financial Planning
=========================

This module introduces financial planning functionalities to Odoo.

Financial management is based on account moves and on bank statement lines
(for forecasting other costs and revenues not yet invoiced or not invoiceable).


Configuration
=============

To configure this module, you need to:

#. selects accounts for financial planning

This module forecasting is based on account moves, which are in turn related to
accounts. At the menu

#. create a template and add fixed cost lines
# - select the bank statement for financial planning

#. manage financial planning date in different objects:
 - account.invoice >> date_financial_planning
 - account.move >> financial_date


 (??) - account.move.user_type_id.type => internal_type

NOTES:
- check in invoice no final saldo updated >> ok
- when creating bank.line from forecast set date = financial_date >>0k!
- add financial balance on bank statement lines >> non fattibile
- !! when possible, update all SALDOS!! >> ok

Open Points
=====

- Multi-company
- What if I delete a forecast, links to is still missing.



Credits
=======

Contributors
------------

* Giacomo Grasso <giacomo.grasso.82@gmail.com>
