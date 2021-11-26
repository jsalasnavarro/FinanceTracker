-- creating table of all accounts
CREATE TABLE finance_accounts (
    account_id SERIAL PRIMARY KEY,
    account VARCHAR(30) UNIQUE NOT NULL,
    balance money NOT NULL,
    account_type VARCHAR(15),
    dt DATE
);

-- creating history of account transactions table
CREATE TABLE finance_account_history (
    history_id SERIAL PRIMARY KEY,
    account_id INT,
    balance MONEY,
    dt DATE,
    FOREIGN KEY(account_id)
    REFERENCES finance_accounts(account_id)
);

-- creating table to track income
CREATE TABLE monthly_income (
    income_id SERIAL PRIMARY KEY,
    income money NOT NULL,
    source VARCHAR(30) NOT NULL,
    account_id INT,
    income_category VARCHAR(30) NOT NULL,
    dt DATE,
    FOREIGN KEY (account_id)
    REFERENCES finance_accounts(account_id)
);

-- creating table to track expense categories
CREATE TABLE expense_categories(
    category_id SERIAL PRIMARY KEY,
    expense_category varchar(30) NOT NULL UNIQUE
);


-- creating table to track individual expenses
CREATE TABLE monthly_expenses (
    expense_id BIGSERIAL PRIMARY KEY,
    income_id INT,
    vendor VARCHAR(30) NOT NULL,
    cost money NOT NULL,
    category_id INT,
    account_id INT,
    dt DATE,
    details varchar(50),
    FOREIGN KEY (income_id)
    REFERENCES monthly_income(income_id),
    FOREIGN KEY (category_id)
    REFERENCES expense_categories(category_id),
    FOREIGN KEY (account_id)
    REFERENCES finance_accounts(account_id)
);