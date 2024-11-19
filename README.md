
# Server Load Tester (python)

A Python-based code for safely testing server behavior under traffic load from crawler-like Google Bot. This tool is designed to help evaluate server performance without causing disruption, making it an ideal choice for simulating controlled stress testing.

---

## Features

- **Rate Limiting**: Prevent server overload with configurable delays.
- **Realistic User Agents**: Simulate Googlebot and other common crawler behaviors.
- **Concurrent Users**: Test with multiple simultaneous users.
- **Crawler Path Simulation**: Evaluate server response to typical crawler traffic.
- **Detailed Logs**: Comprehensive reporting on requests, errors, and response times.
- **Safety Controls**: Built-in safeguards like timeouts and conservative defaults.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/edouardkombo/server-load-tester.git
   cd server-load-tester
   pip install -r requirements.txt || or python3 -m pip install -r requirements.txt
   ```
---

## Usage

Run the tool from the command line:

    python server_tester.py https://your-site.com --max-requests 100 --concurrent-users 5 --request-delay 1.0
    
---

## Arguments

- **--max-requests**: Total number of requests to send.
- **--concurrent-users**: Number of simultaneous users to simulate.
- **--request-delay**: Time delay (in seconds) between consecutive requests.

---

## How It Works

**Simulates Crawler Traffic**: Mimics real-world crawler activity with realistic user agents and paths.
**Adjustable Concurrency**: Configurable to test different levels of server load.
**Tracks Responses**: Logs request status, errors, and response times for analysis.

---

## Best Practices

Test Safely:
- Run tests on staging or development environments first.
- Use conservative settings initially (e.g., low concurrency, longer delays).
- Monitor Resources: Keep an eye on server performance during testing.
- Respect Robots.txt: Ensure compliance with server rules to avoid unintended issues.
- Notify Hosting Provider: Inform your hosting provider if planning extensive tests.

---

## Example Output

        Starting load test on: https://your-site.com
        Simulating 5 concurrent users for 100 requests.
        Request 1: 200 OK, Response Time: 0.345s
        Request 2: 503 Service Unavailable, Response Time: 1.234s
        ...
        Test completed. Success: 87, Failures: 13
        Average Response Time: 0.567s
    

---

## Contribution

Feel free to fork this repository and submit pull requests. Contributions are welcome!

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

