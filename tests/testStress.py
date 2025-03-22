import asyncio
import httpx
import time
import numpy as np

async def make_request(client, endpoint):
    try:
        start_time = time.time()  # Start time for this request
        response = await client.get(endpoint)
        end_time = time.time()  # End time for this request
        return response.status_code, end_time - start_time  # Return status code and response time
    except Exception as e:
        return str(e), None  # Capture errors (e.g., connection errors)

async def main():
    # Set a reasonable connection limit
    limits = httpx.Limits(max_connections=500)
    async with httpx.AsyncClient(base_url="http://localhost:8000", limits=limits) as client:
        # Number of requests
        num_requests = 50

        # Start the timer for the entire test
        test_start_time = time.time()

        # Simulate concurrent requests
        tasks = [make_request(client, "/get-sessions/Guest") for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)

        # Stop the timer for the entire test
        test_end_time = time.time()

        # Calculate total time and average time per request
        total_time = test_end_time - test_start_time
        response_times = [time_taken for status_code, time_taken in results if time_taken is not None]
        avg_time_per_request = np.mean(response_times) if response_times else 0

        # Calculate percentiles
        p90 = np.percentile(response_times, 90) if response_times else 0
        p95 = np.percentile(response_times, 95) if response_times else 0

        # Count passed and failed requests
        passed = sum(1 for status_code, _ in results if status_code == 200)
        failed = len(results) - passed

        # Print results
        print(f"Total requests: {num_requests}")
        print(f"Passed: {passed}, Failed: {failed}")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Average time per request: {avg_time_per_request:.4f} seconds")
        print(f"90th percentile response time: {p90:.4f} seconds")
        print(f"95th percentile response time: {p95:.4f} seconds")

asyncio.run(main())