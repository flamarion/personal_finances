from flask import Blueprint, render_template, request, jsonify, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy import exc
from pfv2.helpers import fixdate
from pfv2.models import Account, Category, Transaction, Budget
from pfv2.forms import TransactionForm
from pfv2 import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/frontpage', methods=['GET', 'POST'])
@main.route('/frontpage/<op>/<int:id>', methods=['GET', 'POST'])
@login_required
def frontpage(op=None, id=None):

    if request.method == "POST":
        # Retrieving form data
        tr_account = request.form['tr_account']
        tr_category = request.form['tr_category']
        # TODO: Set date format before insert
        tr_date = request.form['tr_date']
        tr_desc = request.form['tr_desc']
        tr_value = request.form['tr_value']
        tr_type = request.form['tr_type']
        tr_owner = current_user.id

        if op == "edit":
            transaction = Transaction.query.filter_by(id=id).filter_by(owner_id=current_user.id).first()

            transaction.name = tr_desc
            transaction.date = tr_date
            transaction.value = tr_value
            transaction.owner_id = tr_owner
            transaction.account_id = tr_account
            transaction.category_id = tr_category
            transaction.nature = tr_type

            try:
                db.session.commit()
                flash(f"Transaction {tr_desc} updated")
                return redirect(url_for('main.frontpage'))
            except:
                db.session.rollback()
                # I'm raising the exception to handle it correctly
                flash(f"Something went wrong to update the {tr_desc}")
                raise
            # TODO: Update the Account and Budget Balance based on tr_type
        else:
            # New transaction settings
            new_transaction = Transaction(name=tr_desc,
                                          date=tr_date,
                                          value=tr_value,
                                          owner_id=tr_owner,
                                          account_id=tr_account,
                                          category_id=tr_category,
                                          nature=tr_type)
            # TODO: Implement Update Account Balance
            try:
                db.session.add(new_transaction)
                db.session.commit()
                flash(f"New Transaction added: {tr_desc}", 'success')
                return redirect(url_for('main.frontpage'))
            except:
                db.session.rollback()
                flash('Unexpected error', 'danger')
                raise

            # TODO: Update the Account and Budget Balance based on tr_type

    else:

        form = TransactionForm()

        # Remove Budget
        if op == "rmtr":
            try:
                Transaction.query.filter_by(id=id).filter_by(owner_id=current_user.id).delete()
                db.session.commit()
                flash(f"Transaction Removed", 'danger')
                return redirect(url_for('main.frontpage'))
            except:
                db.session.rollback()
                # TODO: Handle the exception correctly.
                flash('Unexpected error', 'danger')
                raise

        # Edit budget
        elif op == "edittr":
            accounts = [(i.id, i.name) for i in Account.query.filter_by(owner_id=current_user.id).all()]
            categories = [(i.id, i.name) for i in Category.query.filter_by(owner_id=current_user.id).all()]
            form.tr_account.choices = accounts
            form.tr_category.choices = categories
            form.submit.label.text = 'Save'
            transaction = Transaction.query.filter_by(id=id).filter_by(owner_id=current_user.id).first()
            return render_template('edit_transaction.html', transaction=transaction, form=form)

        else:
            accounts = [(i.id, i.name) for i in Account.query.filter_by(owner_id=current_user.id).all()]
            categories = [(i.id, i.name) for i in Category.query.filter_by(owner_id=current_user.id).all()]
            form.tr_account.choices = accounts
            form.tr_category.choices = categories
            # TODO: Limit the number of results to N
            # incomes = Income.query.filter_by(owner_id=current_user.id).order_by(Income.date.desc()).limit(10).all
            transactions = Transaction.query.filter_by(owner_id=current_user.id).order_by(Transaction.date.desc()).all()
            return render_template('front_page.html', form=form, accounts=accounts, transactions=transactions)
