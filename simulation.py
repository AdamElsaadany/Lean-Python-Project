import simpy
import random
import statistics
import matplotlib.pyplot as plt

# --- Simulation Parameters (in minutes) ---
RANDOM_SEED = 42
AVG_COFFEE_TIME = 3 
CUSTOMER_INTERVAL = 2
SIM_TIME = 120

# Define the possible variations in service time and their probabilities.
time_variations = [
    AVG_COFFEE_TIME,
    AVG_COFFEE_TIME * 0.95, AVG_COFFEE_TIME * 0.90, AVG_COFFEE_TIME * 0.85,
    AVG_COFFEE_TIME * 0.80, AVG_COFFEE_TIME * 0.75, AVG_COFFEE_TIME * 1.05,
    AVG_COFFEE_TIME * 1.10, AVG_COFFEE_TIME * 1.15, AVG_COFFEE_TIME * 1.20,
    AVG_COFFEE_TIME * 1.25,
]
time_weights = [35, 20, 10, 5, 5, 5, 10, 5, 3, 1, 1]

# --- Simulation Process Functions ---

def coffee_shop(env, baristas, wait_times_list):
    """Defines the process for a single customer's visit."""
    arrival_time = env.now
    
    with baristas.request() as request:
        yield request
        
        served_time = env.now
        wait = served_time - arrival_time
        wait_times_list.append(wait)
        
        coffee_making_time = random.choices(time_variations, weights=time_weights, k=1)[0]
        yield env.timeout(coffee_making_time)

def setup(env, num_baristas, wait_times_list):
    """Initializes the simulation environment and generates customers."""
    # Create the barista resource with a given capacity.
    baristas = simpy.Resource(env, capacity=num_baristas)
    
    # Continuously generate new customers.
    customer_count = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / CUSTOMER_INTERVAL))
        customer_count += 1
        env.process(coffee_shop(env, baristas, wait_times_list))

# --- Simulation Runner ---

def run_simulation(num_baristas):
    """A wrapper function to run a complete simulation scenario and return the average wait time."""
    random.seed(RANDOM_SEED)
    wait_times = []
    
    env = simpy.Environment()
    env.process(setup(env, num_baristas, wait_times))
    env.run(until=SIM_TIME)
    
    return statistics.mean(wait_times)

# --- Main Program Execution ---

if __name__ == '__main__':
    # Store the results from both the 'As-Is' and 'To-Be' scenarios.
    results = {
        "1 Barista (As-Is)": run_simulation(num_baristas=1),
        "2 Baristas (To-Be)": run_simulation(num_baristas=2),
    }

    # Print a summary of the results to the terminal.
    print("\n--- Final Comparison ---")
    for scenario, wait_time in results.items():
        print(f"{scenario}: Average Wait Time = {wait_time:.2f} minutes")

    # --- Visualization ---
    
    # Prepare data for plotting.
    scenarios = list(results.keys())
    wait_times = list(results.values())
    
    # Create the plot figure and axes.
    plt.figure(figsize=(8, 6))
    bars = plt.bar(scenarios, wait_times, color=['#d45d5d', '#5dd467']) # Red for 'As-Is', Green for 'To-Be'
    
    # Add titles and labels for clarity.
    plt.title('Process Improvement: Average Customer Wait Time', fontsize=16)
    plt.ylabel('Average Wait Time (minutes)', fontsize=12)
    
    # Add data labels on top of each bar for readability.
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2f} min', va='bottom', ha='center', fontsize=12)

    # Save the generated figure to a file and display it.
    plt.savefig('simulation_results.png')
    plt.show()