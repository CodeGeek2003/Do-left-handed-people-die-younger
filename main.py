import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# importing dataset
pure_data1 = "https://gist.githubusercontent.com/mbonsma/8da0990b71ba9a09f7de395574e54df1/raw/aec88b30af87fad8d45da7e774223f91dad09e88/lh_data.csv"
lefthanded_data = pd.read_csv(pure_data1)
# making plot to show the data in eyecatching way
fig, ax = plt.subplots()  # create figure and axis objects
ax.plot('Age', 'Female', data=lefthanded_data, marker='o')  # plot "Female" vs. "Age"
ax.plot('Age', "Male", data=lefthanded_data, marker='o')  # plot "Male" vs. "Age"
ax.legend()
ax.set_xlabel("Age")
ax.set_ylabel("Gender")
lefthanded_data = lefthanded_data.assign(Birth_year=1986 - lefthanded_data.Age)
lefthanded_data = lefthanded_data.assign(Mean_lh=lefthanded_data[["Male", "Female"]].mean(axis=1))
fig, ax = plt.subplots()
ax.plot('Birth_year', 'Mean_lh', data=lefthanded_data)  # plot 'Mean_lh' vs. 'Birth_year'
ax.set_xlabel("Mean_lh")
ax.set_ylabel("Birth_year")
# probability of left-handed given age of death
def P_lh_given_A(ages_of_death, study_year=1990):
    early_1900s_rate = lefthanded_data.Mean_lh.iloc[-10:].mean()
    late_1900s_rate = lefthanded_data.Mean_lh.iloc[:10].mean()
    middle_rates = lefthanded_data.loc[lefthanded_data['Birth_year'].isin(study_year - ages_of_death)]['Mean_lh']
    youngest_age = study_year - 1986 + 10  # the youngest age is 10
    oldest_age = study_year - 1986 + 86  # the oldest age is 86
    P_return = np.zeros(ages_of_death.shape)  # create an empty array to store the results
    # extract rate of left-handedness for people of ages 'ages_of_death'
    P_return[ages_of_death > oldest_age] = early_1900s_rate/100
    P_return[ages_of_death < youngest_age] = late_1900s_rate/100
    P_return[np.logical_and((ages_of_death <= oldest_age), (ages_of_death >= youngest_age))] = middle_rates / 100

    return P_return
# Death distribution data for the United States in 1999
pure_data2 = "https://gist.githubusercontent.com/mbonsma/2f4076aab6820ca1807f4e29f75f18ec/raw/62f3ec07514c7e31f5979beeca86f19991540796/cdc_vs00199_table310.tsv"
death_distribution_data = pd.read_csv(pure_data2, sep ='\t', skiprows=[1])
death_distribution_data=death_distribution_data.dropna(subset=['Both Sexes'])
# plot number of people who died as a function of age
fig, ax = plt.subplots()
ax.plot('Both Sexes', "Age", data =death_distribution_data, marker='o') # plot 'Both Sexes' vs. 'Age'
ax.set_xlabel("Both Sexes")
ax.set_ylabel("Age")
# sum over P_lh for each age group
def P_lh(death_distribution_data, study_year = 1990):
    p_list = death_distribution_data['Both Sexes'] * P_lh_given_A(death_distribution_data['Age'], study_year)
    p = np.sum(p_list)
    return p/np.sum(death_distribution_data['Both Sexes'])
print(P_lh(death_distribution_data))
#probability of being A years old given that you are left-handed
def P_A_given_lh(ages_of_death, death_distribution_data, study_year = 1990):
    P_A = death_distribution_data['Both Sexes'][ages_of_death] / np.sum(death_distribution_data['Both Sexes'])
    P_left = P_lh(death_distribution_data,
                  study_year)  # use P_lh function to get probability of left-handedness overall
    P_lh_A = P_lh_given_A(ages_of_death,
                          study_year)  # use P_lh_given_A to get probability of left-handedness for a certain age
    return P_lh_A * P_A / P_left
# plot the probability of being a particular age given that you're right-handed
def P_A_given_rh(ages_of_death, death_distribution_data, study_year = 1990):
    P_A = death_distribution_data['Both Sexes'][ages_of_death] / np.sum(death_distribution_data['Both Sexes'])
    P_right = 1-P_lh(death_distribution_data,
                  study_year) # either you're left-handed or right-handed, so P_right = 1 - P_left
    P_rh_A = 1- P_lh_given_A(ages_of_death,
                          study_year) # P_rh_A = 1 - P_lh_A
    return P_rh_A*P_A/P_right

ages = np.arange(6, 115, 1) # make a list of ages of death to plot
# calculate the probability of being left- or right-handed for each
left_handed_probability = P_A_given_lh(ages,death_distribution_data)
right_handed_probability = P_A_given_rh(ages,death_distribution_data)

# create a plot of the two probabilities vs. age
fig, ax = plt.subplots() # create figure and axis objects
ax.plot(ages, left_handed_probability, label = "Left-handed")
ax.plot(ages, right_handed_probability, label = "Right-handed")
ax.legend() # add a legend
ax.set_xlabel("Age at death")
ax.set_ylabel(r"Probability of being age A at death")
# calculate average ages for left-handed and right-handed groups
# use np.array so that two arrays can be multiplied
average_lh_age =  np.nansum(ages*np.array(left_handed_probability))
average_rh_age =  np.nansum(ages*np.array(right_handed_probability))

# print the average ages for each group
print("Average age of left handed" + str(average_lh_age))
print("Average age of right handed" + str(average_rh_age))
# print the difference between the average ages
print("The difference in average ages is " + str(round(average_rh_age - average_lh_age, 1)) + " years.")
# Calculate the probability of being left- or right-handed for all ages
left_handed_probability_2018 = P_A_given_lh(ages, death_distribution_data, 2018)
right_handed_probability_2018 = P_A_given_rh(ages, death_distribution_data, 2018)
# calculate average ages for left-handed and right-handed groups
average_lh_age_2018 = np.nansum(ages*np.array(left_handed_probability_2018))
average_rh_age_2018 = np.nansum(ages*np.array(right_handed_probability_2018))

print("The difference in  ages is " +str(round(average_rh_age_2018 - average_lh_age_2018, 1)) + " years.")
plt.show()