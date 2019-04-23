#### C5 Lambda: Get Running Instance Info
- A lambda service will be needed to return information about the running instances
  - Participating instances will be identified by unique tags
  - Tags will contain summary display data about the init configuration

- Config details used to start each instance
  - branch
  - PR
  - expandable field to show optional config details
- Runtime info
  - instance id
  - DNS
    - URL's to the running applications: DNS + contextual by branch
  - Pre-set shutdown time
  - Link to Cloud Watch Logs for instance
    - Display docker-compose output

[
    {
        config: {
            branch: "text",
            pr: "text",
            started_by: "text",
            requested_timeslot: 60,
            environment: [
                {
                    name: "text",
                    values: "text"
                }
            ]
        },
        instance: {
            instance_id: "text",
            dns: "text",
            shutdown_time: "text",
            logs: "text",
             #varies by branch
            services: [
                {
                    name: "text",
                    url: "text"
                }
            ]
        }
    }
]
