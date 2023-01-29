# Finance
This program is a web application, built using the Python Flask framework, that allows users to register for an account to 'buy' and 'sell' stocks. Real company stock prices are obtained through the IEX API. The steps below assume you are running the program on Linux.

**Build**

Ensure Python 3 is installed on your system along with the following libraries (use pip install):

* cs50
* flask
* flask_session
* werkzeug
* requests
* urllib

Ensure SQLite3 is installed on your system by running
```shell
$ sudo apt install sqlite3
```

**Configure**

Before running the program, you need to register for an API key in order to be able to query IEX's data. To do so, follow these steps:

* Visit https://iexcloud.io/cloud-login#/register/.
* Select the “Individual” account type, then enter your name, email address, and a password, and click “Create account”.
* Once registered, scroll down to “Get started for free” and click “Select Start plan” to choose the free plan.
* Once you’ve confirmed your account via a confirmation email, visit https://iexcloud.io/console/tokens.
* Copy the key that appears under the Token column (it should begin with pk_).
* In your terminal window, execute:

```shell
export API_KEY=value
```
where value is that (pasted) value, without any space immediately before or after the =. You also may wish to paste that value in a text document somewhere, in case you need it again later.

**Usage**

Start Flask’s built-in web server (within finance/)
```shell
$ flask run
```
Visit the URL outputted by flask to see the distribution code in action.

