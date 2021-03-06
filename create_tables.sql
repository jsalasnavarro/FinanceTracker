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

-- added a new column to finance account history then created foreign
-- key to monthly_expenses table

ALTER TABLE finance_account_history
ADD COLUMN expense_id int;

ALTER TABLE finance_account_history
ADD CONSTRAINT con
FOREIGN KEY (expense_id)
REFERENCES monthly_expenses(expense_id);

ALTER TABLE finance_account_history
ADD COLUMN income_id int;

ALTER TABLE finance_account_history
ADD CONSTRAINT income
FOREIGN KEY (income_id)
REFERENCES monthly_income(income_id);

ALTER TABLE finance_account_history
ADD COLUMN transfer_id int;

ALTER TABLE finance_account_history
ADD CONSTRAINT transfer_id
FOREIGN KEY (transfer_id)
REFERENCES transfers(id);

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
    cost MONEY NOT NULL,
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

CREATE TABLE transfers (
    id SERIAL PRIMARY KEY,
    amount MONEY NOT NULL,
    from_id INT,
    to_id INT,
    details VARCHAR(50),
    dt DATE,
    FOREIGN KEY (from_id)
    REFERENCES finance_accounts(account_id),
    FOREIGN KEY (to_id)
    REFERENCES finance_accounts(account_id)
);