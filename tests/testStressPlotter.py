import matplotlib.pyplot as plt

# Sample data
passed_requests = 248  # Number of requests that passed
failed_requests = 252  # Number of requests that failed
total_elapsed_time = 5.13 # Total elapsed time in seconds
average_request_time = 3.1164  # Average request time in seconds

# Data for the bar chart
categories = [f'Passed ({passed_requests})', f'Failed ({failed_requests})']
values = [passed_requests, failed_requests]

# Creating the bar chart
plt.bar(categories, values, color=['green', 'red'])

# Adding title
plt.title(f'Total Requests: {passed_requests + failed_requests}')

# Adding labels
plt.xlabel('Request Status')
plt.ylabel('Number of Requests')

# Adjust y-axis limits to make the plot taller
max_value = max(values)
plt.ylim(0, max_value + 10)  # Add 10 units above the max value

# Adding text annotations with boxes in the top-right corner
annotation_1 = f'Total elapsed time: {total_elapsed_time}s'
annotation_2 = f'Average request time: {average_request_time:.2f}s'

# Position the annotations in the top-right corner
plt.text(0.95, 0.95, annotation_1, fontsize=12, ha='right', va='top', 
         transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.5'))

plt.text(0.95, 0.85, annotation_2, fontsize=12, ha='right', va='top', 
         transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.5'))

# Display the graph
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()