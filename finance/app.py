import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query cash balance and initialise grand total variable
    cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    grand_total = cash_balance

    # Generate a list of unique stock names owned by the user
    unique_stock_symbols = db.execute("SELECT DISTINCT symbol FROM purchases WHERE user_id = ? ORDER BY symbol", session["user_id"])

    # Initalise lists for unique symbols and a full summary table
    symbols_list = []
    summary_list = []

    # Generate a list of unique stock symbols that the current user owns
    for unique_symbol in unique_stock_symbols:
        symbols_list.append(unique_symbol["symbol"])

    # Initalise a dictionary for each of these stock symbols
    for symbol in symbols_list:
        summary_list.append({"name": "0", "price": 0.0, "symbol": symbol, "quantity": 0.0, "total": 0.0})

    # For each stock, populate the summary details to display on the homepage
    for stock in summary_list:
        stock_details = lookup(stock["symbol"])

        stock["name"] = stock_details["name"]
        stock["price"] = stock_details["price"]

        shares_bought = db.execute("SELECT SUM(quantity) FROM purchases WHERE symbol = ?", stock["symbol"])
        shares_sold = db.execute("SELECT SUM(quantity) FROM sales WHERE symbol = ?", stock["symbol"])

        if (shares_sold[0]["SUM(quantity)"]) is None:
            (shares_sold[0]["SUM(quantity)"]) = 0

        current_shares_owned = (shares_bought[0]["SUM(quantity)"]) - (shares_sold[0]["SUM(quantity)"])

        stock["quantity"] = current_shares_owned
        stock["total"] = stock["price"] * stock["quantity"]
        grand_total += stock["total"]

    # Remove any stocks that are no longer owned
    for stock in summary_list:
        if stock["quantity"] == 0:
            summary_list.remove(stock)

    return render_template("index.html", cash_balance=cash_balance, grand_total=grand_total, summary_list=summary_list)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol and shares are entered
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        symbol = request.form.get("symbol")

        if not request.form.get("shares") or not request.form.get("shares").isnumeric():
            return apology("must provide valid number of shares")

        number_of_shares = int(request.form.get("shares"))

        if number_of_shares <= 0:
            return apology("input must be a positive integer")

        # Obtain quote through API and calculate total price
        if lookup(symbol) == None:
            return apology("symbol does not exist")

        stock_details = lookup(symbol)
        stock_unit_price = stock_details["price"]
        stock_total_price = float(number_of_shares) * stock_unit_price

        current_user_balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

        # Obtain current date and time
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check for sufficient funds
        if current_user_balance < stock_total_price:
            return apology("insufficient funds")

        # If funds are sufficient add the transaction to the purhcases table and deduct from cash balance
        elif current_user_balance > stock_total_price:

            db.execute("INSERT INTO purchases (user_id, name, price, symbol, quantity, time, type) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], stock_details["name"], stock_details["price"], stock_details["symbol"], number_of_shares, date_time, "buy")

            new_balance = current_user_balance - stock_total_price

            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])

            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Clear history table
    db.execute("DELETE FROM history")

    # Merge all transactions for the current user into the history table
    purchase_history = db.execute("SELECT * FROM purchases WHERE user_id = ?", session["user_id"])
    sales_history = db.execute("SELECT * FROM sales WHERE user_id = ?", session["user_id"])
    transaction_history = purchase_history + sales_history
    sorted_transaction_history = sorted(transaction_history, key=lambda d: d["time"], reverse=True)

    return render_template("history.html", sorted_transaction_history=sorted_transaction_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol = request.form.get("symbol")

        # Obtain quote through API
        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol")

        # Display quote
        return render_template("quoted.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    # check username and password
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if username == "" or len(db.execute('SELECT username FROM users WHERE username = ?', username)) > 0:
        return apology("Invalid Username: Blank, or already exists")

    if password == "" or password != confirmation:
        return apology("Invalid Password: Blank, or does not match")

    # Add new user to users db (includes: username and HASH of password)
    db.execute('INSERT INTO users (username, hash) VALUES(?, ?)', username, generate_password_hash(password))

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    # Log user in, i.e. Remember that this user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    current_user_balance = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Generate a list of unique stock names owned by the user
    unique_stock_symbols = db.execute("SELECT DISTINCT symbol FROM purchases WHERE user_id = ? ORDER BY symbol", session["user_id"])

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get symbol input
        if not request.form.get("symbol") or request.form.get("symbol") == "Select Stock":
            return apology("no stock was selected")

        stock_symbol = request.form.get("symbol")

        # Get number of shares to sell input

        if not request.form.get("shares"):
            return apology("must provide number of shares")

        shares_to_sell = int(request.form.get("shares"))

        if shares_to_sell < 0:
            return apology("input must be a positive integer")

        # Query the number of shares bough and sold for this stock
        shares_bought = db.execute("SELECT SUM(quantity) FROM purchases WHERE symbol = ? AND user_id = ?", stock_symbol, session["user_id"])
        shares_sold = db.execute("SELECT SUM(quantity) FROM sales WHERE symbol = ? AND user_id = ?", stock_symbol, session["user_id"])

        if (shares_sold[0]["SUM(quantity)"]) is None:
            (shares_sold[0]["SUM(quantity)"]) = 0

        # Check the current number of shares owned is sufficient for the sale
        current_shares_owned = (shares_bought[0]["SUM(quantity)"]) - (shares_sold[0]["SUM(quantity)"])

        if shares_to_sell > current_shares_owned:
            return apology("insufficeint shares owned")

        else:
            # Obtain current date and time
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add the transaction to the sales table and update cash balance
            stock_details = lookup(stock_symbol)

            db.execute("INSERT INTO sales (user_id, name, price, symbol, quantity, time, type) VALUES(?, ?, ?, ?, ?, ?, ?)", session["user_id"], stock_details["name"], stock_details["price"], stock_details["symbol"], shares_to_sell, date_time, "sell")

            sale_value = float(shares_to_sell) * stock_details["price"]

            new_balance = current_user_balance + sale_value
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html", unique_stock_symbols=unique_stock_symbols)
