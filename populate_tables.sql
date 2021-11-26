INSERT INTO finance_accounts (account)
SELECT
    DISTINCT account
FROM
    monthly_expenses_original


INSERT INTO monthly_income (income,source,income_category,dt)
SELECT
    income,
    source,
    category,
    dt
FROM
    monthly_original_original


INSERT INTO expense_categories (expense_category)
SELECT DISTINCT
    CASE SUBSTRING(category FROM 1 FOR (position('-' IN category)))
        WHEN ''
            THEN category
        ELSE 
            TRIM(TRAILING '-' FROM SUBSTRING(category FROM 1 FOR (position('-' IN category))))
    END category 
FROM
    monthly_expenses_original
ORDER BY category ASC


-- inserting into new expense table
-- referencing finance_accounts for account_id and expense_categories for category_id
INSERT INTO monthly_expenses (vendor,cost,category_id,account_id,dt,details)
SELECT
    meo.vendor,
    meo.cost,
    ec.category_id,
    fa.account_id,
    meo.dt,
    CASE position('-' IN meo.category)
        WHEN 0
            THEN ''
        ELSE 
            SUBSTRING(meo.category FROM (position('-' IN meo.category))+1 FOR LENGTH(meo.category))
    END details   
FROM
    monthly_expenses_original AS meo
JOIN finance_accounts fa ON fa.account = meo.account
JOIN expense_categories ec ON ec.expense_category =
    CASE position('-' IN meo.category)
        WHEN 0
            THEN meo.category
        ELSE
            TRIM(TRAILING '-' FROM SUBSTRING(meo.category FROM 1 FOR (position('-' IN meo.category))))
    END
ORDER BY dt ASC