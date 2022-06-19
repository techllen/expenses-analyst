SELECT * FROM expense_analyst_db.transactions;

DELETE FROM expense_analyst_db.transactions;

SELECT MAX(year) as current_year FROM(SELECT year FROM transactions AS years GROUP BY year) AS year;

SELECT * FROM transactions WHERE month = 11 AND year = 2022;

SELECT amount FROM transactions WHERE category = "Income" AND year = 2022;

SELECT amount FROM transactions WHERE amount = 0 AND year = 2022;

SELECT category, SUM(amount) 
AS category_total 
FROM transactions
WHERE year = 2022
GROUP BY category;


