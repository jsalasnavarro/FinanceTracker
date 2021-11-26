-- export data as a csv
COPY (SELECT vendor, cost, category, payment_type, dt FROM monthly_expenses)
TO '/Users/jon/Downloads/monthly_expenses.csv'
WITH CSV HEADER


-- separates category and category details into two columns from archived expense table
-- used to insert columns into new expense_categories table
SELECT
    CASE position('-' IN category)
        WHEN 0
            THEN category
        ELSE 
            TRIM(TRAILING '-' FROM SUBSTRING(category FROM 1 FOR (position('-' IN category))))
    END category,
    CASE position('-' IN category)
        WHEN 0
            THEN ''
        ELSE 
            SUBSTRING(category FROM (position('-' IN category))+1 FOR LENGTH(category))
    END details   
FROM
    monthly_expenses_original
ORDER BY category ASC


-- match account id from new finance account table with account name from old expenses table
SELECT
    account_id,
    meo.account
FROM
    monthly_expenses_original AS meo
JOIN finance_accounts fa ON fa.account = meo.account
ORDER BY account_id

-- match category id from new table with category in archived table
SELECT 
    ec.category_id,
    CASE position('-' IN meo.category)
        WHEN 0
            THEN meo.category
        ELSE
            TRIM(TRAILING '-' FROM SUBSTRING(meo.category FROM 1 FOR (position('-' IN meo.category))))
    END category
FROM monthly_expenses_original AS meo
JOIN expense_categories ec ON ec.expense_category =
    CASE position('-' IN meo.category)
        WHEN 0
            THEN meo.category
        ELSE
            TRIM(TRAILING '-' FROM SUBSTRING(meo.category FROM 1 FOR (position('-' IN meo.category))))
    END
ORDER BY ec.category_id ASC


--selecting total monthly income and expenses
--for citi credit card select from 14th of previous month to current date (will only be applicable if c--urrent month   
--before 14th), for all other months select from first of current month to current date*/
SELECT sum(cost)
FROM (SELECT * FROM monthly_expenses
WHERE dt BETWEEN (SELECT MAKE_DATE((SELECT EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER), (SELECT EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER - 1),14)) AND CURRENT_DATE
AND account = 'citi'
UNION
SELECT * FROM monthly_expenses
WHERE dt BETWEEN (SELECT make_date((SELECT EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER), (SELECT EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER),1)) AND CURRENT_DATE
AND account <> 'citi') cost_total
UNION
SELECT sum(income) FROM monthly_income
WHERE dt BETWEEN (SELECT make_date((SELECT EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER), (SELECT EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER),1)) AND CURRENT_DATE