import heapq
import random

class Event:
    """
    Store the properties of one event in the Schedule class defined below.
    Each event has:
      - timestamp: time at which it needs to run
      - function: the function to call when running the event
      - args and kwargs: arguments/keyword arguments to pass to that function
    """
    def __init__(self, timestamp, function, *args, **kwargs):
        self.timestamp = timestamp
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __lt__(self, other):
        """
        Overload the < operator so our priority queue knows how to compare two events.
        Events with earlier (smaller) times should go first.
        """
        return self.timestamp < other.timestamp

    def run(self, schedule):
        """
        Run an event by calling the function with its arguments. The first
        argument to any event function is always the schedule in which
        events are being tracked.
        """
        self.function(schedule, *self.args, **self.kwargs)


class Schedule:
    """
    An event schedule implemented as a priority queue using heapq.
    Provides methods to:
     - add events at a specific time
     - add events after a certain interval
     - run the next event
     - check what the next event time is
    """
    def __init__(self):
        self.now = 0.0
        self.priority_queue = []

    def add_event_at(self, timestamp, function, *args, **kwargs):
        heapq.heappush(
            self.priority_queue,
            Event(timestamp, function, *args, **kwargs)
        )

    def add_event_after(self, interval, function, *args, **kwargs):
        self.add_event_at(self.now + interval, function, *args, **kwargs)

    def next_event_time(self):
        return self.priority_queue[0].timestamp if self.priority_queue else float('inf')

    def run_next_event(self):
        if not self.priority_queue:
            return
        event = heapq.heappop(self.priority_queue)
        self.now = event.timestamp
        event.run(self)

    def __repr__(self):
        return f"Schedule(time={self.now}, events={len(self.priority_queue)})"

    def print_events(self):
        print(repr(self))
        for event in sorted(self.priority_queue):
            print(f"  {event.timestamp}: {event.function.__name__}")


class Queue:
    """
    Represents a single-server queue.
      - queue_length: how many people are waiting (not being served yet)
      - in_service: how many people are currently being served (0 or 1 here)
      - service_rate: the rate at which the server completes service (deterministic)
    """
    def __init__(self, service_rate):
        self.queue_length = 0
        self.in_service = 0
        self.service_rate = service_rate  # e.g., if service_rate=2, service time = 0.5

        # For visualization or statistics, we can store data over time:
        self.queue_length_history = []
        self.time_history = []

    def arrival(self, schedule):
        """
        Called whenever a traveler arrives. Increment the queue length.
        If the server is idle, immediately start service.
        """
        self.queue_length += 1
        self.record_state(schedule.now)   # record after the arrival

        # If no one is being served, start service immediately
        if self.in_service == 0:
            self.start_service(schedule)

    def start_service(self, schedule):
        """
        Starts service on a traveler (if available in the queue).
        Then schedule an event to end the service deterministically.
        """
        if self.queue_length > 0 and self.in_service == 0:
            self.queue_length -= 1
            self.in_service = 1
            self.record_state(schedule.now)

            # Deterministic service time is 1/self.service_rate
            service_time = 1.0 / self.service_rate
            schedule.add_event_after(service_time, self.end_service)

    def end_service(self, schedule):
        """
        Called when a service completes. If there is someone else
        in the queue, start serving them immediately.
        """
        self.in_service = 0
        self.record_state(schedule.now)

        if self.queue_length > 0:
            self.start_service(schedule)

    def record_state(self, time):
        """
        Record the current queue length for later visualization or debugging.
        """
        self.time_history.append(time)
        self.queue_length_history.append(self.queue_length + self.in_service)

    def __repr__(self):
        return (f"Queue(queue_length={self.queue_length}, "
                f"in_service={self.in_service}, "
                f"service_rate={self.service_rate})")


class Airport:
    """
    Holds one or more queues. Here we only demonstrate a single queue.
    This class schedules arrivals into its queue.
    """
    def __init__(self, arrival_rate, service_rate):
        self.arrival_rate = arrival_rate
        self.queue = Queue(service_rate=service_rate)

    def schedule_initial_arrival(self, schedule):
        """
        Schedule the first arrival.
        """
        # Exponential inter-arrival time
        inter_arrival_time = random.expovariate(self.arrival_rate)
        schedule.add_event_after(inter_arrival_time, self.handle_arrival)

    def handle_arrival(self, schedule):
        """
        When an arrival event occurs, add it to the queue.
        Then schedule the next arrival.
        """
        self.queue.arrival(schedule)
        # Schedule the next arrival
        inter_arrival_time = random.expovariate(self.arrival_rate)
        schedule.add_event_after(inter_arrival_time, self.handle_arrival)


def run_simulation(arrival_rate, service_rate, run_until):
    """
    Run an M/D/1 queue simulation with the specified arrival rate (λ),
    service rate (μ), and total run time.
    """
    # Initialize a schedule
    schedule = Schedule()

    # Create an airport with a single queue
    airport = Airport(arrival_rate=arrival_rate, service_rate=service_rate)

    # Schedule the first arrival
    airport.schedule_initial_arrival(schedule)

    # Run events until the next event time would exceed `run_until`
    while schedule.priority_queue and schedule.next_event_time() <= run_until:
        schedule.run_next_event()

    # Simulation is done. We can look at the queue stats.
    print("Simulation complete.")
    print("Final schedule state:", schedule)
    print("Final queue state:", airport.queue)

    # Example of simple textual visualization of queue length over time:
    print("\nTime vs. (Queue + In Service):")
    for t, q_len in zip(airport.queue.time_history, airport.queue.queue_length_history):
        print(f"  t={t:.2f}, length={q_len}")

    # You might plot these values using matplotlib, for example:
    # import matplotlib.pyplot as plt
    # plt.step(airport.queue.time_history, airport.queue.queue_length_history, where='post')
    # plt.xlabel('Time')
    # plt.ylabel('Number in System (Queue + Server)')
    # plt.title('M/D/1 Queue Length Over Time')
    # plt.show()


if __name__ == "__main__":
    # Example usage:
    # arrival_rate = 0.8 (on average 0.8 people arrive per time unit)
    # service_rate = 1.0 (on average 1 service completion per time unit => deterministic service time of 1.0)
    # run_until = 20.0 (simulation runs until time 20.0)
    run_simulation(arrival_rate=0.8, service_rate=1.0, run_until=20.0)
