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
accounts. At the menu "Accounting > Adviser > Chart of Accounts", select
the accounts for planning and flag the field "Financial Planning".

#. Create financial forecast journal

Create a Financial Planning journal, which shall be of type "Bank".
Select the flag "Financial Planning".

#. Create a bank statements for Financial Planning

Create a bank statements related to the Financial Planning. You can call it
"Virtual Bank 2017", it might be useful to use one statement for a determined
period. Link it to the financial planning journal.


Usage
=============

#. Payables and receivables

At the menu "Finance > Others > Payables and Receivables" we see all account moves
we flagged initially for financial planning

#. create a template and add fixed cost lines

At the menu "Finance > Financial Planning > Templates" create a template, link it
to the "Virtual bank 2017" and cost lines.

 # - select the bank statement for financial planning


Open Points
=====

- The boolean Financial Planning on journal not very useful
- Link the virtual bank not to template but on each forecast ?
- take recurrent costs from previous month
- compute bank balance and print on note field (e.g)



Credits
=======

Contributors
------------

* Giacomo Grasso <giacomo.grasso.82@gmail.com>
