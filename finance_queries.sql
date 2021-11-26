--
COPY (SELECT vendor, cost, category, payment_type, dt FROM monthly_expenses)
TO '/Users/jon/Downloads/monthly_expenses.csv'
WITH CSV HEADER

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


-- remove details of category, details follow'-'
SELECT DISTINCT TRIM(TRAILING '-' FROM CATEGORY)
FROM (
    SELECT
        SUBSTRING(category FROM 1 FOR (position('-' IN category))) AS category
    FROM
        monthly_expenses
    WHERE
        category<>'') new_category
WHERE
    category <> ''