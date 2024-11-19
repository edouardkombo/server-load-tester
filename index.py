import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor
import argparse
from urllib.parse import urljoin
import logging

class ServerLoadTester:
    def __init__(self, base_url, max_requests=100, concurrent_users=5, 
                 request_delay=1.0, timeout=10):
        self.base_url = base_url
        self.max_requests = max_requests
        self.concurrent_users = concurrent_users
        self.request_delay = request_delay
        self.timeout = timeout
        self.success_count = 0
        self.error_count = 0
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Common crawler user agents for testing
        self.user_agents = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Googlebot-Image/1.0; +http://www.google.com/bot.html)',
            'Googlebot-News',
            'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36'
        ]
        
        # Common paths to test
        self.test_paths = [
            '/',
            '/robots.txt',
            '/sitemap.xml',
            '/news/',
            '/about/',
            '/contact/'
        ]

    def make_request(self, path):
        """Make a single request with safety controls"""
        try:
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
            }
            
            url = urljoin(self.base_url, path)
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            self.logger.info(f"Request to {url} - Status: {response.status_code}")
            
            if response.status_code == 200:
                self.success_count += 1
            else:
                self.error_count += 1
                
            return response.status_code
            
        except requests.exceptions.RequestException as e:
            self.error_count += 1
            self.logger.error(f"Error making request to {path}: {str(e)}")
            return None
        
        finally:
            # Enforce rate limiting
            time.sleep(self.request_delay)

    def run_test(self):
        """Run the load test with multiple concurrent users"""
        self.logger.info(f"Starting load test with {self.concurrent_users} concurrent users")
        self.logger.info(f"Maximum requests: {self.max_requests}")
        
        requests_made = 0
        results = []
        
        with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
            while requests_made < self.max_requests:
                # Submit batch of requests
                futures = []
                batch_size = min(self.concurrent_users, self.max_requests - requests_made)
                
                for _ in range(batch_size):
                    path = random.choice(self.test_paths)
                    futures.append(executor.submit(self.make_request, path))
                    requests_made += 1
                
                # Collect results
                for future in futures:
                    results.append(future.result())
                
                self.logger.info(f"Completed {requests_made} requests")
        
        # Report results
        self.logger.info("\nTest Results:")
        self.logger.info(f"Total Requests: {requests_made}")
        self.logger.info(f"Successful Requests: {self.success_count}")
        self.logger.info(f"Failed Requests: {self.error_count}")
        
        if self.success_count > 0:
            success_rate = (self.success_count / requests_made) * 100
            self.logger.info(f"Success Rate: {success_rate:.2f}%")

def main():
    parser = argparse.ArgumentParser(description='Server Load Testing Tool')
    parser.add_argument('url', help='Base URL of the server to test')
    parser.add_argument('--max-requests', type=int, default=100,
                        help='Maximum number of requests to make')
    parser.add_argument('--concurrent-users', type=int, default=5,
                        help='Number of concurrent users to simulate')
    parser.add_argument('--request-delay', type=float, default=1.0,
                        help='Delay between requests in seconds')
    
    args = parser.parse_args()
    
    tester = ServerLoadTester(
        args.url,
        max_requests=args.max_requests,
        concurrent_users=args.concurrent_users,
        request_delay=args.request_delay
    )
    tester.run_test()

if __name__ == '__main__':
    main()
