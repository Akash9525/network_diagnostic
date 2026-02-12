# Networking Concepts & Debugging Approach

## Health Checks

Health checks are automated probes used to determine whether a server or service is reachable and functioning correctly. They help detect failures early and improve system availability.

## Failover vs Redundancy

* **Redundancy** ensures backup resources are available to prevent single points of failure.
* **Failover** is the automated process of switching to a backup system when the primary system fails.

## Debugging Strategy

When diagnosing a network issue, follow a layered approach:

1. **DNS Check** – Ensure domain resolves correctly.
2. **Ping Test** – Verify host reachability.
3. **TCP Check** – Confirm required ports are open.
4. **HTTP Validation** – Validate application response.
5. **SSL Inspection** – Check certificate validity.

This structured method reduces Mean Time to Resolution (MTTR) during incidents.

## Security Considerations

Network failures may also result from firewall restrictions, WAF rules, rate limiting, or DDoS protection mechanisms. Proper monitoring and alerting are essential for proactive response.



## questions 

1.) How does this help in production?"

ans:-) Detect failures fast.

2.) "Why parallel execution?"

ans:-) Reduces diagnostic time.

3.) "Why retries?"

ans:-) Handles transient network failures.

4.) "What layer does ping test?"

ans:-) Network Layer (ICMP).