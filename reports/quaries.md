1. How much money did we receive from January to June 2025? (Overview Card 1)

sql
SELECT COUNT(*) AS payments,
       ROUND(SUM(amount_inr)/10000000.0, 2) AS crore_inr
FROM recharges
WHERE recharge_date BETWEEN '2025-01-01' AND '2025-06-30';
--------------------------------------------------------------------------------------------

2. Average monthly revenue per subscriber from payments received (Overview Card 3)

sql
SELECT ROUND(AVG(actual_arpu_6m), 2) AS avg_actual,
       ROUND(SUM(actual_arpu_6m), 0) AS monthly_total
FROM customer_features;
--------------------------------------------------------------------------------------------

3. How much does ARPU overstate money received? (Overview Card 3 note)

sql
SELECT ROUND(AVG(stated_arpu), 2) AS stated,
       ROUND(AVG(actual_arpu_6m), 2) AS actual,
       ROUND(AVG(arpu_gap), 2) AS gap,
       ROUND(100.0 * (SUM(stated_arpu) - SUM(actual_arpu_6m))
             / SUM(actual_arpu_6m), 2) AS over_pct
FROM customer_features;

--------------------------------------------------------------------------------------------
4. Is the gap the same for prepaid and postpaid? (Overview Hero and Support 1)

sql
SELECT connection_type, COUNT(*) AS subs,
       ROUND(AVG(stated_arpu), 2) AS stated,
       ROUND(AVG(actual_arpu_6m), 2) AS actual
FROM customer_features
GROUP BY connection_type;
--------------------------------------------------------------------------------------------

5. Which plans bring in the most actual monthly revenue? (Plan tab cards)

sql
SELECT plan_name, COUNT(*) AS subs,
       ROUND(SUM(actual_arpu_6m), 0) AS rev,
       ROUND(AVG(actual_arpu_6m), 2) AS per_sub
FROM customer_features
GROUP BY plan_name ORDER BY rev DESC LIMIT 5;

--------------------------------------------------------------------------------------------

WITH d AS (SELECT recharge_total_6m AS rev,
                  NTILE(10) OVER (ORDER BY recharge_total_6m DESC) AS dec_
           FROM customer_features),
     g AS (SELECT dec_, SUM(rev) AS rev FROM d GROUP BY dec_)
SELECT dec_, rev,
       ROUND(100.0 * rev / (SELECT SUM(rev) FROM g), 2) AS pct,
       ROUND(100.0 * SUM(rev) OVER (ORDER BY dec_)
             / (SELECT SUM(rev) FROM g), 2) AS cum_pct
FROM g ORDER BY dec_;
--------------------------------------------------------------------------------------------

A2. Plans by subscribers, with price (Plan selector order and Card 1)

sql
SELECT plan_name, plan_type, price_inr, COUNT(*) AS subs
FROM customer_features
GROUP BY plan_name, plan_type, price_inr
ORDER BY subs DESC;
--------------------------------------------------------------------------------------------

C5. Which payment channels take the most payments? (Plan Support 1)

sql
SELECT channel, COUNT(*) AS payments,
       ROUND(100.0*COUNT(*)/408089, 1) AS pct
FROM recharges GROUP BY channel ORDER BY payments DESC;
--------------------------------------------------------------------------------------------

 Do prepaid and postpaid pay through the same channels? (explains why channels differ by plan)

sql
SELECT txn_type, channel, COUNT(*) AS n,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY txn_type), 1) AS pct
FROM recharges GROUP BY txn_type, channel
ORDER BY txn_type, n DESC;

--------------------------------------------------------------------------------------------

L1. Revenue and churn by region (Plan Support 2 base)

sql
SELECT region, COUNT(*) AS subs,
       ROUND(SUM(actual_arpu_6m), 0) AS monthly_rev,
       ROUND(100.0*AVG(is_churned), 2) AS churn
FROM customer_features GROUP BY region ORDER BY churn DESC;

--------------------------------------------------------------------------------------------
L7. Revenue per subscriber by region (Plan Support 2, closest fit)

sql
SELECT region, COUNT(*) AS subs,
       ROUND(AVG(actual_arpu_6m), 2) AS arpu,
       ROUND(AVG(mb_per_active_day), 0) AS mb_per_day
FROM customer_features GROUP BY region ORDER BY arpu DESC;
--------------------------------------------------------------------------------------------
C3. Average payment by type (explains Prepaid vs Postpaid)

sql
SELECT txn_type, ROUND(AVG(amount_inr), 2) AS avg_amt,
       MIN(amount_inr) AS mn, MAX(amount_inr) AS mx
FROM recharges GROUP BY txn_type;
--------------------------------------------------------------------------------------------

C4. Number of payments in six months (why prepaid received falls short of stated)

sql
SELECT connection_type,
       ROUND(AVG(recharge_count), 2) AS payments,
       ROUND(AVG(recharge_total_6m), 0) AS total_6m
FROM customer_features GROUP BY connection_type;

--------------------------------------------------------------------------------------------
B9. Subscribers who paid nothing in six months (explains the stated-vs-received gap)

sql
SELECT SUM(recharge_count = 0) AS paid_nothing,
       ROUND(100.0 * AVG(CASE WHEN recharge_count = 0 THEN is_churned END), 2) AS their_churn,
       ROUND(AVG(stated_arpu), 2) AS base_stated_arpu
FROM customer_features;
--------------------------------------------------------------------------------------------