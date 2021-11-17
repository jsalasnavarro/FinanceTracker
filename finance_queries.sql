// export table data to a csv
/*COPY (SELECT vendor, cost, category, payment_type, dt FROM monthly_expenses)
TO '/Users/jon/Downloads/monthly_expenses.csv'
WITH CSV HEADER*/

// selecting total monthly income and expenses
// for citi credit card select from 14th of previous month to current date (will only be applicable if current month   
// before 14th), for all other months select from first of current month to current date
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


/*SELECT * FROM monthly_income
ORDER BY dt DESC*/

/*UPDATE monthly_expenses
SET account = 'afcc'
WHERE dt BETWEEN '2021-11-01' AND '2021-11-16'
AND account = 'afc'*/