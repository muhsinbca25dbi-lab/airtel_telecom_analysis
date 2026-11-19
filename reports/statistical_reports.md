T.1

F-test:
- F = Check output
- p = Check output
- Decision: Check whether variances differ.

2-test:
- Z = Check output
- p > 0.05
Decision:
Fail to reject H₀.

Conclusion:
There is no statistically significant difference in the average revenue between Group A and Group B before the offer. Therefore, we fail to reject H₀.
---------------------------------------------------------------------------------------------------------------------------------
T.2

Z-test:
- Z = 2.5457
- p = 0.0109

Decision:
p = 0.0109 which is less than 0.05.
Reject H₀

Conclusion:
There is a statistically significant difference in the proportion of smartphone users between Group A and Group B.
---------------------------------------------------------------------------------------------------------------------------------
T.3

F-test:
F = Run f_test(A, B) output

p = Run output

Decision: Check whether variances differ.

Z-test:
Z = Run z_mean2(B, A) output

p = Run output

Decision:
- p < 0.05 → Reject H₀.
- p > 0.05 → Fail to reject H₀.

Conclusion:
If p is less than 0.05, there is sufficient statistical evidence that Group B has higher average daily data usage than Group A.
---------------------------------------------------------------------------------------------------------------------------------
T.4

F-test:
- F = f_test(b,a) output
- p = Output value

- Decision: Check whether variances differ.

T-test:
- t = Output value
- p = Output value

Decision:
- p < 0.05 → Reject H₀.
- p > 0.05 → Fail to reject H₀.

Conclusion:
If p < 0.05:

There is sufficient statistical evidence that Group B paid more on average than Group A. Therefore, the offer significantly increased revenue.
---------------------------------------------------------------------------------------------------------------------------------
T.5

Z-test:
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that prepaid and postpaid subscribers have different churn rates. Therefore, we reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------
T.6

Z-test:
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that subscribers with open tickets have a different churn rate compared to subscribers who never complained. Therefore, we reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------

T.7

Z-test:
- Group A: 1328 / 4610
- Group B: 632 / 3374
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that Year-0 and Year-3 subscribers have different churn rates. Therefore, we reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------
T.8

Z-test:
- Himachal Pradesh: 417 / 1247
- Punjab: 77 / 558
- Z = Check output
- p-value < 0.05

Decision:
Reject H₀
Since the p-value is less than 0.05, the result is statistically significant.

Conclusion:
There is sufficient statistical evidence that Himachal Pradesh and Punjab subscribers have different churn rates. Therefore, we reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------
T.9

Z-test:
- Smartphone: 4507 / 18971
- Feature-phone: 719 / 3029
- Z = Check output
- p-value > 0.05

Decision:
Fail to reject H₀
Since the p-value is greater than 0.05, the result is not statistically significant.

Conclusion:
There is insufficient statistical evidence to conclude that smartphone and feature-phone users have different churn rates. Therefore, we fail to reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------
T.10

Decision
- p < 0.05 → Reject H₀.
- p > 0.05 → Fail to reject H₀.

Conclusion
If p < 0.05, there is a statistically significant difference in average daily data usage between the groups.
One correction bro: dev query customer-wise average calculate cheyyunnathaanu. Gender/device comparison-inu gen use cheyyam.
---------------------------------------------------------------------------------------------------------------------------------
T.11

F-test
- Groups compared: Female vs Male
- p-value < 0.05
- Result: Significant difference in variances.

Z-test (Mean)
- Groups compared: Female vs Male
- p-value < 0.05

- Result: Significant difference in average daily data usage.

Decision
Reject H₀

Conclusion
There is sufficient statistical evidence to conclude that male and female subscribers have different average daily data usage.
---------------------------------------------------------------------------------------------------------------------------------
T12

Group Comparison
- Never roaming: 5,767 subscribers, 2,573 churned.
- Roaming users: 16,233 subscribers, 2,653 churned.
Z-proportion Test

Test: Two-sample Z-test for proportions.
- Never roaming churn rate: 44.61%.
- Roaming users churn rate: 16.34%.
- Z-statistic: -43.3361.
- P-value: Less than 0.05.
Decision

Reject H₀.

Since the p-value is less than 0.05, the result is statistically significant.

Conclusion
There is sufficient statistical evidence to conclude that subscribers who use roaming and subscribers who never use roaming have significantly different churn rates. Subscribers who never use roaming have a higher observed churn rate than subscribers who use roaming.
---------------------------------------------------------------------------------------------------------------------------------
T13

Group Comparison
- Groups compared: Male vs Female.
- Variable: Six-month recharge amount.
F-test

Test: F-test for variance comparison.
- F-statistic: 1.0202.
- P-value: 0.3036.
- Result: No statistically significant difference in variances.
Z-test (Mean)

Test: Two-sample Z-test for means.
- Groups compared: Male vs Female.
- Z-statistic: 0.2324.
- P-value: 0.8162.
- Result: No statistically significant difference in average six-month recharge amounts.
Decision

Fail to reject H₀.

Since the p-value is greater than 0.05, the result is not statistically significant.

Conclusion
There is insufficient statistical evidence to conclude that male and female subscribers have different average six-month recharge amounts. Therefore, we fail to reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------
T14

Group Comparison
- Groups compared: Feature Phone vs Smartphone.
- Variable: Average daily voice usage (minutes).
F-test

Test: F-test for variance comparison.
- F-statistic: 1.0115.
- P-value: 0.6731.
- Result: No statistically significant difference in variances.
Z-test (Mean)

Test: Two-sample Z-test for means.
- Groups compared: Feature Phone vs Smartphone.
- Z-statistic: 0.4166.
- P-value: 0.6770.
- Result: No statistically significant difference in average daily voice usage.
Decision

Fail to reject H₀.

Since the p-value is greater than 0.05, the result is not statistically significant.

Conclusion
There is insufficient statistical evidence to conclude that smartphone and feature-phone users have different average daily voice usage. Therefore, we fail to reject the null hypothesis (H₀).
---------------------------------------------------------------------------------------------------------------------------------