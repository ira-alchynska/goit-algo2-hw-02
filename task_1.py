from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes the 3D printing queue based on priorities and printer constraints.

    Args:
        print_jobs: List of print jobs.
        constraints: Printer constraints.

    Returns:
        Dict containing the print order and the total time.
    """
    # Sort jobs by priority (highest priority first)
    print_jobs = sorted(print_jobs, key=lambda job: job['priority'])
    
    # Grouping jobs
    groups = []
    current_group = []
    current_group_volume = 0
    current_group_time = 0

    for job in print_jobs:
        # Check if the job can be added to the current group
        if (current_group_volume + job['volume'] <= constraints['max_volume']) and (len(current_group) < constraints['max_items']):
            current_group.append(job)
            current_group_volume += job['volume']
            current_group_time = max(current_group_time, job['print_time'])
        else:
            # Add the current group to the list of groups
            groups.append((current_group, current_group_time))
            # Create a new group with the current job
            current_group = [job]
            current_group_volume = job['volume']
            current_group_time = job['print_time']

    # Add the last group
    if current_group:
        groups.append((current_group, current_group_time))

    # Form the result
    print_order = []
    total_time = 0
    for group, group_time in groups:
        print_order.extend([job['id'] for job in group])
        total_time += group_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Testing
def test_printing_optimization():
    # Test 1: Jobs with the same priority
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Test 2: Jobs with different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90}, 
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150} 
    ]

    # Test 3: Exceeding volume constraints
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Test 1 (same priority):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Print order: {result1['print_order']}")
    print(f"Total time: {result1['total_time']} minutes")

    print("\nTest 2 (different priorities):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Print order: {result2['print_order']}")
    print(f"Total time: {result2['total_time']} minutes")

    print("\nTest 3 (exceeding constraints):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Print order: {result3['print_order']}")
    print(f"Total time: {result3['total_time']} minutes")

if __name__ == "__main__":
    test_printing_optimization()