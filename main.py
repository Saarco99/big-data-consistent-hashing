import random
import numpy as np
import bisect
import matplotlib.pyplot as plt


class ConsistentHashing:
    def __init__(self, num_servers, num_keys):
        self.num_servers = num_servers
        self.num_keys = num_keys
        self.servers = []
        self.virtual_servers_unsorted = []
        self.virtual_servers = []
        self.keys = []
        self.virtual_copies = 4

    def generate_random_keys(self):
        self.keys = [random.randint(0, 2 ** 32 - 1) for _ in range(self.num_keys)]

    def generate_random_servers(self):
        self.servers = [random.randint(0, 2 ** 32 - 1) for _ in range(self.num_servers)]
        self.servers.sort()

    def assign_keys_to_servers(self):
        server_loads = [0] * len(self.servers)  # Initialize server loads with zeros
        for key in self.keys:
            server_id = self.find_server(key)
            server_loads[server_id] += 1
        return server_loads

    def assign_keys_to_virtual_servers(self):
        server_loads = [0] * len(self.servers)  # Initialize server loads with zeros
        for key in self.keys:
            real_server_id = self.find_virtual_server(key)
            server_loads[real_server_id] += 1
        return server_loads



    def find_server(self, key):
        index = bisect.bisect_left(self.servers, key)
        if index == len(self.servers):
            return 0
        return index

    def simulate_consistent_hashing(self):
        self.generate_random_keys()
        self.generate_random_servers()
        server_loads = self.assign_keys_to_servers()
        return server_loads

    def simulate_consistent_hashing_with_virtual_copies(self):
        self.generate_virtual_servers()
        self.generate_random_keys()
        virtual_server_loads = self.assign_keys_to_virtual_servers()
        return virtual_server_loads

    def generate_virtual_servers(self):
        for i in range(self.num_servers):
            for j in range(self.virtual_copies):
                virtual_server = random.randint(0, 2 ** 32 - 1)
                self.virtual_servers.append(virtual_server)

        self.assign_virtual_servers_to_servers()
        self.virtual_servers.sort()

    def assign_virtual_servers_to_servers(self):
        self.virtual_servers_unsorted = self.virtual_servers

    def find_virtual_server(self, key):
        index = bisect.bisect_left(self.virtual_servers_unsorted, key)
        if index == len(self.virtual_servers):
            return 0
        index = int(index/4)
        return index


# generate 4*self.num_servers numbers for each server
# and assign 4 virtual copies for each real server in self.servers


def calculate_load_metrics(load_values):
    median_load = np.median(load_values)
    average_load = np.mean(load_values)
    min_load = min(load_values)
    max_load = max(load_values)
    percentile_25 = np.percentile(load_values, 25)
    percentile_75 = np.percentile(load_values, 75)
    return median_load, average_load, min_load, max_load, percentile_25, percentile_75


def plot_load_distribution(load_values, title):
    plt.hist(load_values, bins=10, edgecolor='black')
    plt.title(title)
    plt.xlabel('Load')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


def main():
    num_servers = 100
    num_keys = 10000

    virtual_env = ConsistentHashing(num_servers, num_keys)

    # Simulate consistent hashing without virtual copies
    server_loads = virtual_env.simulate_consistent_hashing()
    metrics_without_virtual_copies = calculate_load_metrics(server_loads)
    print("Load Metrics without Virtual Copies:")
    show_servers_load(metrics_without_virtual_copies)
    plot_load_distribution(server_loads, "Load Distribution without Virtual Copies")

    # Simulate consistent hashing with virtual copies
    server_loads_with_virtual_copies = virtual_env.simulate_consistent_hashing_with_virtual_copies()
    metrics_with_virtual_copies = calculate_load_metrics(server_loads_with_virtual_copies)
    print("\nLoad Metrics with Virtual Copies:")
    show_servers_load(metrics_with_virtual_copies)
    plot_load_distribution(server_loads_with_virtual_copies, "Load Distribution with Virtual Copies")


def show_servers_load(metrics):
    print("Median Load:", metrics[0])
    print("Average Load:", metrics[1])
    print("Minimum Load:", metrics[2])
    print("Maximum Load:", metrics[3])
    print("25th Percentile Load:", metrics[4])
    print("75th Percentile Load:", metrics[5])


if __name__ == "__main__":
    main()
