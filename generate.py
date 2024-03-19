import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data
num_samples = 1000

height_mean = 170
height_std = 10
height = np.random.normal(height_mean, height_std, num_samples)

# Adjust sugar intake mean and std
# Higher sugar intake is associated with higher risk of diabetes, and it increases with age
age_mean = 45                   # Older age is associated with higher risk of diabetes
age_std = 15                    # Increased variability in age
age = np.random.normal(age_mean, age_std, num_samples)

weekly_sugar_intake_mean = 200 + age * 2  # Adjust sugar intake mean based on age
weekly_sugar_intake_std = 60             # Increased variability in sugar intake
weekly_sugar_intake = np.random.normal(weekly_sugar_intake_mean, weekly_sugar_intake_std, num_samples)

# Adjust activity mean and std
weekly_activity_mean = 2        # Lower activity level is associated with higher risk of diabetes
weekly_activity_std = 0.5       # Decreased variability in activity
weekly_activity = np.random.normal(weekly_activity_mean, weekly_activity_std, num_samples)

# Adjust weight mean and std
weight_mean = 80                # Higher weight is associated with higher risk of diabetes
weight_std = 15                 # Increased variability in weight
weight = np.random.normal(weight_mean, weight_std, num_samples)

# Generate labels (0 for non-diabetic, 1 for diabetic)
# Adjust label probabilities based on known prevalence of diabetes
# Example: Assume 20% prevalence of diabetes
labels = np.random.choice([0, 1], size=num_samples, p=[0.8, 0.2])

# Create DataFrame
data = pd.DataFrame({
    'Height': height,
    'Weekly Sugar Intake': weekly_sugar_intake,
    'Weekly Activity': weekly_activity,
    'Weight': weight,
    'Age': age,
    'Diabetic': labels
})

# Save DataFrame to CSV
data.to_csv('diabetes_dataset.csv', index=False)
