import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
num_samples = 1000

# Generate age with higher variability
age_mean = 45
age_std = 10
age = np.random.normal(age_mean, age_std, num_samples)

# Adjust sugar intake based on age
weekly_sugar_intake_mean = 200 + (age - age_mean) * 2  # Sugar intake increases with age
weekly_sugar_intake_std = 60
weekly_sugar_intake = np.random.normal(weekly_sugar_intake_mean, weekly_sugar_intake_std, num_samples)

# Adjust activity based on age
# Higher activity level is associated with a lower risk of diabetes
weekly_activity_mean = 2 + (age - age_mean) * 0.05  # Activity increases with age
weekly_activity_std = 0.5
weekly_activity = np.random.normal(weekly_activity_mean, weekly_activity_std, num_samples)

# Generate approximate body fat percentage based on age and sugar intake
# Higher body fat percentage is associated with a higher risk of diabetes
body_fat_percentage_mean = 35 - (age - age_mean) * 0.2 - (weekly_sugar_intake - 200) * 0.02
body_fat_percentage_std = 5
body_fat_percentage = np.random.normal(body_fat_percentage_mean, body_fat_percentage_std, num_samples)

# Generate labels (0 for non-diabetic, 1 for diabetic)
# Adjust label probabilities based on known prevalence of diabetes
probability_of_diabetes = (
    0.15 +                                      # Base probability
    (age - 45) * 0.005 +                        # Age effect
    (weekly_sugar_intake - 200) * 0.001 +       # Sugar intake effect
    (2 - weekly_activity) * 0.05 +              # Activity effect (reverse relationship)
    (body_fat_percentage - 35) * 0.003          # Body fat percentage effect
)

# Bound probability values between 0 and 1
probability_of_diabetes = np.clip(probability_of_diabetes, 0, 1)

# Generate labels
labels = np.random.binomial(1, probability_of_diabetes)

# Generate height (not directly related to diabetes but included for completeness)
height_mean = 170
height_std = 10
height = np.random.normal(height_mean, height_std, num_samples)

# Create DataFrame
data = pd.DataFrame({
    'Height': height,
    'Weekly Sugar Intake': weekly_sugar_intake,
    'Weekly Activity': weekly_activity,
    'Body Fat Percentage': body_fat_percentage,
    'Age': age,
    'Diabetic': labels
})

# Save DataFrame to CSV
data.to_csv('diabetes_dataset.csv', index=False)
